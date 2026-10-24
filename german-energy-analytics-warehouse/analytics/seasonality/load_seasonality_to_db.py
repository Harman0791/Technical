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

def load_csv_to_db(csv_path,table_name):
    df = pd.read_csv(csv_path)
    df.to_sql(
        table_name,
        engine,
        schema="public",
        if_exists="replace",
        index=False
    )
    print(f"Loaded {table_name} into Postgres.")

# Germany seasonality
load_csv_to_db(
    "data/seasonality/germany_seasonality.csv",
    "germany_seasonality"
)

# France seasonality
load_csv_to_db(
    "data/seasonality/france_seasonality.csv",
    "france_seasonality"
)

# Spain seasonality
load_csv_to_db(
    "data/seasonality/spain_seasonality.csv",
    "spain_seasonality"
)