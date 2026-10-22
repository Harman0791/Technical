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


def detect():
    df = pd.read_sql("""
        SELECT date, residual
        FROM germany_seasonality
        ORDER BY date
    """, engine)

    threshold = df["residual"].std() * 3
    df["anomaly_flag"] = df["residual"].abs() > threshold

    # Write to a NEW table, not the dbt view
    df.to_sql("anomalies_python", engine, if_exists="replace", index=False)
    print("Anomalies detected and saved to anomalies_python.")

if __name__ == "__main__":
    detect()
