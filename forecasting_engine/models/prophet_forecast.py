from fbprophet import Prophet
import pandas as pd
import numpy as np

# Generate synthetic solar data (1 week of hourly data)
hours = pd.date_range("2025-01-01", "2025-01-07", freq="H")
irradiance = np.random.uniform(0, 1000, len(hours))  # W/m²
df = pd.DataFrame({"ds": hours, "y": irradiance})

# Train Prophet model
model = Prophet()
model.add_country_holidays(country_name='LK')  # Sri Lanka holidays
model.fit(df)

# Forecast next 24 hours
future = model.make_future_dataframe(periods=24, freq="H")
forecast = model.predict(future)

# Save forecast
forecast.to_csv("data/solar_forecast.csv", index=False)
print("Forecast saved to data/solar_forecast.csv")