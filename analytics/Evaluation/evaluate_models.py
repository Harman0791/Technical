import pandas as pd
from dotenv import load_dotenv
import os
import sqlalchemy as sa
import numpy as np

load_dotenv()  # loads .env file

user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
db = os.getenv("POSTGRES_DB")
host = os.getenv("POSTGRES_HOST")
port = os.getenv("POSTGRES_PORT")

engine = sa.create_engine(
    f"postgresql://{user}:{password}@{host}:{port}/{db}"
)

def evaluate(actual_df, forecast_df, actual_col):
    # Detect merge key
    merge_key = "ds" if "ds" in forecast_df.columns else "date"

    # Normalize date formats
    actual_df["date"] = pd.to_datetime(actual_df["date"]).dt.date
    forecast_df[merge_key] = pd.to_datetime(forecast_df[merge_key]).dt.date

    # Restrict actuals to forecast range
    min_date = forecast_df[merge_key].min()
    max_date = forecast_df[merge_key].max()

    actual_df = actual_df[
        (actual_df["date"] >= min_date) &
        (actual_df["date"] <= max_date)
    ]

    # Merge
    df = pd.merge(
        actual_df,
        forecast_df,
        left_on="date",
        right_on=merge_key,
        how="inner"
    )

    print(f"Merged rows for {actual_col}: {len(df)}")

    if len(df) == 0:
        return np.nan, np.nan, np.nan

    actual = df[actual_col]
    pred = df["forecast"]

    mae = np.mean(np.abs(actual - pred))
    rmse = np.sqrt(np.mean((actual - pred)**2))
    mape = np.mean(np.abs((actual - pred) / actual)) * 100

    return mae, rmse, mape

    
# 1. Load actuals
actuals = pd.read_sql(
    "SELECT date, avg_germany, avg_france, avg_spain FROM daily_average_prices",
    engine
)

# 2. Load forecasts from views (already pointing to the right tables)
germany_fc = pd.read_sql("SELECT * FROM forecast_germany", engine)
france_fc  = pd.read_sql("SELECT * FROM forecast_france", engine)
spain_fc   = pd.read_sql("SELECT * FROM forecast_spain", engine)

results = []

# Germany
mae, rmse, mape = evaluate(actuals, germany_fc, "avg_germany")
results.append(["Germany", mae, rmse, mape])

# France
mae, rmse, mape = evaluate(actuals, france_fc, "avg_france")
results.append(["France", mae, rmse, mape])

# Spain
mae, rmse, mape = evaluate(actuals, spain_fc, "avg_spain")
results.append(["Spain", mae, rmse, mape])

df_results = pd.DataFrame(results, columns=["country", "mae", "rmse", "mape"])
df_results.to_sql("model_evaluation", engine, if_exists="replace", index=False)

print("Model Evaluation is complete and loaded into Postgres")