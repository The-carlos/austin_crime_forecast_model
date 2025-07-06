from google.cloud import bigquery
import pandas as pd
import os
from dotenv import load_dotenv

# Cargar variables desde .env
load_dotenv()

# Establecer credenciales desde variable de entorno
credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
if not credentials_path or not os.path.exists(credentials_path):
    raise FileNotFoundError(f"Credenciales no encontradas en: {credentials_path}")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

# Inicializar cliente
client = bigquery.Client()



# Consulta global (sin país)
QUERY = """
SELECT
  DATE(clearance_date) AS date_registered
  , CASE
    WHEN clearance_status NOT IN ("Not cleared") THEN "Cleared"
    ELSE clearance_status
  END AS clearance_status
  , COUNT(unique_key) AS cases
FROM
  `bigquery-public-data.austin_crime.crime`
WHERE TRUE
  AND clearance_date IS NOT NULL

GROUP BY 1,2
ORDER BY 1 ASC
"""


# Ejecutar consulta
query_job = client.query(QUERY, location="US")
df = query_job.result().to_dataframe()

# Asegurar tipo datetime
df["date_registered"] = pd.to_datetime(df["date_registered"])

# Renombrar columnas para Prophet
df = df.rename(columns={
    "date_registered": "ds",
    "cases": "y",
    "clearance_status": "status"
})

# Mostrar una muestra
print(df.head())

# Guardar resultados
os.makedirs("data", exist_ok=True)
df.to_csv("data/cleared_status_daily.csv", index=False)
print("✅ Datos guardados en data/cleared_status_daily.csv")