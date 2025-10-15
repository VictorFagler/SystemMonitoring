import psutil
import time
import threading
from utils import *
from alarms import *

# === Global state ===
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


# === Core monitoring functions ===
def start_monitoring():
    global monitoring, dashboard_thread
    clear_screen()
    if monitoring:
        user_input = safe_input("\nMonitoring is already running. Do you want to stop it? Y/N\n")
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
    write_log("Monitoring started.")
    print()
    print("\n> Monitoring activated\n")

def monitoring_loop(): #Continuously collect system statistics while monitoring is active.
    global current_stats, monitoring
    psutil.cpu_percent(interval=None)    # Prime CPU measurement

    while monitoring:
        cpu = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage(os.path.abspath(os.sep))

        current_stats["cpu"] = cpu
        current_stats["memory_used"] = bytes_to_gb(mem.used)
        current_stats["memory_total"] = bytes_to_gb(mem.total)
        current_stats["memory_percent"] = mem.percent
        current_stats["disk_used"] = bytes_to_gb(disk.used)
        current_stats["disk_total"] = bytes_to_gb(disk.total)
        current_stats["disk_percent"] = disk.percent


def get_current_stats():
    return current_stats.copy()

def print_stats(stats):
    print(f"\n== Active Monitoring ==\n")
    print(f"CPU: {stats['cpu']}%")
    print(f"Memory: {stats['memory_used']} GB / {stats['memory_total']} GB ({stats['memory_percent']}%)")
    print(f"Disk: {stats['disk_used']} GB / {stats['disk_total']} GB ({stats['disk_percent']}%)\n")

def show_current_stats():  #Show stats and return to menu on Enter without stopping background monitoring
    stop_display = False

    def enterkey_to_break():
        nonlocal stop_display
        safe_input("")
        stop_display = True

    threading.Thread(target=enterkey_to_break, daemon=True).start()

    while not stop_display:
        clear_screen()
        print_stats(current_stats)
        print("\n(Press Enter to return)\n")
        time.sleep(1)

    clear_screen()
    print("Returning to menu...\n")

def list_active_monitoring():
    if monitoring:
        print("\n> Listing active monotoring \n")
        show_current_stats()
    else:
        clear_screen()
        print("\n> No monitoring active")

def check_for_trigger_alarms(stats):
    for alarm in alarm_manager.get_alarms():
            area = alarm["area"]
            threshold = alarm["threshold"]

            if area == "CPU" and stats["cpu"] >= threshold:
                print(f"⚠️  CPU alarm triggered! Usage: {stats['cpu']}% (threshold {threshold}%)  ⚠️")
                write_log(f"CPU alarm triggered: {stats['cpu']}% >= {threshold}%")

            elif area == "Memory" and stats["memory_percent"] >= threshold:
                print(f"⚠️  Memory alarm triggered! Usage: {stats['memory_percent']}% (threshold {threshold}%)  ⚠️")
                write_log(f"Memory alarm triggered: {stats['memory_percent']}% >= {threshold}%")

            elif area == "Disk" and stats["disk_percent"] >= threshold:
                print(f"⚠️  Disk alarm triggered! Usage: {stats['disk_percent']}% (threshold {threshold}%)  ⚠️")
                write_log(f"Disk alarm triggered: {stats['disk_percent']}% >= {threshold}%")

def start_monitoring_mode():
    if monitoring:
        write_log(f"Monitoring Mode Activated")
        print("Monitoring mode started. Press Enter to return to menu.")
        stop_display = False

        def enterkey_to_break():
            nonlocal stop_display
            safe_input()  # just wait for Enter
            stop_display = True

        threading.Thread(target=enterkey_to_break, daemon=True).start()

        while not stop_display:
            stats = get_current_stats()
            clear_screen()
            print_stats(stats)

            # --- Check alarms ---
            check_for_trigger_alarms(stats)

            print("\n(Press Enter to return)\n")
            time.sleep(1)

        clear_screen()
        print("Returning to menu...\n")

    else:
        clear_screen()
        print()
        print("\nMonitoring not active. Press 1 to activate.")