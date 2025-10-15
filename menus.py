from alarms import *
from monitor import *
from utils import *

def build_main_menu():
    while True:
        print("\n=== System Monitoring ===")
        print("1. Start/Stop Monitoring")
        print("2. List Active Monitoring")
        print("3. Create Alarm")
        print("4. Show/Delete Alarms")
        print("5. Start Monitoring Mode")
        print("0. Exit")
      
        choice = safe_input("Choose an option: ").strip()

        match choice:
            case "1":
                start_monitoring()
            case "2":
                list_active_monitoring()
            case "3":
                build_alarm_menu()
            case "4":
                alarm_manager.show_and_delete_alarms()
            case "5":
                start_monitoring_mode()
            case "0":
                print("Exiting...")
                write_log("Program exited by user")
                break
            case _:
                clear_screen()
                print("\n Invalid choice, try again.")

def build_alarm_menu():
    clear_screen()
    area = None
    while True:
        print("\n=== Configure Alarms ===")
        print("1. CPU")
        print("2. Memory")
        print("3. Disk")
        print("\nPress Enter to return")
        choice = safe_input("\nChoose alarm option 1-3: ").strip()

        match choice:
            case "1":
                area = "CPU"
            case "2":
                area = "Memory"
            case "3":
                area = "Disk"
            case "":
                clear_screen()
                return
            case _:
                clear_screen()
                print("\nInvalid choice, try again.\n")
                continue
        break

    while True:
        threshold_input = safe_input(f"Enter threshold for {area} (%): ").strip()
        try:
            threshold = int(threshold_input)
        except ValueError:
            print("Error: Threshold must be a number")
            continue

        if threshold < 1 or threshold > 100:
            print("Error: Threshold must be between 1 and 100")
            continue
        break

    # Create and save the alarm
    alarm = alarm_manager.create_alarm(area, threshold)
    clear_screen()
    print(f"\n✅ Alarm created: [{alarm['area']}] ({alarm['threshold']}%)")
