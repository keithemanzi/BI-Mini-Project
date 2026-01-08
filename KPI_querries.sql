-- Ratio Between Cancelled Flights and Airline
-- Ratio ---
SELECT 
    100.0 * SUM(CASE WHEN f.cancelled = 1 THEN 1 ELSE 0 END) / COUNT(*) 
    AS cancellation_rate
FROM fact_flights f;

-- Metabase chart visualisation code --
SELECT 
    a.airline_code,
    100.0 * SUM(CASE WHEN f.cancelled = 1 THEN 1 ELSE 0 END) / COUNT(*) 
        AS cancellation_ratio
FROM fact_flights f
JOIN dim_airline a ON f.airline_key = a.airline_key
GROUP BY a.airline_code
ORDER BY cancellation_ratio DESC;



-- Ratio between delazed flights and airlines ---
-- code for the ratio ---
SELECT 
    100.0 * SUM(CASE WHEN f.dep_delay > 0 THEN 1 ELSE 0 END) / COUNT(*) 
        AS delay_rate
FROM fact_flights f;
-- Metabase chart visualisation code --
SELECT 
    a.airline_code,
    100.0 * SUM(CASE WHEN f.dep_delay > 0 THEN 1 ELSE 0 END) / COUNT(*) 
        AS delay_ratio
FROM fact_flights f
JOIN dim_airline a ON f.airline_key = a.airline_key
GROUP BY a.airline_code
ORDER BY delay_ratio DESC;



-- Ratio between delayed flights and destination airports --
-- code for the ratio ---
SELECT 
    100.0 * SUM(CASE WHEN dep_delay > 0 THEN 1 ELSE 0 END) / COUNT(*) 
        AS delay_rate
FROM fact_flights;
-- Metabase chart visualisation code --
SELECT 
    ap.airport_code AS destination_airport,
    100.0 * SUM(CASE WHEN f.dep_delay > 0 THEN 1 ELSE 0 END) / COUNT(*) 
        AS delay_ratio
FROM fact_flights f
JOIN dim_airport ap ON f.dest_key = ap.airport_key
GROUP BY ap.airport_code
ORDER BY delay_ratio DESC
LIMIT 10;



-- Ratio between delayed flights and departure airports --
-- code for the ratio ---
SELECT 
    100.0 * SUM(CASE WHEN dep_delay > 0 THEN 1 ELSE 0 END) / COUNT(*) 
        AS overall_delay_rate
FROM fact_flights;
-- Metabase chart visualisation code --
SELECT
    ap.airport_code AS departure_airport,
    100.0 * SUM(CASE WHEN f.dep_delay > 0 THEN 1 ELSE 0 END) / COUNT(*) 
        AS delay_ratio
FROM fact_flights f
JOIN dim_airport ap ON f.origin_key = ap.airport_key
GROUP BY ap.airport_code
ORDER BY delay_ratio DESC
LIMIT 10;

-- fOR MY PERSONAL QUESTION 
-- aIRPORT WITH THE HIGHEST NET INFLOW OF FLIGHTS (ARRIVALS - DEPARTURES) 
WITH flows AS (
    SELECT 
        ap.airport_code,
        SUM(CASE WHEN f.dest_key = ap.airport_key THEN 1 ELSE 0 END) AS arrivals,
        SUM(CASE WHEN f.origin_key = ap.airport_key THEN 1 ELSE 0 END) AS departures
    FROM dim_airport ap
    JOIN fact_flights f 
        ON f.dest_key = ap.airport_key OR f.origin_key = ap.airport_key
    GROUP BY ap.airport_code
)
SELECT 
    airport_code,
    (arrivals - departures) AS net_flow
FROM flows
ORDER BY net_flow DESC
LIMIT 1;
-- this was visualised using a flanel chart in metabase