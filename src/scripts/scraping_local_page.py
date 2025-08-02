import os
import re
import sys
import time
import quopri
from datetime import datetime, timedelta
import shutil
from bs4 import BeautifulSoup
from src.scripts.update_item_ml import update_item
from src.lib.logger import log

def get_line_count(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return sum(1 for line in f)
    except FileNotFoundError:
        return 0
    except Exception as e:
        print(f"Error al contar líneas en el archivo {filename}: {e}")
        return -1

def add_codigo_retries(codigo, base_path="src/autoit/inputs/", max_lines=10):
    if not os.path.exists(base_path):
        os.makedirs(base_path)

    archivos = os.listdir(base_path)
    count = len([archivo for archivo in archivos if archivo.startswith('CC-')])
    i = count -1 if count else 0
    
    name = f"CC-retries-{i}.txt"
    filename = os.path.join(base_path, name)
    
    if os.path.exists(filename):
        line_count = get_line_count(filename)

        if line_count >= max_lines:
            i+=1
            name = f"CC-retries-{i}.txt"

    filename = os.path.join(base_path, name)
    try:
        with open(filename, "a", encoding="utf-8") as f:
            f.write(f"{codigo}\n")
            print(f"Código '{codigo}' agregado a '{filename}'")

    except Exception as e:
        print(f"Error al escribir en el archivo {filename}: {e}")

def extract_product_info(soup):
    # Diccionario de patrones (origen: patrón)    
    patterns = {
        'AZ': [
            r'amazon\.com/dp/([A-Z0-9]{10})',
            r'amazon\.com/[^/]+/dp/([A-Z0-9]{10})',
            r'amazon\.com/gp/product/([A-Z0-9]{10})'
        ],
        'CC': [
            r'camelcamelcamel\.com/product/([A-Z0-9]{10})',
            r'camelcamelcamel\.com/[^/]+/product/([A-Z0-9]{10})'
        ]
    }

    # Buscar en todo el contenido del archivo como texto plano
    html_text = str(soup)

    # Solo analizar las primeras líneas (más rápido)
    first_lines = "\n".join(html_text.splitlines()[:30])

    for source, regex_list in patterns.items():
        for pattern in regex_list:
            match = re.search(pattern, first_lines)
            if match:
                return match.group(1), source

    return None, None

def extract_price(valor_str):
    if not valor_str:
        return None
    # Buscar números con punto decimal usando regex
    match = re.search(r'[\d.,]+', valor_str)
    if match:
        numero = match.group(0).replace(',', '')  # elimina comas tipo 1,234.56
        try:
            return float(numero)
        except ValueError:
            return None
    return None

def clean_files(file_path, move=True, subdir='otros'):
    print(file_path)
    print()
    print(move)
    print()
    print(subdir)
    move=True
    if move:
        print(subdir, file_path)
        destino_dir = os.path.join("pages", subdir)
        os.makedirs(destino_dir, exist_ok=True)

        # Mover archivo individual si existe
        if os.path.exists(file_path) and os.path.isfile(file_path):
            destino_archivo = os.path.join(destino_dir, os.path.basename(file_path))
            try:
                shutil.move(file_path, destino_archivo)
            except Exception as e:
                log("error_processing_files", f"Error 2 processing file {file_path}: {e}")
                print(f"ERROR: No se pudo mover el archivo {file_path}. Error: {e}")
    else:
        try:
            os.remove(file_path)
        except Exception as e:
            log("error_processing_files", f"Error 3 processing file {file_path}: {e}")
            print(f"ERROR: No se pudo eliminar el archivo {file_path}. Error: {e}")

def page_catcha(soup):
    textos = [text for text in soup.stripped_strings]
    
    condiciones = [
        any("Enter the characters you see below" in t for t in textos),
        any("Sorry, we just need to make sure you're not a robot" in t for t in textos),
        any("Type the characters you see in this image:" in t for t in textos),
    ]
    return all(condiciones)

def page_not_found(soup):
    textos = [text for text in soup.stripped_strings]
    
    condiciones = [
        any("¿Estás buscando algo?" in t for t in textos),
        any("Lo sentimos." in t for t in textos),
        any("no es una página activa" in t for t in textos),
        any("Haz clic aquí para volver" in t for t in textos)
    ]
    return all(condiciones)

def item_not_available(soup):
    textos = [text for text in soup.stripped_strings]
    
    condiciones = [
        any("No disponible por el momento." in t for t in textos),
        any("No sabemos si este producto volverá a estar disponible, ni cuándo." in t for t in textos),
    ]
    return all(condiciones)

def item_cannot_be_sent(soup):
    textos = [text for text in soup.stripped_strings]
    
    condiciones = [
        any("No puede enviarse este producto al punto de entrega seleccionado." in t for t in textos),
        any("Selecciona un punto de entrega diferente." in t for t in textos),
    ]
    return all(condiciones)

def get_price(soup, codigo, file_path):
    section = soup.find(id='corePriceDisplay_desktop_feature_div')

    if not section:
        section = soup.find(id='corePrice_desktop')

    if section:
        price = section.find(class_='a-price')
        if price:
            price_value = extract_price(price.get_text(strip=True))
            log("price_extracted", f"Item {codigo} price extracted: {price_value}")
            print(f"{codigo}: Precio encontrado: {price_value}")
            update_item(file_path, codigo, price_value, 'active')
            return True
        else:
            print(f"{codigo}: No se encontró el precio.")
    else:
        print(f"{codigo}: No se encontró el contenedor")
    
    return False

def get_price_cc(soup, codigo, file_path):
    section = soup.find(id='buy-box')

    if section:
        price = section.find(class_='bgp')
        if price:
            price_value = extract_price(price.get_text(strip=True))
            if price_value != None:                
                log("price_extracted", f"Item {codigo} price extracted: {price_value}")
                print(f"{codigo}: Precio encontrado: {price_value}")
                update_item(file_path, codigo, price_value, 'active')
                return True
            else:
                print(f"{codigo}: No se encontró el precio.")
        else:
            print(f"{codigo}: No se encontró el precio.")
    else:
        print(f"{codigo}: No se encontró el contenedor")
    
    return False

def amazon_scraping(soup, codigo, file_path):
    if page_catcha(soup):
        log("page_catcha", f"Item {codigo} display catcha.")
        return [True, 'catcha']

    if page_not_found(soup):
        log("page_not_found", f"Item {codigo} not found.")
        update_item(file_path, codigo, None, 'softDeleted')
        return [True, 'page_not_found']

    if item_not_available(soup):
        log("item_not_available", f"Item {codigo} not available.")
        update_item(file_path, codigo, None, 'paused')
        return [True, 'item_not_available']

    if item_cannot_be_sent(soup):
        log("item_cannot_be_sent", f"Item {codigo} cannot be sent.")
        update_item(file_path, codigo, None, 'paused')
        return [True, 'item_cannot_be_sent']

    if get_price(soup, codigo, file_path):
        return [True, 'OK']

    print(f"***** {codigo} NO FILTRADO *****")
    log("unfiltered_items", f"Item {codigo} not filtered. Check manually.")

    # Add code to retry file using camelcamelcamel.com to get the price
    add_codigo_retries(codigo)

    return [True, 'unfiltered_items']


def camel_scraping(soup, codigo, file_path):
    price_found = get_price_cc(soup, codigo, file_path)
    return [True, 'cc-ok' if price_found else 'cc-invalid']

def procesar_archivo(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        decoded = quopri.decodestring(content).decode("utf-8", errors="ignore")
        soup = BeautifulSoup(decoded, 'html.parser')
        codigo, src = extract_product_info(soup)

        if codigo == None or src == None:
            log("invalid_files", f"Archivo no válido: {file_path}")
            # Eliminar archivo
            clean_files(file_path, False, 'invalid') #True
            return

        move = False
        if src == 'AZ':
            move, subdir = amazon_scraping(soup, codigo, file_path)
        if src == 'CC':
            move, subdir = camel_scraping(soup, codigo, file_path)

        # Eliminar archivo
        clean_files(file_path, move, subdir)

    except Exception as e:
        print(f"Error procesando {file_path}: {e}")
        log("error_processing_files", f"Error processing file {file_path}: {e}")
        time.sleep(3)
        # Eliminar archivo
        clean_files(file_path, True, 'excepciones')

import time
from datetime import datetime, timedelta

def main():
    print("Iniciando scraping.")
    start_time = datetime.now()
    minute_threshold = 58 # Min to interrup execution
    path = os.path.join(os.path.expanduser("~"), "Downloads")
    os.makedirs(path, exist_ok=True)

    while datetime.now().minute < minute_threshold:
        # Listar archivos HTML válidos
        archivos = [f for f in os.listdir(path) if f.endswith('.mhtml')]

        if not archivos:
            print("No hay archivos HTML para procesar.")
            time.sleep(30)
            sys.exit()

        for archivo in archivos:
            if datetime.now().minute >= minute_threshold:
                break

            file_path = os.path.join(path, archivo)
            print()
            print(f"*** {archivo} ***")
            print()
            procesar_archivo(file_path)
            time.sleep(1)

        time.sleep(1)
    
    log("exit_scraping", f"Max runtime reached ({elapsed_time}). Exiting script.")
    print(f"[{current_time}] Max runtime reached ({elapsed_time}). Exiting script.")
    time.sleep(10)

if __name__ == "__main__":
    main()
