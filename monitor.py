import psutil
import time
import threading
from utils import *
from alarms import *

monitoring = False
dashboard_thread = None
current_stats = {
    "cpu": 0,
    "memory_used": 0,
    "memory_total": 0,
    "memory_percent": 0,
    "disk_used": 0,
    "disk_total": 0,
    "disk_percent": 0
}

def start_monitoring():
    global monitoring, dashboard_thread
    clear_screen()
    if monitoring:
        user_input = input("\nMonitoring is already running. Do you want to stop it? Y/N\n")
        if user_input.lower() == "y":
            monitoring = False
            clear_screen()
            print("\n> Monitoring stopped.\n")
            return
        else:
            clear_screen()
            print("\n> Continuing monitoring...\n")
            return  # Do not start a new thread

    # Start monitoring if not already running
    monitoring = True
    dashboard_thread = threading.Thread(target=monitoring_loop, daemon=True)
    dashboard_thread.start()
    print()
    print("\n> Monitoring activated\n")

def monitoring_loop():
    global current_stats, monitoring
    psutil.cpu_percent(interval=None)    # Prime CPU measurement

    while monitoring:
        cpu = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage(os.path.abspath(os.sep))
        current_stats["cpu"] = cpu
        current_stats["memory_used"] = to_gb(mem.used)
        current_stats["memory_total"] = to_gb(mem.total)
        current_stats["memory_percent"] = mem.percent
        current_stats["disk_used"] = to_gb(disk.used)
        current_stats["disk_total"] = to_gb(disk.total)
        current_stats["disk_percent"] = disk.percent

def get_current_stats():
    return current_stats.copy()

def show_current_stats():  #Show stats and return to menu on Enter without stopping background monitoring
    stop_display = False

    def wait_for_enter():
        nonlocal stop_display
        input("\nPress Enter to return to menu...\n")
        stop_display = True

    input_thread = threading.Thread(target=wait_for_enter, daemon=True)
    input_thread.start()

    while not stop_display:
        stats = current_stats
        clear_screen()
        print()
        print(f"\n== Active Monitoring ==\n")
        print(f"CPU: {stats['cpu']}%")
        print(f"Memory: {stats['memory_used']} GB / {stats['memory_total']} GB ({stats['memory_percent']}%)")
        print(f"Disk: {stats['disk_used']} GB / {stats['disk_total']} GB ({stats['disk_percent']}%)")
        print("\n(Press Enter to return)\n")
        time.sleep(1)

    clear_screen()
    print("Returning to menu...\n")

def list_active_monitoring():
    if monitoring:
        print("\n> Listing active monotoring \n")
        show_current_stats()
    else:
        print("\n> No monotoring activated ")

def start_monitoring_mode():
    if monitoring:
        print("Monitoring mode started. Press Enter to return to menu.")
        stop_display = False

        def wait_for_enter():
            nonlocal stop_display
            input()  # just wait for Enter
            stop_display = True

        input_thread = threading.Thread(target=wait_for_enter, daemon=True)
        input_thread.start()

        while not stop_display:
            stats = get_current_stats() 
            clear_screen()
            print("\n== Active Monitoring ==\n")
            print(f"CPU: {stats['cpu']}%")
            print(f"Memory: {stats['memory_used']} GB / {stats['memory_total']} GB ({stats['memory_percent']}%)")
            print(f"Disk: {stats['disk_used']} GB / {stats['disk_total']} GB ({stats['disk_percent']}%)\n")

            for alarm in alarm_manager.get_alarms():
                area = alarm["area"]
                threshold = alarm["threshold"]

                if area == "CPU" and stats["cpu"] >= threshold:
                    print(f"⚠️  CPU alarm triggered! Usage: {stats['cpu']}% (threshold {threshold}%)  ⚠️")

                elif area == "RAM" and stats["memory_percent"] >= threshold:
                    print(f"⚠️  RAM alarm triggered! Usage: {stats['memory_percent']}% (threshold {threshold}%)  ⚠️")

                elif area == "Memory" and stats["disk_percent"] >= threshold:
                    print(f"⚠️  Disk alarm triggered! Usage: {stats['disk_percent']}% (threshold {threshold}%)  ⚠️")

            print("\n(Press Enter to return)\n")
            time.sleep(1)

        clear_screen()
        print("Returning to menu...\n")
    else:
        print("Monitoring not active.")