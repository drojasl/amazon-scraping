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

def add_codigo_retries(codigo, filename="src/autoit/inputs/CC-retries.txt"):
    try:
        with open(filename, "a", encoding="utf-8") as f:
            f.write(f"{codigo}\n")

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

def clean_files(file_path, files_dir, move=True, subdir='otros'):
    move = True
    if move:
        print(subdir, file_path)
        destino_dir = os.path.join("pages", subdir)
        os.makedirs(destino_dir, exist_ok=True)

        # Mover archivo individual si existe
        if os.path.exists(file_path) and os.path.isfile(file_path):
            destino_archivo = os.path.join(destino_dir, os.path.basename(file_path))
            shutil.move(file_path, destino_archivo)

        # Mover carpeta si existe
        if os.path.exists(files_dir) and os.path.isdir(files_dir):
            destino_carpeta = os.path.join(destino_dir, os.path.basename(files_dir))
            shutil.move(files_dir, destino_carpeta)

    else:
        os.remove(file_path)
        if os.path.exists(files_dir):
            shutil.rmtree(files_dir)

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
            # update_item(file_path, codigo, price_value, 'active')
            return True
        else:
            print(f"{codigo}: No se encontró el precio.")
    else:
        print(f"{codigo}: No se encontró el contenedor")
    
    return False


def amazon_scraping(soup, codigo, file_path, files_dir):
    if page_catcha(soup):
        log("page_catcha", f"Item {codigo} display catcha.")
        clean_files(file_path, files_dir, False, 'catcha')
        return False

    if page_not_found(soup):
        log("page_not_found", f"Item {codigo} not found.")
        clean_files(file_path, files_dir, False, 'page_not_found')
        # update_item(file_path, codigo, None, 'paused')
        return False

    if item_not_available(soup):
        log("item_not_available", f"Item {codigo} not available.")
        clean_files(file_path, files_dir, False, 'item_not_available')
        # update_item(file_path, codigo, None, 'paused')
        return False

    if item_cannot_be_sent(soup):
        log("item_cannot_be_sent", f"Item {codigo} cannot be sent.")
        clean_files(file_path, files_dir, False, 'item_cannot_be_sent')
        # update_item(file_path, codigo, None, 'paused')
        return False

    if get_price(soup, codigo, file_path):
        clean_files(file_path, files_dir, False, 'OK')
        return False

    print(f"***** {codigo} NO FILTRADO *****")
    log("unfiltered_items", f"Item {codigo} not filtered. Check manually.")

    # Add code to retry file using camelcamelcamel.com to get the price
    add_codigo_retries(codigo)

    return True


def camel_scraping(soup):
    clean_files(file_path, files_dir, True, 'invalidos')
    return False

def procesar_archivo_mas_antiguo():
    path = './pages'

    # Listar archivos HTML válidos
    archivos = [f for f in os.listdir(path) if f.endswith('.mhtml')]
    if not archivos:
        print("No hay archivos HTML para procesar.")
        time.sleep(30)
        sys.exit()

    # Ordenar por fecha de modificación (ascendente)
    archivos.sort(key=lambda f: os.path.getmtime(os.path.join(path, f)))

    # Tomar el más antiguo
    archivo = archivos[0]

    ruta_archivo = os.path.join(path, archivo)
    tiempo_modificacion = os.path.getmtime(ruta_archivo)
    tiempo_actual = time.time()

    if tiempo_actual - tiempo_modificacion <= 40:
        print(f"El archivo {archivo} fue modificado recientemente. Esperando 60 segundos para procesar...")
        time.sleep(30)
        return

    file_path = os.path.join(path, archivo)
    files_dir = os.path.join(path, f'{archivo.replace('.html', '')}_files')

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        decoded = quopri.decodestring(content).decode("utf-8", errors="ignore")
        soup = BeautifulSoup(decoded, 'html.parser')
        codigo, src = extract_product_info(soup)

        if codigo == None or src == None:
            log("invalid_files", f"Archivo no válido: {archivo}")
            # Eliminar archivo y carpeta asociada
            clean_files(file_path, files_dir, False, 'invalidos') #True
            return

        move = False
        if src == 'AZ':
            move = amazon_scraping(soup, codigo, file_path, files_dir)
        if src == 'CC':
            clean_files(file_path, files_dir, False, 'CC')  #True
            # move = camel_scraping(soup)

        # Eliminar archivo y carpeta asociada
        clean_files(file_path, files_dir, False, 'not-filtered') #True

    except Exception as e:
        print(f"Error procesando {archivo}: {e}")
        log("error_processing_files", f"Error processing file {archivo}: {e}")
        # Eliminar archivo y carpeta asociada
        clean_files(file_path, files_dir, False, 'excepciones') #True

import time
from datetime import datetime, timedelta

def main():
    start_time = datetime.now()
    max_runtime = timedelta(hours=0, minutes=58)  # Adjust the buffer as needed

    while True:
        current_time = datetime.now()
        elapsed_time = current_time - start_time

        if elapsed_time >= max_runtime:
            print(f"[{current_time}] Max runtime reached ({elapsed_time}). Exiting script.")
            break

        procesar_archivo_mas_antiguo()
        time.sleep(1)

if __name__ == "__main__":
    main()
