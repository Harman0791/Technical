SELECT
  date,
  hour_of_day,
  germany - france AS de_vs_fr,
  germany - italy AS de_vs_it,
  germany - spain AS de_vs_es
FROM {{ ref('facts_dayahead_prices')}}
ORDER BY date, hour_of_day