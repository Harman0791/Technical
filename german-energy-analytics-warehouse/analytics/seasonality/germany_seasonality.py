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
# Load germany daily averages
df = pd.read_sql("""
     SELECT date, avg_germany
     FROM daily_average_prices
     ORDER BY date
""", engine)

df = df.set_index("date")

# STL decomposition (weekly seasonality = 7 days)
stl = STL(df["avg_germany"], period= 7)
result = stl.fit()

#save components
components = pd.DataFrame({
    "trend": result.trend,
    "seasonal":result.seasonal,
    "residual":result.resid
})

components.to_csv("data/seasonality/germany_seasonality.csv")
