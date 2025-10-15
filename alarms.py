from utils import *
import json

ALARM_FILE = os.path.join("data", "alarms_list.json")  # File to store alarms

class AlarmManager:
    def __init__(self, file_path=ALARM_FILE):
        self.file_path = file_path
        self.alarms = []
        self.load_alarms()  # Load alarms from file at startup

    def create_alarm(self, area, threshold):
        alarm = {"area": area, "threshold": int(threshold)}
        self.alarms.append(alarm)
        self.alarms.sort(key=lambda a: a["area"])  # keep sorted all the time
        self.save_alarms()
        write_log(f"Alarm created: [{area}] ({threshold}%)")
        return alarm
    
    def get_alarms(self):
        return self.alarms
    
    def delete_alarm(self, index):
        if 0 <= index < len(self.alarms):
            removed_alarm = self.alarms.pop(index)
            self.save_alarms()
            write_log(f"Alarm deleted: [{removed_alarm['area']}] ({removed_alarm['threshold']}%)")
            return removed_alarm
        else:
            return None
        
    def show_and_delete_alarms(self):
        while True:
            clear_screen()
            alarms = self.get_alarms()
            self._print_alarm_list(alarms)

            if not alarms:
                safe_input("\nPress Enter to return to menu...")
                clear_screen()
                return

            input_choice = safe_input("Your choice (Enter to exit): ").strip()
            if input_choice == "":
                clear_screen()
                return

            self._handle_alarm_choice(input_choice)

    def _print_alarm_list(self, alarms):
        print("\n=== Active Alarms ===\n")

        # Show the most recently deleted alarm (once)
        if getattr(self, "_last_removed", None):
            last_removed = self._last_removed
            print(f"❌ Deleted alarm: [{last_removed['area']}] ({last_removed['threshold']}%)\n")
            self._last_removed = None

        if not alarms:
            print("No active alarms.")
            return

        for i, alarm in enumerate(alarms, start=1):
            print(f"{i}. [{alarm['area']}] ({alarm['threshold']}%)")
        print("\nPress Enter to return or type a number to delete an alarm.\n")

    def _handle_alarm_choice(self, input_choice):
        try:
            index = int(input_choice) - 1
            removed = self.delete_alarm(index)
            if removed:
                self._last_removed = removed
            else:
                print("\n❌ Invalid number.")
                safe_input("\nPress Enter to continue...")
        except ValueError:
            print("\n❌ Please enter a valid number.")
            safe_input("\nPress Enter to continue...")
 
 #   === File Handling ===

    def save_alarms(self):
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(self.alarms, f, indent=4)

        except Exception as e:
            print(f"❌ Error saving alarms: {e}")
            write_log(f"Error saving alarms: {e}")

    def load_alarms(self):  #Load alarms from JSON file if it exists. 
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r") as f:
                    self.alarms = json.load(f)

            except (json.JSONDecodeError, OSError) as e:
                print(f"⚠️  Warning: Could not load alarms ({e}). Starting fresh.")
                self.alarms = []
                write_log(f"Alarm file load error: {e}")

alarm_manager = AlarmManager() # Create a shared global instance