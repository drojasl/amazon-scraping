import time
import requests
import sqlite3
from protected.config import API_URL, SELLER_ID, DB_PATH
from src.scripts.auth import get_validated_token
from src.lib.dolar_hoy import get_trm_banrep
from src.scripts.save_item import save_item_attributes
from src.scripts.validate_item_in_DB import is_item_in_DB
from src.lib.logger import log

def get_headers():
    token = get_validated_token()
    return {'Authorization': f"Bearer {token}"}

def add_new_items_to_db():
    start_time = time.time()
    scroll_id = None
    page = 1
    dollar_rate = get_trm_banrep()
    base_url = f"{API_URL}/users/{SELLER_ID}/items/search?search_type=scan"
    more_items = True
    headers = get_headers()

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        print(f"Page: {page}")
        while more_items:
            time.sleep(1)  # avoid hitting API rate limits

            # Refresh headers every 100 pages
            if page % 100 == 0:
                print(f"Page: {page}")
                headers = get_headers()

            url = f"{base_url}&scroll_id={scroll_id}" if scroll_id else base_url
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()

            results = data.get('results', [])
            scroll_id = data.get('scroll_id')

            if not results:
                print(f"Total pages processed: {page}")
                more_items = False
                continue

            for item_id in results:
                try:
                    in_db = is_item_in_DB(cursor, item_id)
                    if in_db != 1:
                        save_item_attributes(cursor, conn, in_db, item_id, dollar_rate)
                except Exception as item_error:
                    log("add_new_items_to_db", f"Error processing item {item_id}: {item_error}")

            page += 1

    except requests.exceptions.RequestException as req_err:
        log("add_new_items_to_db", f"API request failed: {req_err}")
        print(f"❌ API Request Error: {req_err}")

    except Exception as general_err:
        log("add_new_items_to_db", f"Unexpected error: {general_err}")
        print(f"❌ Unexpected Error: {general_err}")

    finally:
        try:
            conn.close()
        except:
            pass
        duration = time.time() - start_time
        minutes = int(duration // 60)
        seconds = int(duration % 60)
        print(f"⏱️ Total duration: {minutes} minutes and {seconds} seconds")

if __name__ == "__main__":
    add_new_items_to_db()