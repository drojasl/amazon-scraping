import os
import sys
import time
import subprocess

def main():
    path = './pages'

    archivos = [f for f in os.listdir(path)]

    if not archivos:
        sys.exit()
        
    conteo_az_cc = sum(1 for archivo in archivos if archivo.startswith('AZ-') or archivo.startswith('CC-'))
    
    print(f"Archivos por procesar: {conteo_az_cc}")
    
    if conteo_az_cc == 0:
        print("EJECUTAR PROCESO DE LIMPIEZA")
        delete_pages = "delete_pages_folder.bat"
        subprocess.Popen(delete_pages)

    time.sleep(10)
    sys.exit()

if __name__ == "__main__":
    main()
