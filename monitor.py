import psutil
import os


def to_gb(val):
    return round(val / (1024**3), 1)


# Funktion för CPU-användning
def get_cpu_usage():
    return round(psutil.cpu_percent(interval=0), 1)  # procent CPU-användning

# Funktion för minne
def get_memory_usage():
    mem = psutil.virtual_memory()
    used_gb = to_gb(mem.used)
    total_gb = to_gb(mem.total)
    percent = round(mem.percent, 1)
    return used_gb, total_gb, percent

# Funktion för disk
def get_disk_usage():
    root_path = os.path.abspath(os.sep)  # / på Linux, C:\ på Windows
    disk = psutil.disk_usage(root_path)
    used_gb = to_gb(disk.used)
    total_gb = to_gb(disk.total)
    percent = round(disk.percent, 1)
    return used_gb, total_gb, percent

# Start monitoring: skriver ut systemdata
def start_monitoring():
    cpu = get_cpu_usage()
    mem_used, mem_total, mem_percent = get_memory_usage()
    disk_used, disk_total, disk_percent = get_disk_usage()
    return cpu, mem_used, mem_total, mem_percent, disk_used, disk_total, disk_percent

def list_active_monitoring():
    print("List active alarms started...")

def start_monitoring_mode():
    print("Start monitoring mode")