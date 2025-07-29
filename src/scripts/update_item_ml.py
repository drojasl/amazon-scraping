import sys
import json
import requests
import sqlite3
from protected.config import API_URL, DB_PATH
from src.scripts.auth import get_access_token, get_validated_token
from src.lib.dolar_hoy import get_trm_banrep
from src.lib.logger import log


def update_item_mercadolibre(item_id, new_price, new_status):

    token = get_validated_token()

    url = API_URL + "/items/" + item_id
    payload = json.dumps({
        "price": new_price,
        "status": new_status,
    })
    headers = {
        'Authorization': "Bearer " + token
    }
    try:
        response = requests.request("PUT", url, headers=headers, data=payload)
        response.raise_for_status()
        data = response.json()
        log("update_item_ml_success", f"Item {item_id} updated successfully. New price: {new_price}, New status: {new_status}")

    except requests.exceptions.HTTPError as err:
        print(f"Error al actualizar el item en Mercadolibre {item_id}")
        log("update_item_ml_error", f"Error updating item {item_id}: {err}")
        if err.response.status_code == 400 or err.response.status_code == 404:
            log("update_item_ml_not_found", f"Item {item_id} not found or bad request. Check manually. {new_status}")

'''
status: active, paused, closed
price: 1000
'''
def update_item(file_path, sku, current_dollar_price, new_status=''):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, item_id, base_pesos_price, base_dollar_price, initial_dollar_value, status, permalink FROM items WHERE sku = ?", (sku,))
    rows = cursor.fetchall()

    resultados = []
    if rows:
        activos = [row for row in rows if row[5] == 'active']

        if activos:
            resultados = activos
        else:
            resultados = [rows[-1]]
    else:
        print(f"Item not found in DB: sku: {sku}")
        log("Item_not_found_in_db", f"Sku {sku} not found in DB. File path: {file_path}")

    for row in resultados:
        id = row[0]
        item_id = row[1]
        initial_pesos_price = row[2]
        initial_dollar_price = row[3]
        initial_dollar_value = row[4]
        db_status = row[5]

        if initial_dollar_price is None or initial_dollar_price == 0:
            cursor.execute("""
                UPDATE items
                SET base_dollar_price = ?, updated_at = CURRENT_TIMESTAMP
                WHERE item_id = ?
            """, (current_dollar_price, item_id))
            conn.commit()

        # Logear cuando el estado es active y el new_status es paused
        if db_status == 'active' and new_status == 'paused':
            log("deactivated_codes", f"Item {sku} ({item_id}) paused.")

        if db_status == new_status and new_status == 'paused':
            return  # No action needed if status is already paused

        new_price = get_updated_price(initial_pesos_price, initial_dollar_price, initial_dollar_value, current_dollar_price)
        print(f"Item {sku} ({item_id}) new price: {new_price} COP")
        log("updated_prices", f"Item {sku} ({item_id}) new price. Base price: {initial_pesos_price} to new price: {new_price} COP")

        # update_item_mercadolibre(item_id, new_price, new_status)

        if db_status != new_status:
            cursor.execute("""
                UPDATE items
                SET status = ?, updated_at = CURRENT_TIMESTAMP
                WHERE item_id = ?
            """, (new_status, item_id))
            conn.commit()

    conn.close()


def get_updated_price(initial_pesos_price, initial_dollar_price, initial_dollar_value, current_dollar_price):
    """
    Si hay variacion del precio del producto:
    - Calcular a trm original el nuevo valor en pesos.
        Si el producto pasa de 10 a 15 dolares (Sumar 5 dolares al valor en pesos usando trm original):

    Si hay variación de la TRM del dólar:
    - Calcular el valor definitivo del producto usando el paso anterior y una regla de tres.
    """
    # Get current dollar value from TRM
    current_dollar_value = get_trm_banrep()

    print(initial_pesos_price, initial_dollar_price, initial_dollar_value, current_dollar_price, current_dollar_value)

    initial_pesos_price = float(initial_pesos_price)
    initial_dollar_price = float(initial_dollar_price)
    initial_dollar_value = float(initial_dollar_value)
    current_dollar_price = float(current_dollar_price)
    current_dollar_value = float(current_dollar_value)

    print(initial_dollar_price, initial_dollar_value, current_dollar_price, current_dollar_value, initial_pesos_price)
    # Variation of the product price

    # Calculate price variation using original TRM
    updated_pesos_price = initial_pesos_price + ((current_dollar_price - initial_dollar_price) * initial_dollar_value)

    # Variation of the TRM
    new_price_pesos = (current_dollar_value * updated_pesos_price) / initial_dollar_value
    print(f"new_pesos_price: {new_price_pesos}")

    # Calculate minimum price value
    min_pesos_price = current_dollar_price * current_dollar_value * 1.5
    print(f"Minimum pesos price: {min_pesos_price}")

    new_price = round(max(new_price_pesos, min_pesos_price), -2) # redondear a múltiplos de 100

    log("updated_prices_internal", f"De: {initial_pesos_price} A: {new_price}, [new_price_pesos: {new_price_pesos}, min_pesos_price: {min_pesos_price}] final_new_price: {new_price}, initial_dollar_price: {initial_dollar_price}, current_dollar_price: {current_dollar_price}], initial_dollar_value: {initial_dollar_value}, current_dollar_value: {current_dollar_value}")

    return new_price

# update_item('xxx', 'B002NSMERY', 130, 'active') # B002NSMERY, B07RNNMZW3, B00000J48J, B0D1FTH57Y, B0DNFSH3Y9
