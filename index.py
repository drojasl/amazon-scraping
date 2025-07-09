import os
import time
import sys
from datetime import datetime
from src.scripts.add_new_items_to_db import add_new_items_to_db
from src.lib.timer import print_now
from src.lib.cleaner import clean_old_entries
from src.scripts.generate_sku_input_files import generate_sku_batches

def start_scraping_process():
    # Ejecutar carga de nuevos codigos en la base de datos
    start_time = print_now("Inicia carga de nuevos codigos")
    add_new_items_to_db()
    print_now("Finaliza carga de nuevos codigos", start_time)

    # Limpiar archivos antiguos
    # clean_old_entries("logs/", 15)
    # clean_old_entries("pages/", 3)

    # Crear inputs para el proceso de descarga de paginas
    generate_sku_batches()
    print_now("Inicia lectura de inputs")

def monitor_input_folder(folder_path="src/autoit/inputs"):
    try:
        # Ensure folder exists
        os.makedirs(folder_path, exist_ok=True)

        # Count number of files in the directory
        files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        file_count = len(files)

        print(f"Files in '{folder_path}': {file_count} | [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]")

        if file_count == 0:     # Podría cambiarse a 3 o 5 por proceso de DB? Evaluar
            print_now("Finaliza lectura de inputs")
            start_scraping_process()

        elif 10 < file_count <= 50:
            time.sleep(3600)  # 1 hour in seconds
            monitor_input_folder()

        elif file_count <= 10:
            time.sleep(600)  # 10 minutes in seconds
            monitor_input_folder()

        

    except Exception as e:
        print(f"An error occurred: {e}")
        time.sleep(600)  # Wait before retrying in case of error
        monitor_input_folder()

if __name__ == "__main__":
    monitor_input_folder()
