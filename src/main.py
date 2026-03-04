import pyaudio
import numpy as np
import time

# Configuraciones de PyAudio
FORMAT = pyaudio.paInt16  # Formato de audio
CHANNELS = 1               # Número de canales (1 para mono)
RATE = 44100               # Tasa de muestreo (Hz)
CHUNK = 1024               # Tamaño del buffer

# Inicializar PyAudio
p = pyaudio.PyAudio()

# Abrir el flujo de audio
stream = p.open(format=FORMAT,
                 channels=CHANNELS,
                 rate=RATE,
                 input=True,
                 frames_per_buffer=CHUNK)

print("Midiendo decibelios... Presiona Ctrl+C para detener.")

try:
    while True:
        decibelios = []
        start_time = time.time()

        # Recoger datos durante un segundo
        while time.time() - start_time < 1:
            data = stream.read(CHUNK)
            audio_data = np.frombuffer(data, dtype=np.int16)
            
            # Calcular la amplitud RMS (Root Mean Square)
            rms = np.sqrt(np.mean(np.square(audio_data)))
            print("CHUNK: ", rms)
            
            # Convertir a decibelios
            if rms > 0:
                db = 20 * np.log10(rms)
            else:
                db = -np.inf
            
            decibelios.append(db)

        # Calcular la media de decibelios
        media_db = np.mean(decibelios)
        print(f"Media de decibelios en el último segundo: {media_db:.2f} dB")

except KeyboardInterrupt:
    print("Deteniendo la medición.")

# Detener y cerrar el flujo
stream.stop_stream()
stream.close()
p.terminate()