import sqlite3
from protected.config import get_db_path

def ejecutar(query, db_path=get_db_path()):
    print(f"Ejecutando en: {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Ejecutar consulta
    cursor.execute(query)
    conn.commit()
    conn.close()

def ejecutar_consulta(query, db_path=get_db_path()):
    print(f"Ejecutando en: {db_path}")
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
SET base_dollar_price = 138.48, updated_at = datetime('now')
WHERE item_id IN ('MCO1801849336')
"""
'''


query = """
SELECT 'https://articulo.mercadolibre.com.co/MCO-' || SUBSTR(item_id, 4), sku, status, base_dollar_price
FROM items
WHERE sku IN (
'B087DZFQ8B',
'B088NM3Z7S',
'B08799BRLM',
'B086M8PL8P',
'B089KPQH4V',
'B083JVB21K',
'B083KK2S98',
'B081SWQKR4',
'B085VT6F1S',
'B083B6XPVZ',
'B082SVJWD8',
'B081STKP4W',
'B083W2V3PV',
'B085M52JTP',
'B085D97MNX',
'B086YDZM3P',
'B084Z17NTD',
'B084RJRXB6',
'B083VT17V3',
'B07BB9515J',
'B079GGYQ62',
'B00004SRCS',
'B00009R9EZ',
'B0000515I6',
'B00A3ZE1SE',
'B002KINBHY',
'B001RLQNSO',
'B000GEDSPE',
'B0077UY4FI',
'B002NCTEVE',
'B002LE8PDM',
'B07CVVDMVF',
'B075MPML9D',
'B00SKU47RE',
'B00JRD13T8',
'B00JZW4DCA',
'B00AQSTAJ8',
'B000WIV45U',
'B000ALILGO',
'B019Z3P8ZY',
'B00ZC1NQBC',
'B01F6XWPOY',
'B00XBCY7X0',
'B00V05BD1O',
'B00UOTEPJE',
'B00UOTER9W',
'B00XBE8Q1W',
'B00V067A38',
'B00V063PKK',
'B00SINNRAG',
'B00NTTH35Y',
'B00MZ8B6G2',
'B00LQXHX4Q',
'B00FHU94IW',
'B00DRIL27W',
'B00DQCT33Y',
'B004R7QUSI',
'B003XB9ZSQ',
'B003HEQJZQ',
'B00205KJM2'
);
"""


'''
query = """
DELETE FROM items 
WHERE status = 'under_review'
"""
'''

'''
query = """
    ALTER TABLE items
    ADD COLUMN deleted_at TIMESTAMP NULL DEFAULT NULL
"""
'''

'''
query = """
SELECT item_id, status, sku
FROM items
WHERE base_dollar_price IS NOT NULL
"""
'''

query = """
SELECT COUNT(sku) FROM items 
WHERE sku != 'N/A' AND status != 'softDeleted'
ORDER BY updated_at ASC 
"""

ejecutar_consulta(query)
