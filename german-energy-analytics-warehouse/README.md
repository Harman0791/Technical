
⭐ Project Overview
This project builds a complete analytics warehouse for European day‑ahead electricity prices (Germany, France, Spain).
It is designed to showcase the core skills expected from a modern data engineer:

Advanced SQL

dbt transformations

Dimensional modeling

Time‑series forecasting (Prophet, ARIMA, Holt‑Winters)

Data quality checks

Pipeline orchestration with Prefect

Postgres as the warehouse

Model evaluation (MAE, RMSE, MAPE)

Seasonality, volatility, anomaly detection

The entire system runs automatically through a Prefect flow.

⭐ Why Energy Data
Germany is undergoing a major energy transition. Electricity price behavior reflects:

1. renewable energy penetration

2. grid stability

3. seasonal patterns

4. volatility events

5. demand fluctuations

This makes energy data ideal for building a realistic analytics pipeline.


⭐ Architecture
                ┌──────────────────────────┐
                │   ENTSO‑E / OPSD API     │
                └──────────────┬───────────┘
                               ▼
                     Raw Data Ingestion
                               ▼
                    Postgres (raw tables)
                               ▼
                     dbt Transformations
                (daily averages, fact tables)
                               ▼
                     Forecasting Layer
        Germany → Prophet | France → ARIMA | Spain → Holt‑Winters
                               ▼
                     Forecast Tables in Postgres
                               ▼
                     Analytics & Evaluation
         (seasonality, anomalies, volatility, MAE/RMSE/MAPE)
                               ▼
                     Prefect Orchestration

