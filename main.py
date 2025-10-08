from monitor import *
from logger import *
from alarms import *

def build_main_menu():
    while True:
        print("\n=== System Monitoring ===")
        print("1. Start/Stop Monitoring")
        print("2. List Active Monitoring")
        print("3. Create Alarm")
        print("4. Delete Alarm")
        print("5. Show Alarms")
        print("6. Start Monitoring Mode")
        print("0. Exit")
        
        try:
            choice = input("Choose an option: ").strip()
        except KeyboardInterrupt: # Handle Ctrl+C cleanly & Exit the menu loop
            print("\n\nExiting program...")
            break 

        if choice == "1":
            start_monitoring()

        elif choice == "2":
            list_active_monitoring()

        elif choice == "3":
            build_alarm_menu(alarm_manager)

        elif choice == "4":
            delete_alarm_menu(alarm_manager)

        elif choice == "5":
            alarms = alarm_manager.get_alarms()
            clear_screen()
            if alarms:
                print("\n--- Active Alarms ---")
                for i, alarm in enumerate(alarms, start=1):
                 print(f"{i}. [{alarm['area']}] ({alarm['threshold']}%)")
            else:
                print("\nNo alarms created yet.")

        elif choice == "6":
            start_monitoring_mode()
            
        elif choice == "0":
            print("Exiting...")
            break
        
        else:
            print("Invalid choice, try again.")

build_main_menu()