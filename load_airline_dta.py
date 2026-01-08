import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="anton",
    user="user",
    password="password"
)
cur = conn.cursor()

print("Connected to Postgres.")

# Drop existing tables if needed
cur.execute("DROP TABLE IF EXISTS fact_flights CASCADE;")
cur.execute("DROP TABLE IF EXISTS dim_date CASCADE;")
cur.execute("DROP TABLE IF EXISTS dim_airline CASCADE;")
cur.execute("DROP TABLE IF EXISTS dim_airport CASCADE;")
cur.execute("DROP TABLE IF EXISTS staging_flights CASCADE;")

conn.commit()
print("Old tables dropped.")

# Create dimension tables
cur.execute("""
CREATE TABLE IF NOT EXISTS dim_date (
    date_key SERIAL PRIMARY KEY,
    full_date DATE UNIQUE,
    year INT,
    month INT,
    day INT
);
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS dim_airline (
    airline_key SERIAL PRIMARY KEY,
    airline_code VARCHAR(10) UNIQUE
);
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS dim_airport (
    airport_key SERIAL PRIMARY KEY,
    airport_code VARCHAR(10) UNIQUE
);
""")

# Create fact table
cur.execute("""
CREATE TABLE IF NOT EXISTS fact_flights (
    flight_id SERIAL PRIMARY KEY,
    date_key INT REFERENCES dim_date(date_key),
    airline_key INT REFERENCES dim_airline(airline_key),
    origin_key INT REFERENCES dim_airport(airport_key),
    dest_key INT REFERENCES dim_airport(airport_key),
    dep_delay FLOAT,
    arr_delay FLOAT,
    cancelled INT,
    diverted INT,
    distance FLOAT
);
""")

conn.commit()
print("Tables created.")

# Create staging table
cur.execute("""
CREATE TABLE IF NOT EXISTS staging_flights (
    flight_date DATE,
    airline_code VARCHAR(10),
    origin_code VARCHAR(10),
    dest_code VARCHAR(10),
    dep_delay FLOAT,
    arr_delay FLOAT,
    cancelled INT,
    diverted INT,
    distance FLOAT
);
""")

conn.commit()
print("Staging table created.")

csv_path = "airline_2m.csv"
chunksize = 50000
chunk_number = 1

for chunk in pd.read_csv(csv_path, encoding="ISO-8859-1", chunksize=chunksize, low_memory=False):
    print(f"Loading chunk {chunk_number}...")
    chunk = chunk[[
        "FlightDate", "Reporting_Airline", "Origin", "Dest",
        "DepDelay", "ArrDelay", "Cancelled", "Diverted", "Distance"
    ]]
    chunk.columns = ["flight_date", "airline_code", "origin_code", "dest_code", "dep_delay", "arr_delay", "cancelled", "diverted", "distance"]
    chunk = chunk.where(pd.notnull(chunk), None)
    rows = chunk.values.tolist()

    execute_values(cur, """
        INSERT INTO staging_flights (
            flight_date, airline_code, origin_code, dest_code,
            dep_delay, arr_delay, cancelled, diverted, distance
        ) VALUES %s
    """, rows)

    conn.commit()
    print(f"Chunk {chunk_number} loaded.")
    chunk_number += 1

print("All data loaded to staging.")

# Populate dimensions
cur.execute("""
INSERT INTO dim_date (full_date, year, month, day)
SELECT DISTINCT flight_date,
       EXTRACT(YEAR FROM flight_date),
       EXTRACT(MONTH FROM flight_date),
       EXTRACT(DAY FROM flight_date)
FROM staging_flights
WHERE flight_date IS NOT NULL
ON CONFLICT (full_date) DO NOTHING;
""")

cur.execute("""
INSERT INTO dim_airline (airline_code)
SELECT DISTINCT airline_code
FROM staging_flights
WHERE airline_code IS NOT NULL
ON CONFLICT (airline_code) DO NOTHING;
""")

cur.execute("""
INSERT INTO dim_airport (airport_code)
SELECT DISTINCT origin_code
FROM staging_flights
WHERE origin_code IS NOT NULL
ON CONFLICT (airport_code) DO NOTHING;
""")

cur.execute("""
INSERT INTO dim_airport (airport_code)
SELECT DISTINCT dest_code
FROM staging_flights
WHERE dest_code IS NOT NULL AND dest_code NOT IN (SELECT airport_code FROM dim_airport)
ON CONFLICT (airport_code) DO NOTHING;
""")

conn.commit()
print("Dimensions populated.")

# Populate fact table
cur.execute("""
INSERT INTO fact_flights (
    date_key, airline_key, origin_key, dest_key,
    dep_delay, arr_delay, cancelled, diverted, distance
)
SELECT 
    d.date_key,
    a.airline_key,
    o.airport_key,
    dest.airport_key,
    s.dep_delay,
    s.arr_delay,
    s.cancelled,
    s.diverted,
    s.distance
FROM staging_flights s
JOIN dim_date d ON s.flight_date = d.full_date
JOIN dim_airline a ON s.airline_code = a.airline_code
JOIN dim_airport o ON s.origin_code = o.airport_code
JOIN dim_airport dest ON s.dest_code = dest.airport_code
WHERE s.flight_date IS NOT NULL
  AND s.airline_code IS NOT NULL
  AND s.origin_code IS NOT NULL
  AND s.dest_code IS NOT NULL;
""")

conn.commit()
print("Fact table populated.")

# Drop staging
cur.execute("DROP TABLE staging_flights;")
conn.commit()
print("Staging table dropped.")

cur.close()
conn.close()
print("Star schema created successfully!")
