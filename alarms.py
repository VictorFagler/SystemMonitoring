alarms = []

def create_alarm(area, name, threshold):
    alarm = {
        "area": area,
        "name": name,
        "threshold": float(threshold)
    }
    alarms.append(alarm)
    print(f"Alarm skapat: {alarm}")

def get_alarms():
    return alarms

def build_alarm_menu():
    while True:
        print("\n--- Configure Alarms ---")
        print("1. CPU Usage")
        print("2. Memory Usage")
        print("3. Disk Usage")
        print("0. Back to Main Menu")

        choice = input("Choose an option: ")
        if choice == "1":
            configure_alarm("CPU")
        elif choice == "2":
            configure_alarm("Memory")
        elif choice == "3":
            configure_alarm("Disk")
        elif choice == "0":
            break
        else:
            print("Invalid choice, try again.")
def configure_alarm(area):
    print(f"\nConfiguring alarm for {area}:")
    name = input("Enter alarm name: ").strip()
    threshold = input("Enter threshold (%): ").strip()

    if not name or not threshold:
        print("Error: Both name and threshold must be filled.")
        return

    try:
        thr_value = float(threshold)
    except ValueError:
        print("Error: Threshold must be a number (e.g., 75 or 75.0).")
        return

    create_alarm(area, name, thr_value)
    print(f"Alarm created: [{area}] {name}, threshold={thr_value}%")


def show_alarms():
    alarms_list = get_alarms()

    print("\n--- Active Alarms ---")
    if not alarms_list:
        print("No alarms created yet.")
        return

    for i, alarm in enumerate(alarms_list, start=1):
        print(f"{i}. [{alarm['area']}] {alarm['name']} — threshold: {alarm['threshold']}")