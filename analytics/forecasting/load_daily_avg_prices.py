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

# 2. Read daily_avg_prices mart
query = """
  SELECT
    date,
    avg_germany
  FROM daily_average_prices
  ORDER BY date
"""
df = pd.read_sql(query, engine)

# 3. Prepare for prophet (rename columns)
df = df.rename(columns={"date":"ds","avg_germany":"y"})
print(df.head())