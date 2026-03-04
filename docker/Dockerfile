# Usamos una imagen ligera de Python
FROM python:3.9-slim

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos el archivo de dependencias y el script
COPY bridge.py .

# Instalamos las librerías necesarias
RUN pip install --no-cache-dir paho-mqtt influxdb-client

# Comando para ejecutar el script
CMD ["python", "-u", "bridge.py"]