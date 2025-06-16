import sys
import requests
import sqlite3
from protected.config import API_URL, DB_PATH
from src.scripts.auth import get_access_token, get_validated_token
from src.lib.dolar_hoy import get_trm_banrep

def save_item_attributes(item_id, dollar):
    token = get_validated_token()

    url = API_URL + "/items/?attributes=id,price,title,permalink,seller_custom_field,seller_sku,status&ids=" + item_id

    payload = {}
    headers = {
        'Authorization': "Bearer " + token
    }
    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        data = response.json()

        if (data[0] and data[0]['body']):

            body = data[0]['body']

            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()

            sku_value = body.get('seller_custom_field') or body.get('seller_sku') or 'N/A'

            cursor.execute("""
            INSERT OR IGNORE INTO items (item_id, title, permalink, price, dollar, status, sku, created_at, updated_at) 
            VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'))
            """, (
                item_id,
                body['title'],
                body['permalink'],
                body['price'],
                dollar,
                body['status'],
                sku_value,
            ))
            conn.commit()
            print(item_id + " Added")

    except requests.exceptions.HTTPError as err:
        print("ERROR")
        print(err)
