from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

freq = pd.read_csv("central_hourly_forecast.csv")  # ds, crime_frequency
types = pd.read_csv("central_top5_types_forecast.csv")  # ds, type, forecast

freq_map = dict(zip(freq["ds"], freq["crime_frequency"]))

@app.get("/forecast")
def forecast(date: str, hour: int):
    ds = f"{date} {hour:02d}:00:00"
    crime_freq = freq_map.get(ds, None)

    top5 = (types[types["ds"] == ds]
            .sort_values("forecast", ascending=False)
            .head(5)[["type", "forecast"]]
            .to_dict(orient="records"))

    return {"area": "Central", "ds": ds, "crime_frequency": crime_freq, "top5_types": top5}
