from bs4 import BeautifulSoup

with open('./CC-B0CWGXSNGZ.html', 'r', encoding='utf-8') as file:
    content = file.read()

soup = BeautifulSoup(content, 'html.parser')

section = soup.find(id='buy-box')

if section:
    price = section.find(class_='bgp')
    print(price.get_text(strip=True))
else:
    print("No se encontró el contenedor con id='buy-box'")
