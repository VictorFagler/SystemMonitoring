import os

def clear_screen(): #Clear the terminal screen for Windows, Linux, or Mac.
    os.system('cls' if os.name == 'nt' else 'clear')

def to_gb(val): #Convert bytes to gigabytes
    return round(val / (1024**3), 1)