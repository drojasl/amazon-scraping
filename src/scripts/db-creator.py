import sqlite3
from protected.config import DB_PATH

# 1. Conectar a la base de datos (se crea si no existe)
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# 2. Crear una tabla (si no existe)
cursor.execute("""
CREATE TABLE IF NOT EXISTS auth (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    access_token TEXT NOT NULL,
    refresh_token TEXT NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# 3. Insertar datos de ejemplo
cursor.execute("INSERT INTO auth (access_token, refresh_token) VALUES ('APP_USR-2019099840668154-051917-5181d1bd1741f055ae3faef289e1a605-85062679', 'TG-682b9e9c45d9d000018ab8f8-85062679')")

# 4. Guardar cambios
conn.commit()

# 5. Consultar tareas
cursor.execute("SELECT id, access_token, refresh_token FROM auth")
for row in cursor.fetchall():
    print(f"{row[0]}: {row[1]} : {row[2]}")

cursor.execute("""
CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id TEXT NOT NULL,
    title TEXT NOT NULL,
    permalink TEXT NOT NULL,
    base_pesos_price TEXT NOT NULL,
    base_dollar_price TEXT NULL,
    initial_dollar_value TEXT NOT NULL,
    status TEXT NOT NULL,
    sku TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_item_id ON items (item_id)")
conn.commit()

# 3. Insertar datos de ejemplo
'''
cursor.execute("""
INSERT INTO items (item_id, title, permalink, base_pesos_price, initial_dollar_value, status, sku, created_at, updated_at) 
VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'))
""", (
    'MCO462494879',
    'Lampara Colgar Intage Thick Hemp Industrial Ceiling Light',
    'https://internal-shop.mercadoshops.com.co/MCO-462494879-lampara-colgar-intage-thick-hemp-industrial-ceiling-light-_JM',
    '164900',
    '4000',
    'active',
    'B01N3OTFJF'
))
#conn.commit()

cursor.execute("SELECT id, item_id, title, permalink, base_pesos_price, initial_dollar_value, status, sku, created_at, updated_at FROM items")
for row in cursor.fetchall():
    print(f"{row[0]}: {row[1]}: {row[2]}: {row[3]}: {row[4]}: {row[5]}: {row[6]}: {row[7]}: {row[8]}: {row[9]}")
'''
# 6. Cerrar conexión
conn.close()