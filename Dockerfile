# 1. Usamos una imagen ligera de Python
FROM python:3.11-slim

# 2. Evitamos que Python genere archivos .pyc y que el buffer se sature
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 3. Instalamos dependencias del sistema necesarias para psycopg2 y sockets
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 4. Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /app

# 5. Copiamos e instalamos las dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copiamos todo el proyecto (incluyendo templates y static)
COPY . .

# 7. Exponemos el puerto que usará Flask (y el que pondrás en Playit)
EXPOSE 5000

# 8. Comando para ejecutar con Gunicorn + Eventlet (Soporte Real para Sockets)
CMD ["gunicorn", "--worker-class", "eventlet", "-w", "1", "--bind", "0.0.0.0:5000", "index:app"]