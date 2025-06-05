
import pandas as pd

def baseline_forecast(data, steps=1):
    if len(data) == 0:
        return []
    last_value = data[-1]
    return [last_value] * steps
