--- SQL querries for the assigned tasks ---


-- Task 1 -- Find out 5 popular fligh connections --
SELECT 
    CONCAT(o.airport_code, ' → ', d.airport_code) AS route,
    COUNT(*) AS total_flights
FROM fact_flights f
JOIN dim_airport o ON f.origin_key = o.airport_key
JOIN dim_airport d ON f.dest_key = d.airport_key
GROUP BY route
ORDER BY total_flights DESC
LIMIT 5;


-- Task 2 -- Find out 10 most often cancelled flights ---
SELECT 
    CONCAT(o.airport_code, ' → ', d.airport_code) AS route,
    COUNT(*) AS total_flights
FROM fact_flights f
JOIN dim_airport o ON f.origin_key = o.airport_key
JOIN dim_airport d ON f.dest_key = d.airport_key
GROUP BY route
ORDER BY total_flights DESC
LIMIT 5;


-- Task 3 -- Find out the busiest days days with a yaer --
-- here i used 2007 as a case study because the data was spread across a large span of year --
SELECT
    d.full_date AS flight_date,
    COUNT(*) AS total_flights
FROM fact_flights f
JOIN dim_date d ON f.date_key = d.date_key
WHERE d.year = 2007
GROUP BY d.full_date
ORDER BY d.full_date;  -- THE DAYS WITH THE MOST NOISE ARE THE BUSIEST



-- Task 4 -- Find out the busiest weeks within a year --
SELECT
    CAST(EXTRACT(WEEK FROM d.full_date) AS INTEGER) AS week_number,
    COUNT(*) AS total_flights
FROM fact_flights f
JOIN dim_date d ON f.date_key = d.date_key
WHERE d.year = 2007
GROUP BY week_number
ORDER BY week_number;


-- Task 5 -- Personal business question --
-- Which airline operated the most flights in 2007--
SELECT 
    a.airline_code,
    COUNT(*) AS total_flights
FROM fact_flights f
JOIN dim_airline a ON f.airline_key = a.airline_key
JOIN dim_date d ON f.date_key = d.date_key
WHERE d.year = 2007
GROUP BY a.airline_code
ORDER BY total_flights DESC
LIMIT 1;
--- the answer is WN airline code ---