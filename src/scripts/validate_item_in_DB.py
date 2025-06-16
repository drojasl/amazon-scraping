import sys
import requests
import sqlite3
from protected.config import API_URL, DB_PATH
from src.scripts.auth import get_access_token, get_validated_token
from src.lib.dolar_hoy import get_trm_banrep

def is_item_in_DB(item_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT sku FROM items WHERE item_id=?", (item_id,))
    row = cursor.fetchone()

    if row and row[0]:
        print(item_id + " Already on DB")
        return True

    return False