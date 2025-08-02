## Requerimientos del sistema

- AutoIt3
- git
  - https://github.com/drojasl/amazon-scraping
- phyton
  - pip install requests
  - pip install beautifulsoup4
  - pip install python-dotenv

## Preparacion de ejecución

- Abrir navegador web (Chrome) maximizado
- Entrar a Amazon
- Verificar que tenga un ZIPCODE de USA (33166-2623)
- Verificar que el idioma sea Español

# run once per day

python -m src.scripts.add_new_items_to_db
python -m src.scripts.get_sku_list

# running every hour

python -m index
python -m src.scripts.scraping_local_page
