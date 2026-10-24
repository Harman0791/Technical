WITH base AS (
    SELECT
        date,
        hour_of_day,
        france,
        germany,
        italy,
        belgium,
        spain,
        uk
    FROM {{ ref('facts_dayahead_prices') }}
)

SELECT
    date,
    hour_of_day,
    AVG(france)  OVER (
        ORDER BY date, hour_of_day
        ROWS BETWEEN 23 PRECEDING AND CURRENT ROW
    ) AS france_ra_24h,
    AVG(germany) OVER (
        ORDER BY date, hour_of_day
        ROWS BETWEEN 23 PRECEDING AND CURRENT ROW
    ) AS germany_ra_24h,
    AVG(italy)   OVER (
        ORDER BY date, hour_of_day
        ROWS BETWEEN 23 PRECEDING AND CURRENT ROW
    ) AS italy_ra_24h,
    AVG(belgium) OVER (
        ORDER BY date, hour_of_day
        ROWS BETWEEN 23 PRECEDING AND CURRENT ROW
    ) AS belgium_ra_24h,
    AVG(spain)   OVER (
        ORDER BY date, hour_of_day
        ROWS BETWEEN 23 PRECEDING AND CURRENT ROW
    ) AS spain_ra_24h,
    AVG(uk)      OVER (
        ORDER BY date, hour_of_day
        ROWS BETWEEN 23 PRECEDING AND CURRENT ROW
    ) AS uk_ra_24h
FROM base
ORDER BY date, hour_of_day