import pandas as pd
import sqlalchemy as sa
from statsmodels.tsa.holtwinters import ExponentialSmoothing
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

# Load Spain daily averages
df = pd.read_sql("""
    SELECT date, avg_spain
    FROM daily_average_prices
    ORDER BY date
""", engine)

df = df.set_index("date")

# Holt-Winters model
model = ExponentialSmoothing(
    df["avg_spain"],
    trend="add",
    seasonal="add",
    seasonal_periods=7
)

fit = model.fit()

# Forecast 30 days
forecast_values = fit.forecast(30)

# Create proper DataFrame
forecast_df = pd.DataFrame({
    "date": pd.date_range(start=df.index[-1] + pd.Timedelta(days=1), periods=30, freq="D"),
    "forecast": forecast_values.values
})

# Save clean CSV
forecast_df.to_csv("data/forecasting/spain_price_forecast.csv", index=False)

print("Spain forecast saved correctly.")
