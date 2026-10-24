from prefect import flow, task
import subprocess

#--------------- TASKS ----------- #

@task
def ingest_data():
    subprocess.run(["python","analytics/ingestion/ingest_data.py"], check=True)

@task
def run_dbt():
    subprocess.run(["dbt", "run"], cwd="dbt", check=True)

@task
def forecast_germany():
    subprocess.run(["python","analytics/forecasting/german_prophet_forecast.py"],check=True)

@task
def forecast_france():
    subprocess.run(["python","analytics/forecasting/france_arima_forecast.py"],check=True)

@task
def forecast_spain():
    subprocess.run(["python","analytics/forecasting/spain_holt_winter_forcasts.py"],check=True)

@task
def seasonality():
    subprocess.run(["python", "analytics/seasonality/seasonality_all_countries.py"], check=True)

@task
def anomalies():
    subprocess.run(["python", "analytics/anomalies/detect_anomalies.py"], check=True)

@task
def volatility():
    subprocess.run(["python", "analytics/volatility/calc_volatility.py"], check=True)

@task
def evaluation():
    subprocess.run(["python", "analytics/evaluation/evaluate_models.py"], check=True)

@task
def load_to_postgres():
    subprocess.run(["python", "analytics/forecasting/load_forecasts_to_db.py"], check=True)

#----MASTER FLOW---#
@flow(name="energy_pipeline")
def energy_pipeline():
    ingest_data()
    run_dbt()
    forecast_germany()
    forecast_france()
    forecast_spain()
    seasonality()
    anomalies()
    volatility()
    evaluation()
    load_to_postgres()

#-----ENTRY POINT------#
if __name__ == "__main__":
    energy_pipeline()