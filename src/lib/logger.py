import os
from datetime import datetime

def log(nombre_base_archivo, mensaje):
    # Asegurar que exista la carpeta 'logs'
    carpeta_logs = "logs"
    os.makedirs(carpeta_logs, exist_ok=True)

    # Obtener fecha actual para el nombre del archivo
    fecha_hoy = "" #datetime.now().strftime("%Y-%m-%d")
    nombre_archivo_con_fecha = f"{nombre_base_archivo}_{fecha_hoy}.log"

    # Ruta completa al archivo
    ruta_log = os.path.join(carpeta_logs, nombre_archivo_con_fecha)

    # Timestamp del mensaje
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linea = f"[{timestamp}] {mensaje}\n"

    # Escribir la línea en modo append
    with open(ruta_log, "a", encoding="utf-8") as f:
        f.write(linea)
