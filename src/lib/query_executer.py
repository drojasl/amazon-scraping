import sqlite3
from protected.config import DB_PATH

def ejecutar(query, db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Ejecutar consulta
    cursor.execute(query)
    conn.commit()
    conn.close()

def ejecutar_consulta(query, db_path=DB_PATH):

    try:
        # Conexión a la base de datos
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Ejecutar consulta
        cursor.execute(query)
        resultados = cursor.fetchall()

        # Obtener nombres de columnas
        columnas = [descripcion[0] for descripcion in cursor.description]

        # Imprimir encabezado
        print(" | ".join(columnas))
        print("-" * (len(" | ".join(columnas)) + 5))

        # Imprimir filas
        for fila in resultados:
            print(" | ".join(str(campo) for campo in fila))

        conn.close()
        print("---------")
        print(db_path)
        print(f"\nTotal de filas: {len(resultados)}")

    except sqlite3.Error as e:
        print("Error al ejecutar la consulta:", e)

query = """
SELECT item_id, status, sku
FROM items
WHERE sku <> 'N/A' AND sku IN (
    SELECT sku
    FROM items
    GROUP BY sku
    HAVING COUNT(*) > 1
)
ORDER BY sku;
"""

'''
query = """
SELECT item_id, status, sku
FROM items
WHERE sku == 'N/A'
"""
'''

'''
query = """
DELETE FROM items
WHERE item_id = 'MCO2693059922e'
"""
'''

'''
query = """
UPDATE items
SET base_dollar_price = NULL, updated_at = datetime('now')
WHERE item_id IN ('MCO2896566652', 'MCO1447078233')
"""
''''

ejecutar(query, 'protected/db/mercadolibre.db')
