SELECT
 date,
 AVG(france) AS avg_france,
 AVG(germany) AS avg_germany,
 AVG(belgium) AS avg_belgium,
 AVG(italy) AS avg_italy,
 AVG(spain) AS avg_spain,
 AVG(uk) AS avg_uk
FROM {{ ref('facts_dayahead_prices')}}
GROUP BY date
ORDER BY date
