## Requerimientos del sistema

- AutoIt3
- git
  - https://github.com/drojasl/amazon-scraping
- phyton
- pip install requests
- pip install beautifulsoup4
- pip install python-dotenv

## Preparacion de ejecución

- Abrir navegador web (DEBE quedar ubicado en la esquina superior izquierda)
- Entrar a Amazon
- Verificar que tenga el ZIPCODE 33166-2623
- Guardar una pagina
  - ruta al proyecto /amazon_scraping/pages
- Verificar que el idioma sea Español
- Abrir al menos 4 o 5 pestañas

# run once a week

python -m src.scripts.add_new_items_to_db

# run once per day

python -m src.scripts.get_sku_list

# always running

python -m index
python -m src.scripts.scraping_local_page
