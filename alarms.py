class AlarmManager:
    def __init__(self):
        self.alarms = []

    def create_alarm(self, area, threshold):
        alarm = {
            "area": area,
            "threshold": float(threshold)
        }
        self.alarms.append(alarm)
        return alarm

    def get_alarms(self):
        return self.alarms
    
alarm_manager = AlarmManager() # Create shared instance

def build_alarm_menu(alarm_manager):
    print("\n=== Configure Alarms ===")
    while True:
        print("1. CPU")
        print("2. RAM")
        print("3. Memory")
        choice = input("Choose 1-3: ").strip()

        if choice == "1":
            area = "CPU"
            break
        elif choice == "2":
            area = "RAM"
            break
        elif choice == "3":
            area = "Memory"
            break
        else:
            print("\nInvalid choice, try again.\n")

    while True:
        threshold_input = input(f"Enter threshold for {area} (%): ").strip()
        try:
            threshold = float(threshold_input)
        except ValueError:
            print("Error: Threshold must be a number")
            continue

        if threshold < 1 or threshold > 100:
            print("Error: Threshold must be between 1 and 100")
            continue
        break

    alarm = alarm_manager.create_alarm(area, threshold)
    print(f"\n✅ Alarm created: [{alarm['area']}] ({alarm['threshold']}%)")