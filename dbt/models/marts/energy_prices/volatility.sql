SELECT
  date,
  hour_of_day,

  ABS(france - LAG(france) OVER (ORDER BY date, hour_of_day)) AS france_volatility,
  ABS(germany - LAG(germany) OVER (ORDER BY date, hour_of_day)) AS germany_volatility,
  ABS(italy - LAG(italy) OVER (ORDER BY date, hour_of_day)) AS italy_volatility,
  ABS(belgium - LAG(belgium) OVER (ORDER BY date, hour_of_day)) AS belgium_volatility,
  ABS(spain - LAG(spain) OVER (ORDER BY date, hour_of_day)) AS spain_volatility,
  ABS(uk - LAG(uk) OVER (ORDER BY date, hour_of_day)) AS uk_volatility
FROM {{ ref('facts_dayahead_prices')}}
ORDER BY date, hour_of_day