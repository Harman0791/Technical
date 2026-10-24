import pandas as pd
import sqlalchemy as sa
from statsmodels.tsa.seasonal import STL
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

def run_stl(country, column):
    df = pd.read_sql(f"""
        SELECT date, {column}
        FROM daily_average_prices
        ORDER BY date
    """, engine)

    df = df.set_index("date")

    stl = STL(df[column], period=7)
    result = stl.fit()

    components = pd.DataFrame({
        "date": df.index,
        "trend": result.trend,
        "seasonal": result.seasonal,
        "residual": result.resid
    })

    components.to_sql(f"{country}_seasonality", engine, if_exists="append", index=False)
    print(f"{country.capitalize()} seasonality saved.")

def main():
    run_stl("germany", "avg_germany")
    run_stl("france", "avg_france")
    run_stl("spain", "avg_spain")

if __name__ == "__main__":
    main()
