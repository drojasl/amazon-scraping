import sys
import requests
import sqlite3
from protected.config import API_URL, DB_PATH
from src.scripts.auth import get_access_token, get_validated_token

def get_seller_sku_attribute(attributes):
    if not attributes:
        return 'N/A'
    for attr in attributes:
        if attr.get("id") == "SELLER_SKU":
            return attr.get("value_name")
    return 'N/A'

def save_item_attributes(cursor, conn, in_db, item_id, dollar):
    token = get_validated_token()

    url = API_URL + "/items/?attributes=id,price,title,permalink,seller_custom_field,seller_sku,status,attributes&ids=" + item_id

    payload = {}
    headers = {
        'Authorization': "Bearer " + token
    }
    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        data = response.json()

        if (data[0] and data[0]['body']):

            body = data[0]['body']

            title = body.get('title', 'No Title Provided')
            link = body.get('permalink', 'No Link Provided')
            price = body.get('price', 0)
            status = body.get('status', 'unknown')
            sku_value = body.get('seller_custom_field') or body.get('seller_sku') or get_seller_sku_attribute(body.get('attributes'))

            if in_db == -1:
                if sku_value != 'N/A':
                    cursor.execute("""
                        UPDATE items
                        SET sku = ?, updated_at = datetime('now')
                        WHERE item_id = ?
                    """, (
                        sku_value,
                        item_id
                    ))
                    conn.commit()
                    print(item_id + " Updated SKU for: " + item_id)

                return

            cursor.execute("""
            INSERT INTO items (item_id, title, permalink, base_pesos_price, initial_dollar_value, status, sku, created_at, updated_at) 
            VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'))
            """, (
                item_id,
                title,
                link,
                price,
                dollar,
                status,
                sku_value,
            ))
            conn.commit()
            print(item_id + " Added")

    except requests.exceptions.HTTPError as err:
        print("Error al guardar el item:")
        log("save_item_error", f"Error saving item {item_id}: {err}")

# save_item_attributes('MCO540277566', 4000)