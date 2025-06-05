
from fastapi import FastAPI, Query
from forecast_service.baseline_forecast import baseline_forecast
from forecast_service.ml_forecast import train_xgboost_model, load_model, forecast_with_model
import pandas as pd
import os

app = FastAPI()

DATA_PATH = "forecast_service/data/telemetry.csv"

def load_data():
    if os.path.exists(DATA_PATH):
        df = pd.read_csv(DATA_PATH)
        return df["value"].tolist()
    return []

@app.get("/forecast")
def get_forecast(steps: int = Query(5, ge=1, le=50)):
    data = load_data()
    model = load_model()
    if model:
        preds = forecast_with_model(model, data, steps)
    else:
        preds = baseline_forecast(data, steps)
    return {"forecast": preds}

@app.post("/train")
def train_model():
    data = load_data()
    model = train_xgboost_model(data)
    return {"status": "model trained"}
