from protected.config import API_URL, CLIENT_ID, SECRET_KEY, DB_PATH, SELLER_ID
import sys
import sqlite3
import requests
from src.lib.logger import log

def get_validated_token():
    token, refresh = get_access_token()
    validate_token(token, refresh)
    token, refresh = get_access_token()
    return token


def get_access_token():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT access_token, refresh_token FROM auth")
    row = cursor.fetchone()
    if row:
        token = row[0]
        refresh = row[1]
    else:
        token = None
        refresh = None
    conn.close()

    return [token, refresh]


def refresh_access_token(refresh):
    """Refresca el token de acceso y actualiza la base de datos"""
    try:
        url = f"{API_URL}/oauth/token"
        
        payload = {
            'grant_type': 'refresh_token',
            'client_id': CLIENT_ID,
            'client_secret': SECRET_KEY,
            'refresh_token': refresh
        }
        
        headers = {
            'accept': 'application/json',
            'content-type': 'application/x-www-form-urlencoded'
        }

        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()
        
        token_data = response.json()
        
        if not all(key in token_data for key in ['access_token', 'refresh_token']):
            raise ValueError("Respuesta del API incompleta")
        
        new_access = token_data['access_token']
        new_refresh = token_data.get('refresh_token', refresh)

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE auth 
            SET access_token = ?, 
                refresh_token = ?,
                updated_at = datetime('now')
            WHERE refresh_token = ?
        """, (new_access, new_refresh, refresh))
        
        conn.commit()
        conn.close()
        print("Token actualizado correctamente")
        
    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud: {str(e)}")
        return None
    except sqlite3.Error as e:
        print(f"Error en la base de datos: {str(e)}")
        conn.rollback()
        return None
    except Exception as e:
        print(f"Error inesperado: {str(e)}")
        return None


def validate_token(token, refresh):
    url = API_URL + "/users/" + SELLER_ID + "/items/search?"

    payload = {}
    headers = {'Authorization': "Bearer " + token}
    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        if response.status_code == 401:
            error_data = response.json()
            if error_data.get('error') == 'not_found' and error_data.get('message') == 'invalid_token':
                print("Token expirado")
                refresh_access_token(refresh)

    except requests.exceptions.HTTPError as err:
        print("Authentication error")
        log("auth_error", f"Error validating token: {err}")

