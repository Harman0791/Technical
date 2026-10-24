import pandas as pd
import sqlalchemy as sa
from statsmodels.tsa.arima.model import ARIMA
from dotenv import load_dotenv
import os

load_dotenv()  # loads .env file

user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
db = os.getenv("POSTGRES_DB")
host = os.getenv("POSTGRES_HOST")
port = os.getenv("POSTGRES_PORT")

engine = sa.create_engine(
    f"postgresql://{user}:{password}@{host}:{port}/{db}"
)

query = """
    SELECT
        date,
        avg_france
    FROM daily_average_prices
    ORDER BY date
"""
df = pd.read_sql(query, engine)
df = df.set_index("date")

# ARIMA(p,d,q) — you can tune these later
model = ARIMA(df["avg_france"], order=(5, 1, 2))
fit = model.fit()

forecast_values = fit.forecast(steps=30)

#Create proper dataframe
forecast_df = pd.DataFrame({
    "date" :pd.date_range(start=df.index[-1] + pd.Timedelta(days=1), periods=30, freq="D"),
    "forecast": forecast_values.values
})

# Save forecast
forecast_df.to_csv("data/forecasting/france_forecast.csv")
print("France Forecast Saved Correctly")
