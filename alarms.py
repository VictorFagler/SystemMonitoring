from utils import *
import json

ALARM_FILE = "alarms.json"  # File to store alarms

class AlarmManager:
    def __init__(self, file_path=ALARM_FILE):
        self.file_path = file_path
        self.alarms = []
        self.load_alarms()  # Load alarms from file at startup

    def create_alarm(self, area, threshold):
        """Create a new alarm and save immediately."""
        alarm = {
            "area": area,
            "threshold": int(threshold)
        }
        self.alarms.append(alarm)
        self.save_alarms()
        return alarm

    def get_alarms(self):
        """Return the list of alarms."""
        return self.alarms

    def save_alarms(self):
        """Save alarms to JSON file."""
        with open(self.file_path, "w") as f:
            json.dump(self.alarms, f, indent=4)

    def load_alarms(self):
        """Load alarms from JSON file if it exists."""
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r") as f:
                    self.alarms = json.load(f)
            except json.JSONDecodeError:
                print("Warning: Could not decode alarms.json. Starting with empty alarms.")
                self.alarms = []

# Create a shared global instance
alarm_manager = AlarmManager()


def build_alarm_menu(alarm_manager):
    """Menu to create new alarms and save them."""
    clear_screen()
    while True:
        print("\n=== Configure Alarms ===")
        print("1. CPU")
        print("2. RAM")
        print("3. Memory")
        choice = input("Choose alarm option 1-3: ").strip()

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
            threshold = int(threshold_input)
        except ValueError:
            print("Error: Threshold must be a number")
            continue

        if threshold < 1 or threshold > 100:
            print("Error: Threshold must be between 1 and 100")
            continue
        break

    # Create the alarm and save it
    alarm = alarm_manager.create_alarm(area, threshold)
    clear_screen()
    print()
    print(f"\n✅ Alarm created: [{alarm['area']}] ({alarm['threshold']}%)")