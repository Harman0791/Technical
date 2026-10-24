WITH dedup AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY date, hour_of_day
            ORDER BY date
        ) AS rn
    FROM {{ ref('stg_entsoe_dayahead_prices') }}
)

SELECT
    date,
    hour_of_day,
    year,
    month,
    day,
    weekday,
    france,
    italy,
    belgium,
    spain,
    uk,
    germany
FROM dedup
WHERE rn = 1