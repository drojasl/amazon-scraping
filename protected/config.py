import re

def get_seller_id() -> str:
    file_path = "protected/activeSeller.py"
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"No se encontró {file_path}")

    # Extrae el valor de SELLER_ID (comillas opcionales)
    m = re.search(r'^\s*SELLER_ID\s*=\s*[\'"]?([A-Za-z0-9_-]+)[\'"]?\s*$',
                  text, re.MULTILINE)
    if not m:
        raise ValueError("No se pudo leer SELLER_ID desde activeSeller.py")

    return m.group(1)

def get_db_path() -> str:
    seller_id = get_seller_id()
    db_path = f"protected/db/mercadolibre_{seller_id}.db"
    return str(db_path)

API_URL="https://api.mercadolibre.com"
CLIENT_ID="2019099840668154"
SECRET_KEY="zZUy7A3GUwuBUpuFSErp8nawWqhskaaD"
SELLER_ID = get_seller_id()
DB_PATH = get_db_path()
