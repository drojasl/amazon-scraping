import sys
from protected.config import API_URL
from src.scripts.auth import get_access_token, get_validated_token

def is_item_in_DB(cursor, item_id):
    cursor.execute("SELECT sku FROM items WHERE item_id=?", (item_id,))
    row = cursor.fetchone()

    if row and row[0]:
        if row and row[0] == 'N/A':
            return -1   # -1 to update SKU
        return 1        # 1 if item is in DB with SKU

    return 0            # Not in DB at all
