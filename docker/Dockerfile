# docker/Dockerfile

# Imagen base oficial de Python
FROM python:3.10-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar archivos del proyecto
COPY requirements.txt .

# Instalar dependencias
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código fuente
COPY api/ ./api/
COPY model/ ./model/

# Exponer el puerto que usará FastAPI
EXPOSE 8080

# Comando por defecto para iniciar el servidor
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8080"]
