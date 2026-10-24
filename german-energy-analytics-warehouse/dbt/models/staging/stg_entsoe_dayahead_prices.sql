SELECT
 date,
 hour,
COALESCE(france, 0) AS france,
COALESCE(germany, 0) AS germany,
COALESCE(italy, 0) AS italy,
COALESCE(belgium, 0) AS belgium,
COALESCE(spain, 0) AS spain,
COALESCE(uk, 0) AS uk,

--Derived fields
 EXTRACT(YEAR FROM date) AS year,
 EXTRACT(MONTH FROM date) AS month,
 EXTRACT(DAY FROM date) AS day,
 TO_CHAR(date, 'Day') AS weekday,
 hour AS hour_of_day

FROM {{ source('energy_raw','entsoe_dayahead_prices') }}