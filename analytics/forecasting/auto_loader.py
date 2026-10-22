import pandas as pd
from dotenv import load_dotenv
import os
import sqlalchemy as sa

load_dotenv()  # loads .env file

user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
db = os.getenv("POSTGRES_DB")
host = os.getenv("POSTGRES_HOST")
port = os.getenv("POSTGRES_PORT")

engine = sa.create_engine(
    f"postgresql://{user}:{password}@{host}:{port}/{db}"
)

def drop_dependent_views(table_name):
    """Automatically find and drop views that depend on a table."""
    query = f"""
        SELECT viewname
        FROM pg_views
        WHERE definition LIKE '%{table_name}%';
    """

    with engine.begin() as conn:
        views = conn.execute(sa.text(query)).fetchall()
        for (view,) in views:
            print(f"Dropping dependent view: {view}")
            conn.execute(sa.text(f"DROP VIEW IF EXISTS {view} CASCADE"))


def recreate_view(table_name):
    """Recreate the simple passthrough view."""
    view_name = f"forecast_{table_name.split('_')[0]}"
    with engine.begin() as conn:
        print(f"Recreating view: {view_name}")
        conn.execute(sa.text(
            f"CREATE VIEW {view_name} AS SELECT * FROM {table_name};"
        ))

def clean_forecast_df(df):
    # Spain: only 2 columns → add index column
    if len(df.columns) == 2:
        df.columns = ["date", "forecast"]
        df.insert(0, "ds", df["date"])  # rename date → ds
        return df[["ds", "forecast"]]

    # France: ARIMA output
    if "predicted_mean" in df.columns:
        df = df.rename(columns={"Unnamed: 0": "ds", "predicted_mean": "forecast"})
        return df[["ds", "forecast"]]

    # Germany: Prophet output
    if "ds" in df.columns and "yhat" in df.columns:
        df = df.rename(columns={"yhat": "forecast"})
        return df[["ds", "forecast"]]

    return df


def load_csv(csv_path, table_name):
    df = pd.read_csv(csv_path)
    df = clean_forecast_df(df)

    # 1. Drop dependent views
    drop_dependent_views(table_name)

    # 2. Drop table
    with engine.begin() as conn:
        print(f"Dropping table: {table_name}")
        conn.execute(sa.text(f"DROP TABLE IF EXISTS {table_name}"))

    # 3. Recreate table from CSV
    df.to_sql(
        table_name,
        engine,
        schema="public",
        if_exists="replace",
        index=False
    )
    print(f"Loaded {table_name} into Postgres.")

    # 4. Recreate view
    recreate_view(table_name)


# Germany
load_csv("data/forecasting/germany_forecast.csv", "germany_price_forecast")

# France
load_csv("data/forecasting/france_forecast.csv", "france_price_forecast")

# Spain
load_csv("data/forecasting/spain_forecast.csv", "spain_price_forecast")
