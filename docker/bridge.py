import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import json

# --- Configuración de InfluxDB (Usa los datos de tu .env) ---
token = "mi_token_super_secreto"
org = "mi_organizacion"
bucket = "sensores"
url = "http://influxdb:8086"

client_influx = InfluxDBClient(url=url, token=token, org=org)
write_api = client_influx.write_api(write_options=SYNCHRONOUS)

# --- Configuración MQTT ---
MQTT_BROKER = "mosquitto"
MQTT_PORT = 1883
MQTT_TOPIC = "sensores/sonido/decibelios" # Ejemplo: sensores/temperatura/datos

def on_connect(client, userdata, flags, rc):
    print(f"Conectado a MQTT con código: {rc}")
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    try:
        # Decodificar el mensaje (asumiendo que envías un número o JSON)
        payload = msg.payload.decode("utf-8")
        valor = float(payload) 
        
        # Extraer el tipo de sensor del tópico (p.ej. "temperatura")
        sensor_type = msg.topic.split("/")[1]

        # Crear el punto para InfluxDB
        point = Point("lectura_sensores") \
            .tag("dispositivo", sensor_type) \
            .field("valor", valor)
        
        write_api.write(bucket=bucket, org=org, record=point)
        print(f"Guardado: {sensor_type} -> {valor}")

    except Exception as e:
        print(f"Error procesando mensaje: {e}")

# Inicializar Cliente MQTT
client_mqtt = mqtt.Client()
client_mqtt.on_connect = on_connect
client_mqtt.on_message = on_message

client_mqtt.connect(MQTT_BROKER, MQTT_PORT, 60)
client_mqtt.loop_forever()