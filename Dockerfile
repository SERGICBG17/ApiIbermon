# Dockerfile para ApiIbermon
FROM python:3.12-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema necesarias para compilar paquetes Python
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    libffi-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements.txt e instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY app ./app

# Copiar datos estaticos (sprites de iniciales, seeds, etc.)
COPY data ./data

# Exponer el puerto 8000
EXPOSE 8000

# Comando para ejecutar la aplicación con uvicorn
# Las variables de entorno se pasan desde docker-compose o docker run
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]