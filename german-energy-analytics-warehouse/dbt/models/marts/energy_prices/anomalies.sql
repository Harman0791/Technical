WITH enriched AS (
    SELECT
        date,
        hour_of_day,
        france,
        germany,
        italy,
        belgium,
        spain,
        uk,
        AVG(france)  OVER (
            ORDER BY date, hour_of_day
            ROWS BETWEEN 23 PRECEDING AND CURRENT ROW
        ) AS france_ra,
        AVG(germany) OVER (
            ORDER BY date, hour_of_day
            ROWS BETWEEN 23 PRECEDING AND CURRENT ROW
        ) AS germany_ra
    FROM {{ ref('facts_dayahead_prices') }}
)

SELECT
    date,
    hour_of_day,
    france,
    france_ra,
    (france - france_ra) AS france_deviation,
    CASE WHEN ABS(france - france_ra) > 20 THEN TRUE ELSE FALSE END AS france_anomaly,
    germany,
    germany_ra,
    (germany - germany_ra) AS germany_deviation,
    CASE WHEN ABS(germany - germany_ra) > 20 THEN TRUE ELSE FALSE END AS germany_anomaly
FROM enriched
ORDER BY date, hour_of_day