import os
import re
import sys
import time
import shutil
from bs4 import BeautifulSoup

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
    
    comments = soup.find_all(string=lambda text: isinstance(text, str) and 'saved from url' in text)
    
    for comment in comments:
        for source, regex_list in patterns.items():
            for pattern in regex_list:
                match = re.search(pattern, comment)
                if match:
                    return match.group(1), source
    
    return None, None

def clean_files(file_path, files_dir, move=True):
    if move:
        os.makedirs("pages/activos", exist_ok=True)
        # Mover archivo individual
        destino_archivo = os.path.join("pages/activos", os.path.basename(file_path))
        shutil.move(file_path, destino_archivo)
        # Mover carpeta si existe
        if os.path.exists(files_dir):
            destino_carpeta = os.path.join("pages/activos", os.path.basename(files_dir))
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

    # print("page_catcha", condiciones)
    # Loguear
    return all(condiciones)

def page_not_found(soup):
    textos = [text for text in soup.stripped_strings]
    
    condiciones = [
        any("¿Estás buscando algo?" in t for t in textos),
        any("Lo sentimos." in t for t in textos),
        any("no es una página activa" in t for t in textos),
        any("Haz clic aquí para volver" in t for t in textos)
    ]

    # print("page_not_found", condiciones)
    # Loguear
    return all(condiciones)

def item_not_available(soup):
    textos = [text for text in soup.stripped_strings]
    
    condiciones = [
        any("No disponible por el momento." in t for t in textos),
        any("No sabemos si este producto volverá a estar disponible, ni cuándo." in t for t in textos),
    ]

    # print("item_not_available", condiciones)
    # Loguear
    return all(condiciones)

def item_cannot_be_sent(soup):
    textos = [text for text in soup.stripped_strings]
    
    condiciones = [
        any("No puede enviarse este producto al punto de entrega seleccionado." in t for t in textos),
        any("Selecciona un punto de entrega diferente." in t for t in textos),
    ]

    # print("item_cannot_be_sent", condiciones)
    # Loguear
    return all(condiciones)

def get_price(soup, codigo):
    section = soup.find(id='apex_offerDisplay_desktop')

    if not section:
        section = soup.find(id='dynamic-aod-ingress-box')

    if section:
        price = section.find(class_='a-price')
        if price:
            print(f"{codigo}: {price.get_text(strip=True)}")
            return True
        else:
            print(f"{codigo}: No se encontró el precio.")
    else:
        print(f"{codigo}: No se encontró el contenedor")
    
    return False


def amazon_scraping(soup, codigo):
    if page_catcha(soup):
        # print(f"{codigo} Catcha")
        return False
    if page_not_found(soup):
        # print(f"{codigo} Not found")
        return False
    if item_not_available(soup):
        # print(f"{codigo} No Disponible")
        return False
    if item_cannot_be_sent(soup):
        # print(f"{codigo} No Se puede enviar")
        return False
    if get_price(soup, codigo):
        return False
    
    print(f"***** {codigo} NO FILTRADO *****")
    return True


def camel_scraping(soup):
    return True

def procesar_archivo_mas_antiguo():
    path = './pages'

    # Listar archivos HTML válidos
    archivos = [f for f in os.listdir(path) if f.endswith('.html')]
    if not archivos:
        print("No hay archivos HTML para procesar.")
        return

    # Ordenar por fecha de modificación (ascendente)
    archivos.sort(key=lambda f: os.path.getmtime(os.path.join(path, f)))

    # Tomar el más antiguo
    archivo = archivos[0]

    file_path = os.path.join(path, archivo)
    files_dir = os.path.join(path, f'{archivo.replace('.html', '')}_files')

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        soup = BeautifulSoup(content, 'html.parser')
        codigo, src = extract_product_info(soup)

        if codigo == None or src == None:
            print(f'ARCHIVO NO VALIDO: {archivo}')
            # Eliminar archivo y carpeta asociada
            clean_files(file_path, files_dir)
            return

        move = False
        if src == 'AZ':
            move = amazon_scraping(soup, codigo)
        if src == 'CC':
            move = camel_scraping(soup)

        # Eliminar archivo y carpeta asociada
        clean_files(file_path, files_dir, move)

    except Exception as e:
        print(f"Error procesando {archivo}: {e}")

# Loop infinito cada 60 segundos
while True:
    procesar_archivo_mas_antiguo()
    time.sleep(1)
