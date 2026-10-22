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


def ingest():
    df = pd.read_csv("data/raw/day_ahead_prices.csv")
    df.to_sql("raw_prices", engine, if_exists="replace", index=False)
    print("Raw data ingested into Postgres.")

if __name__ == "__main__":
    ingest()
