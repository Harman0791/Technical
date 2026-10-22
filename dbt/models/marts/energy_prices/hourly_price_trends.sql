SELECT
  date,
  hour_of_day,
  france,
  germany,
  belgium,
  italy,
  spain,
  uk,
  LAG(france) OVER (ORDER BY date, hour_of_day) AS france_prev,
  LAG(germany) OVER (ORDER BY date, hour_of_day) AS germany_prev
FROM {{ ref('facts_dayahead_prices') }}
ORDER BY date, hour_of_day
