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

def calc():
    df = pd.read_sql("""
        SELECT date, hour_of_day, france, germany, belgium, italy, spain, uk,
               france_prev, germany_prev
        FROM hourly_price_trends
        ORDER BY date, hour_of_day
    """, engine)

    numeric_cols = ["france", "germany", "belgium", "italy", "spain", "uk",
                    "france_prev", "germany_prev"]

    vol = df.groupby("hour_of_day")[numeric_cols].std().reset_index()

    # FIX: write to a NEW table, not the dbt view
    vol.to_sql("volatility_python", engine, if_exists="replace", index=False)

    print("Volatility calculated and saved to volatility_python.")

if __name__ == "__main__":
    calc()
