import sys
import os
import sqlite3
from datetime import datetime
from protected.config import DB_PATH

# Configuración
BATCH_SIZE = 300
MAX_FILES = 5
OUTPUT_DIR = "src/autoit/inputs"
OUTPUT_PREFIX = f"AZ-{datetime.now().strftime('%d-%m-%Y')}_"

# Crear directorio si no existe
os.makedirs(OUTPUT_DIR, exist_ok=True)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

for file_num in range(1, MAX_FILES + 1):
    # 1. Obtener los SKUs más antiguos
    cursor.execute("""
        SELECT id, sku FROM items 
        WHERE sku != 'N/A' 
        ORDER BY updated_at ASC 
        LIMIT ?
    """, (BATCH_SIZE,))
    
    items = cursor.fetchall()
    
    if not items:
        print(f"No hay más SKUs disponibles. Se generaron {file_num-1} archivos.")
        break
    
    # Preparar datos
    skus = [item[1] for item in items]
    ids = [item[0] for item in items]
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # 2. Crear archivo en la carpeta inputs
    filename = os.path.join(OUTPUT_DIR, f"{OUTPUT_PREFIX}{file_num}.txt")
    with open(filename, 'w') as f:
        f.write('\n'.join(skus))
    
    # 3. Actualizar los registros procesados
    cursor.executemany("""
        UPDATE items 
        SET updated_at = ?
        WHERE id = ?
    """, [(current_time, id) for id in ids])
    
    conn.commit()
    
    print(f"Archivo {filename} creado con {len(skus)} SKUs y actualizados en la BD")

conn.close()