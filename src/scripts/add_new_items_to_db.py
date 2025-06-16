import sys
import time
import requests
from  protected.config import API_URL, SELLER_ID
from src.scripts.auth import get_access_token, get_validated_token
from src.lib.dolar_hoy import get_trm_banrep
from src.scripts.save_item import save_item_attributes
from src.scripts.validate_item_in_DB import is_item_in_DB

start_time = time.time()

token = get_validated_token()
dollar = get_trm_banrep()

base_url = f"{API_URL}/users/{SELLER_ID}/items/search?search_type=scan"
scroll_id = None

headers = {
    'Authorization': f"Bearer {token}"
}

try:
    page = 1
    while True:
        # Armar URL con scroll_id si existe
        if scroll_id:
            print("Scroll_id: "+ scroll_id)
            url = f"{base_url}&scroll_id={scroll_id}"
        else:
            url = base_url

        print("Page: " + str(page))
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        results = data.get('results', [])
        scroll_id = data.get('scroll_id')

        if not results:
            break  # Ya no hay más productos

        for item_id in results:
            if not is_item_in_DB(item_id):
                save_item_attributes(item_id, dollar)

        page += 1
        time.sleep(1)

    print("✅ Todos los ítems procesados.")
    duration = time.time() - start_time
    minutes = int(duration // 60)
    seconds = int(duration % 60)
    print(f"⏱️ Duración total: {minutes} minutos y {seconds} segundos")

except requests.exceptions.RequestException as err:
    print("❌ ERROR")
    print(err)

