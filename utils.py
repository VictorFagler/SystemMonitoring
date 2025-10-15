import os
from datetime import datetime

LOG_FILE = os.path.join("logs", "system.log")

def write_log(message): #"Write timestamped log message to file (no logging module)."
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{timestamp} | {message}\n")

def clear_screen(): #Clear the terminal screen for Windows, Linux, or Mac.
    os.system('cls' if os.name == 'nt' else 'clear')

def bytes_to_gb(val): #Convert bytes to gigabytes
    return round(val / (1024**3), 1)

def safe_input(prompt=""):
    try:
        return input(prompt)
    except KeyboardInterrupt:
        print("\nAborted by user.")
        write_log("Aborted by user")
        return ""