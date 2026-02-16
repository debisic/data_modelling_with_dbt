-- Trips Deduplication Statistics
-- Shows how many duplicate records were removed from both green and yellow trips

WITH before_dedup AS (
    SELECT 
        'Green' AS service_type,
        COUNT(*) AS total_records
    FROM {{ ref('stg_green_tripdata') }}
    
    UNION ALL
    
    SELECT 
        'Yellow' AS service_type,
        COUNT(*) AS total_records
    FROM {{ ref('stg_yellow_tripdata') }}
),

after_dedup AS (
    SELECT 
        service_type,
        COUNT(*) AS unique_records
    FROM {{ ref('fct_trips') }}
    GROUP BY service_type
),

statsistics AS (
    SELECT 
        b.service_type,
        b.total_records,
        a.unique_records,
        (b.total_records - a.unique_records) AS duplicates_removed,
        ROUND(100.0 * (b.total_records - a.unique_records) / b.total_records, 2) AS percent_duplicates
    FROM before_dedup b
    JOIN after_dedup a ON b.service_type = a.service_type
),

totals AS (
    SELECT
        'TOTAL' AS service_type,
        SUM(total_records) AS total_records,
        SUM(unique_records) AS unique_records,
        SUM(duplicates_removed) AS duplicates_removed,
        ROUND(100.0 * SUM(duplicates_removed) / SUM(total_records), 2) AS percent_duplicates
    FROM statsistics
),

all_results AS (
    SELECT * FROM statsistics
    UNION ALL
    SELECT * FROM totals
)

SELECT * 
FROM all_results
ORDER BY 
    CASE 
        WHEN service_type = 'Green' THEN 1
        WHEN service_type = 'Yellow' THEN 2
        WHEN service_type = 'TOTAL' THEN 3
    END
