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
            return 

    # Start monitoring if not already running
    monitoring = True
    dashboard_thread = threading.Thread(target=monitoring_loop, daemon=True).start()
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

        current_stats.update({
            "cpu": cpu,
            "memory_used": bytes_to_gb(mem.used),
            "memory_total": bytes_to_gb(mem.total),
            "memory_percent": mem.percent,
            "disk_used": bytes_to_gb(disk.used),
            "disk_total": bytes_to_gb(disk.total),
            "disk_percent": disk.percent
        })

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


last_triggered = {"CPU": None, "Memory": None, "Disk": None}

def check_for_trigger_alarms(stats):
    alarms_dict = alarm_manager.get_alarms()
    triggered_to_show = []  # display in terminal

    for area, alarms in alarms_dict.items():
        if not alarms:
            continue

        current_value = {
            "CPU": stats["cpu"],
            "Memory": stats["memory_percent"],
            "Disk": stats["disk_percent"]
        }[area]

        # Find highest threshold <= current usage
        thresholds = sorted([alarm["threshold"] for alarm in alarms])
        highest_trigger = None
        for t in thresholds:
            if current_value >= t:
                highest_trigger = t
            else:
                break

        if highest_trigger is not None:
            triggered_to_show.append((area, current_value, highest_trigger))
            

            # Only log when crossing threshold
            if last_triggered[area] != highest_trigger:
                write_log(f"{area} alarm ({highest_trigger} %) triggered: {current_value} %")
                last_triggered[area] = highest_trigger
                threading.Thread(target=play_alarm_sound, daemon=True).start()

        else:
            last_triggered[area] = None

    # Display all triggered alarms in terminal
    for area, value, threshold in triggered_to_show:
        print(f"⚠️ {area} alarm triggered! Usage: {value}% (threshold {threshold}%) ⚠️")
        

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

            check_for_trigger_alarms(stats)

            print("\n(Press Enter to return)\n")
            time.sleep(1)

        clear_screen()
        print("Returning to menu...\n")

    else:
        clear_screen()
        print()
        print("\nMonitoring not active. Press 1 to activate.")