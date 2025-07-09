import os
import time
import shutil
from datetime import datetime

def clean_old_entries(path, days=7):
    """
    Deletes files and directories older than the given number of days.
    """
    if not os.path.exists(path):
        print(f"Directorio '{path}' no existe.")
        return

    now = time.time()
    threshold_seconds = days * 86400  # days to seconds

    for entry in os.listdir(path):
        full_path = os.path.join(path, entry)

        try:
            # Get last modification time
            modified_time = os.path.getmtime(full_path)

            # Compare with current time
            if now - modified_time > threshold_seconds:
                if os.path.isfile(full_path):
                    os.remove(full_path)
                    print(f"Deleted file: {full_path}")
                elif os.path.isdir(full_path):
                    shutil.rmtree(full_path)
                    print(f"Deleted directory: {full_path}")
        except Exception as e:
            print(f"Error processing '{full_path}': {e}")
