from monitor import *
from alarms import *


def build_main_menu():
    write_log("Program started")
    while True:
        print("\n=== System Monitoring ===")
        print("1. Start/Stop Monitoring")
        print("2. List Active Monitoring")
        print("3. Create Alarm")
        print("4. Show/delete Alarms")
        print("5. Start Monitoring Mode")
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
            alarm_manager.show_or_delete_alarms()

        elif choice == "5":
            start_monitoring_mode()
            
        elif choice == "0":
            print("Exiting...")
            write_log("Exit program")
            break
        
        else:
            print("Invalid choice, try again.")

build_main_menu()