import os
import time
import sys
from datetime import datetime
from src.scripts.add_new_items_to_db import add_new_items_to_db
from src.lib.timer import print_now
from src.lib.cleaner import clean_old_entries
from src.scripts.generate_sku_input_files import generate_sku_batches
from src.scripts.switch_seller_id import switch_seller_id

def blockDBProcess():
    inputs_path="src/autoit/inputs"
    filename = os.path.join(inputs_path, f"DB_Blocker")
    with open(filename, 'w') as f:
        f.write('Remove this file in order to run DB update process')

def unblockDBProcess():
    inputs_path = "src/autoit/inputs"
    filename = os.path.join(inputs_path, "DB_Blocker")
    if os.path.exists(filename):
        os.remove(filename)

def start_mercadolibre_process():
    blockDBProcess()
    switch_seller_id()

    # Ejecutar carga de nuevos codigos en la base de datos
    start_time = print_now("Inicia carga de nuevos codigos")
    add_new_items_to_db()
    print_now("Finaliza carga de nuevos codigos", start_time)

    # Limpiar archivos antiguos
    clean_old_entries("logs/", 15)
    
    downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
    clean_old_entries(downloads_path, 10)

    # Crear inputs para el proceso de descarga de paginas
    generate_sku_batches()
    unblockDBProcess()
    print_now("Inicia lectura de inputs")

def monitor_input_folder(folder_path="src/autoit/inputs"):
    try:
        # Ensure folder exists
        os.makedirs(folder_path, exist_ok=True)
        
        downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
        download_files = [f for f in os.listdir(downloads_path) if f.endswith('.mhtml')]
        download_count = len(download_files)

        # Count number of files in the directory
        files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        file_count = len(files)

        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]")
        print(f"Cantidad de archivos en Download: {download_count}")
        print(f"Cantidad de archivos en '{folder_path}': {file_count}")

        if file_count == 0 and download_count < 10:     # Si es necesario, borrar manualmente el archivo src/autoit/inputs/DB_Blocker
            print_now("Finaliza lectura de inputs")
            start_mercadolibre_process()

        elif 5 < file_count <= 30:
            print_now("Reintentar en 1 hora")
            time.sleep(3600)  # 1 hour in seconds
            monitor_input_folder()

        elif file_count <= 5:
            print_now("Reintentar en 10 minutos")
            time.sleep(600)  # 10 minutes in seconds
            monitor_input_folder()

        time.sleep(30)
        

    except Exception as e:
        print(f"An error occurred: {e}")
        time.sleep(600)  # Wait before retrying in case of error
        monitor_input_folder()

if __name__ == "__main__":
    monitor_input_folder()
