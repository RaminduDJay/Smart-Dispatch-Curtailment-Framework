
import pandas as pd
import numpy as np
import xgboost as xgb
import joblib
import os

MODEL_PATH = "forecast_service/data/model/xgboost_model.pkl"

def train_xgboost_model(data, window_size=5):
    X, y = [], []
    for i in range(len(data) - window_size):
        X.append(data[i:i+window_size])
        y.append(data[i+window_size])
    model = xgb.XGBRegressor()
    model.fit(np.array(X), np.array(y))
    joblib.dump(model, MODEL_PATH)
    return model

def load_model():
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    return None

def forecast_with_model(model, data, steps=1):
    preds = []
    window = data[-5:]
    for _ in range(steps):
        pred = model.predict([window])[0]
        preds.append(pred)
        window = window[1:] + [pred]
    return preds
