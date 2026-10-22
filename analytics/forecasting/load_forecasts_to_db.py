import pandas as pd
import sqlalchemy as sa
import os
from dotenv import load_dotenv

load_dotenv()  # loads .env file

user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
db = os.getenv("POSTGRES_DB")
host = os.getenv("POSTGRES_HOST")
port = os.getenv("POSTGRES_PORT")

engine = sa.create_engine(
    f"postgresql://{user}:{password}@{host}:{port}/{db}"
)


def load_csv(csv_path, table_name, country):
    df = pd.read_csv(csv_path)

    # Rename Prophet column to match DB schema
    if "yhat" in df.columns:
        df = df.rename(columns={"yhat": "forecast"})

    # Country-specific column alignment
    if country == "france":
        # France uses 'date'
        if "ds" in df.columns:
            df = df.rename(columns={"ds": "date"})
        df = df[["date", "forecast"]]

    elif country == "spain":
        # Spain CSV uses 'date', but DB expects 'ds'
        if "date" in df.columns:
            df = df.rename(columns={"date": "ds"})
        df = df[["ds", "forecast"]]

    else:
        # Germany uses 'ds'
        df = df[["ds", "forecast"]]

    with engine.begin() as conn:
        conn.execute(sa.text(f"TRUNCATE TABLE {table_name}"))

    df.to_sql(
        table_name,
        engine,
        schema="public",
        if_exists="append",
        index=False
    )

    print(f"Loaded {table_name} into Postgres.")


# Germany
load_csv("data/forecasting/germany_forecast.csv", "germany_price_forecast", "germany")

# France
load_csv("data/forecasting/france_forecast.csv", "france_price_forecast", "france")

# Spain
load_csv("data/forecasting/spain_price_forecast.csv", "spain_price_forecast", "spain")
