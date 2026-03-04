import pyaudio
import numpy as np
import time
import paho.mqtt.client as mqtt

class SoundSensorMQTT:
    def __init__(self, broker="localhost", port=1883, topic="sensores/sonido/decibelios"):
        # Configuración Audio
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.CHUNK = 1024
        self.UMBRAL = -50
        
        # Configuración MQTT
        self.broker = broker
        self.port = port
        self.topic = topic
        self.client = mqtt.Client()

        # Inicializar Audio
        self.p = pyaudio.PyAudio()
        self.stream = None

    def conectar_mqtt(self):
        try:
            self.client.connect(self.broker, self.port, 60)
            print(f"✅ Conectado al broker MQTT en {self.broker}")
        except Exception as e:
            print(f"❌ Error conectando a MQTT: {e}")

    def iniciar_audio(self):
        self.stream = self.p.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK
        )
        print("🎙️ Micrófono abierto. Midiendo...")

    def medir_y_enviar(self, duracion_ventana=1):
        """Lee el audio durante X segundos, calcula la media y lo envía."""
        decibelios = []
        start_time = time.time()

        while time.time() - start_time < duracion_ventana:
            data = self.stream.read(self.CHUNK, exception_on_overflow=False)
            audio_data = np.frombuffer(data, dtype=np.int16)
            
            # Cálculo RMS y dB
            rms = np.sqrt(np.mean(np.square(audio_data.astype(np.float32))))
            if rms > 0:
                db = 20 * np.log10(rms)
                if db > self.UMBRAL:
                    decibelios.append(db)

        if decibelios:
            media_db = float(np.mean(decibelios))
            self._enviar_mqtt(media_db)
            return media_db
        return None

    def _enviar_mqtt(self, valor):
        """Método interno para publicar el dato."""
        payload = round(valor, 2)
        self.client.publish(self.topic, payload)
        print(f"📡 Publicado en MQTT: {payload} dB")

    def cerrar(self):
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        self.p.terminate()
        self.client.disconnect()
        print("🔒 Sensor apagado.")

# --- EJECUCIÓN DEL PROGRAMA ---
if __name__ == "__main__":
    # Si Docker corre en la misma PC, el broker es "localhost"
    sensor = SoundSensorMQTT(broker="localhost") 
    
    sensor.conectar_mqtt()
    sensor.iniciar_audio()

    try:
        while True:
            lectura = sensor.medir_y_enviar(duracion_ventana=1)
            if lectura is None:
                print("--- Silencio ---")
    except KeyboardInterrupt:
        sensor.cerrar()