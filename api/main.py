# api/main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import joblib
from prophet.serialize import model_to_json, model_from_json
import os

app = FastAPI(title="Austin Crime Forecasting API")

# Define el esquema de entrada
class ForecastRequest(BaseModel):
    status: str  # "Cleared" o "Not cleared"
    horizon_days: int  # Número de días a predecir

# Ruta al directorio donde están los modelos
MODEL_DIR = "model"

# Endpoint principal
@app.post("/predict")
def predict(req: ForecastRequest):
    status = req.status.lower().replace(" ", "_")
    model_path = os.path.join(MODEL_DIR, f"prophet_{status}.joblib")

    # Validación de existencia del modelo
    if not os.path.exists(model_path):
        raise HTTPException(status_code=404, detail="Modelo no encontrado para el status proporcionado.")

    # Cargar modelo Prophet desde .joblib
    model = joblib.load(model_path)

    # Crear dataframe futuro
    future = model.make_future_dataframe(periods=req.horizon_days)

    # Hacer la predicción
    forecast = model.predict(future)

    # Seleccionar columnas relevantes
    response = forecast[["ds", "yhat"]].tail(req.horizon_days)
    result = response.to_dict(orient="records")

    return result
