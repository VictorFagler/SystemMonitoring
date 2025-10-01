from monitor import *
from logger import *
from alarms import *

def build_main_menu():
    while True:
        print("\n=== System Monitoring ===")
        print("1. Start/Stop Monitoring")
        print("2. List Active Monitoring")
        print("3. Create Alarm")
        print("4. Show Alarms")
        print("5. Start Monitoring Mode")
        print("0. Exit")

        choice = input("Choose an option: ")
        if choice == "1":
            start_monitoring()
        elif choice == "2":
            list_active_monitoring()
        elif choice == "3":
            build_alarm_menu()
        elif choice == "4":
            show_alarms()
        elif choice == "5":
            start_monitoring_mode()
            
        elif choice == "0":
            print("Exiting...")
            break
        else:
            print("Invalid choice, try again.")

build_main_menu()