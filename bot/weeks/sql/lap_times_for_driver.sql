WITH RankedResults AS (
    SELECT id,
           league_id,
           season_id,
           week_id,
           driver_name,
           lap_time,
           points,
           last_updated,
           garage_lapid,
           ROW_NUMBER() OVER (ORDER BY lap_time ASC) AS position,
           COUNT(*) OVER () AS total_drivers
    FROM results
    WHERE league_id = %s AND season_id = %s AND week_id = %s
),
DriverPosition AS (
    SELECT position, total_drivers
    FROM RankedResults
    WHERE driver_name = %s
)
SELECT *
FROM RankedResults
WHERE position BETWEEN
    (SELECT CASE
                WHEN position = 1 THEN 1
                WHEN position = total_drivers THEN GREATEST(1, position - 2)
                ELSE GREATEST(1, position - 1)
            END
     FROM DriverPosition)
    AND
    (SELECT CASE
                WHEN position = 1 THEN LEAST(total_drivers, position + 2)
                WHEN position = total_drivers THEN total_drivers
                ELSE LEAST(total_drivers, position + 1)
            END
     FROM DriverPosition);