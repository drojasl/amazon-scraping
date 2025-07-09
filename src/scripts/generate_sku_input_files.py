import os
import sqlite3
from datetime import datetime
from protected.config import DB_PATH

def generate_sku_batches(batch_size=100, output_dir="src/autoit/inputs"):
    output_prefix = f"AZ-{datetime.now().strftime('%d-%m-%Y')}"

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Connect to database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Fetch all valid SKUs
    cursor.execute("""
        SELECT sku FROM items 
        WHERE sku != 'N/A'
        ORDER BY updated_at ASC 
    """)
    all_items = [row[0] for row in cursor.fetchall()]

    total_items = len(all_items)
    file_counter = 1

    for i in range(0, total_items, batch_size):
        batch = all_items[i:i + batch_size]

        filename = os.path.join(output_dir, f"{output_prefix}_{file_counter}.txt")
        with open(filename, 'w') as f:
            f.write('\n'.join(batch))

        print(f"File {filename} created with {len(batch)} SKUs.")
        file_counter += 1

    print(f"✅ {file_counter - 1} files generated in total.")
    conn.close()

if __name__ == "__main__":
    generate_sku_batches()
