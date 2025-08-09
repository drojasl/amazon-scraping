def switch_seller_id():
    file_path = "protected/activeSeller.py"

    # Valores posibles
    value_a = "85062679"
    value_b = "36362702"

    # Leer contenido actual
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    print(f"Contenido actual de {file_path}:\n{content}")

    new_value = value_a 
    # Buscar el valor actual
    if f'SELLER_ID = "{value_a}"' in content:
        new_value = value_b

    new_content = f'SELLER_ID = "{new_value}"\n'

    # Guardar cambios
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"✅ SELLER_ID actualizado a: {new_value}")

if __name__ == "__main__":
    switch_seller_id()