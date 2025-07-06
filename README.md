# 🚨 Crime Forecast API (Austin, TX)

Este proyecto entrena un modelo de series de tiempo para predecir crímenes **resueltos** y **no resueltos** en Austin, Texas.  
Se despliega mediante FastAPI, Docker y Google Cloud Run.

---

## 🧠 ¿Qué resuelve este proyecto?

- Predicción del número de crímenes con base en datos históricos (2014–2017).
- Forecast separado por estatus: `"Cleared"` o `"Not cleared"`.
- Servicio en la nube accesible mediante una API REST.

---

## 🧭 Etapas del Proyecto

### 1. Extracción de datos desde BigQuery

Se consulta el dataset público:

```
bigquery-public-data.austin_crime.crime
```

- Se agrupan los crímenes por día y por estatus de resolución (`Cleared`, `Not cleared`).
- El script se encuentra en:  
  `notebooks/bigquery_extraction.py`

---

### 2. Procesamiento de los datos

- Se transforma el dataframe al formato esperado por Prophet: columnas `ds` y `y`.
- Se crean dos datasets: uno por cada estatus.
- El procesamiento ocurre dentro del archivo `model/train_model.py`.

---

### 3. Entrenamiento del modelo

- Se utiliza [Prophet](https://facebook.github.io/prophet/) para hacer forecasting.
- Se entrena un modelo para cada clase (`Cleared`, `Not cleared`).
- Los modelos se guardan con `joblib`.

Salida esperada:
```bash
✅ Modelo guardado en: model/prophet_cleared.joblib
✅ Modelo guardado en: model/prophet_not_cleared.joblib
```

---

### 4. Construcción de la API con FastAPI

- Ruta: `POST /predict`
- Entrada:
  ```json
  {
    "status": "Cleared",
    "horizon_days": 30
  }
  ```
- Salida: predicción de crímenes diarios para los próximos `n` días.
- Archivo principal: `api/main.py`

---

### 5. Dockerización

- Se crea un contenedor con todo el proyecto.
- Se expone el puerto `8080` (requerido por Cloud Run).
- Dockerfile en: `docker/Dockerfile`

Comandos usados:
```bash
docker build -f docker/Dockerfile -t crimes-api .
docker run -p 8080:8080 crimes-api
```

---

### 6. Despliegue en GCP

#### 🔐 Autenticación
```bash
gcloud auth configure-docker us-central1-docker.pkg.dev
```

#### 🏷️ Etiquetado y Push
```bash
docker tag crimes-api us-central1-docker.pkg.dev/YOUR_PROJECT_ID/crime-forecast-repo/crimes-api
docker push us-central1-docker.pkg.dev/YOUR_PROJECT_ID/crime-forecast-repo/crimes-api
```

#### ☁️ Despliegue en Cloud Run
```bash
gcloud run deploy crimes-api   --image=us-central1-docker.pkg.dev/YOUR_PROJECT_ID/crime-forecast-repo/crimes-api   --platform=managed   --region=us-central1   --allow-unauthenticated   --port=8080
```

---

### 7. Pruebas y Monitoreo

#### ✅ Probar desde Bash (recomendado)

```bash
curl -X POST https://crimes-api-XXXXXXXXXXXX.us-central1.run.app/predict   -H "Content-Type: application/json"   -d '{"status": "Cleared", "horizon_days": 30}'
```

#### ✅ Probar desde PowerShell

```powershell
$body = '{"status": "Cleared", "horizon_days": 30}'
Invoke-RestMethod -Uri "https://crimes-api-XXXXXXXXXXXX.us-central1.run.app/predict" `
  -Method Post `
  -Body $body `
  -ContentType "application/json"
```

#### ✅ Probar desde Postman

- Método: `POST`
- URL: `https://crimes-api-XXXXXXXXXXXX.us-central1.run.app/predict`
- Headers: `Content-Type: application/json`
- Body:
  ```json
  {
    "status": "Cleared",
    "horizon_days": 30
  }
  ```

---

## 📁 Estructura del Proyecto

```
simplest_google_trends_forecast_model/
├── api/              # Código de la API con FastAPI
│   └── main.py
├── data/             # (opcional) Datos descargados o procesados
├── docker/           # Dockerfile y configuraciones de contenedor
│   └── Dockerfile
├── gcp/              # Scripts para despliegue en GCP
│   └── cloudrun_deploy.sh
├── model/            # Entrenamiento y serialización del modelo
│   └── train_model.py
├── notebooks/        # Exploración y extracción de datos
│   └── bigquery_extraction.py
├── requirements.txt  # Dependencias del proyecto
├── .env              # Variables de entorno (no se sube al repo)
├── .gitignore
└── README.md         # Documentación principal
```

---

## 🚀 Tecnologías Usadas

- 🐍 Python
- 📊 Prophet
- 🌐 FastAPI
- 🐳 Docker
- ☁️ Google Cloud Run
- 📦 Artifact Registry
- 🔍 BigQuery

---

## 🧠 Autor

Desarrollado por [Carlos Sánchez](https://github.com/The-carlos) como práctica para proyectos de MLOps y despliegue de modelos en producción.
