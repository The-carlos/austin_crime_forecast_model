# train_model.py

import pandas as pd
from prophet import Prophet
import joblib
import os

# Cargar datos
df = pd.read_csv("data/cleared_status_daily.csv")

# Asegurar formato de fecha
df["ds"] = pd.to_datetime(df["ds"])

# Crear carpeta para modelos si no existe
os.makedirs("model", exist_ok=True)

# Entrenar y guardar un modelo por cada status
statuses = df["status"].unique()

for status in statuses:
    print(f"Entrenando modelo para: {status}")

    df_status = df[df["status"] == status][["ds", "y"]]

    model = Prophet()
    model.fit(df_status)

    model_filename = f"model/prophet_{status.lower().replace(' ', '_')}.joblib"
    joblib.dump(model, model_filename)

    print(f"✅ Modelo guardado en: {model_filename}")
