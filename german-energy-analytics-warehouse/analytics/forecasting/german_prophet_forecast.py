from prophet import Prophet
from dotenv import load_dotenv
import os
import sqlalchemy as sa
import pandas as pd

load_dotenv()  # loads .env file

user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
db = os.getenv("POSTGRES_DB")
host = os.getenv("POSTGRES_HOST")
port = os.getenv("POSTGRES_PORT")

engine = sa.create_engine(
    f"postgresql://{user}:{password}@{host}:{port}/{db}"
)


# Load data from mart
query = """
    SELECT
      date,
      avg_germany
    FROM daily_average_prices
    ORDER BY date
"""
df = pd.read_sql(query, engine)
df = df.rename(columns={"date":"ds","avg_germany":"y"})

#Create and fit the prophet model
model = Prophet(
    daily_seasonality= False,
    weekly_seasonality= True,
    yearly_seasonality= True
)

model.fit(df)

# make a 30 day future dataframe
future = model.make_future_dataframe(periods=30)

#predict
forecast = model.predict(future)

#save the forecast
forecast.to_csv("data/forecasting/germany_forecast.csv",index=False)