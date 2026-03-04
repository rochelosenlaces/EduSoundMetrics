# Esto forzará a Docker a construir la imagen de tu script de Python
    docker-compose up -d --build


¿Cómo ver si el Bridge está funcionando?
Si quieres ver los print("Guardado...") que pusimos en el código, usa este comando:
    docker logs -f mqtt_bridge