from utils import *
import json

ALARM_FILE = os.path.join("data", "alarms_list.json") 

class AlarmManager:
    def __init__(self, file_path=ALARM_FILE):
        self.file_path = file_path
        self.alarms = {"CPU": [], "Memory": [], "Disk": []}
        self.last_removed = None
        self.load_alarms() 

    def create_alarm(self, area, threshold):
        alarm = {"threshold": int(threshold)}
        self.alarms[area].append(alarm)
        self.alarms[area].sort(key=lambda a: a["threshold"]) 
        self.save_alarms()
        write_log(f"Alarm created: [{area}] ({threshold}%)")
        return alarm
    
    def get_alarms(self):
        return self.alarms
    
    def delete_alarm(self, area, index):
        removed = self.alarms[area].pop(index)
        self.save_alarms()
        write_log(f"Alarm deleted: [{area}] ({removed['threshold']}%)")

        self.last_removed = {"area": area, "threshold": removed["threshold"]} 

        return removed
        
    def show_and_delete_alarms(self):
        while True:
            clear_screen()
            alarms = self.get_alarms()

            flat_alarm_list = []
            for area, alarms_in_area in alarms.items(): 
                for alarm in alarms_in_area:
                    flat_alarm_list.append((area, alarm))

            self.print_alarm_list(flat_alarm_list)

            input_choice = safe_input("Your choice: ").strip()
            if input_choice == "":
                clear_screen()
                return

            self.handle_alarm_choice(input_choice, flat_alarm_list)

    def print_alarm_list(self, flat_alarm_list):
        print("\n=== Active Alarms ===\n")

        if self.last_removed:
            last_removed = self.last_removed
            print(f"❌ Deleted alarm: [{last_removed['area']}] ({last_removed['threshold']}%)\n")
            self.last_removed = None

        if not flat_alarm_list:
            print("No active alarms.")
            return

        for i, (area, alarm) in enumerate(flat_alarm_list, start=1):
            print(f"{i}. [{area}] {alarm['threshold']}%")

        print("\nPress Enter to return or type a number to delete an alarm.\n")

    def handle_alarm_choice(self, input_choice, flat_alarm_list):
        try:
            index = int(input_choice) - 1

            if not (0 <= index < len(flat_alarm_list)):
                print("\n❌ Invalid number.")
                safe_input("\nPress Enter to continue...")
                return

            area, alarm_to_remove = flat_alarm_list[index]

            self.alarms[area].remove(alarm_to_remove)
            self.save_alarms()
            self.last_removed = {"area": area, "threshold": alarm_to_remove["threshold"]}
            write_log(f"Alarm deleted: [{area}] ({alarm_to_remove['threshold']}%)")

        except ValueError:
            print("\n❌ Please enter a valid number.")
            safe_input("\nPress Enter to continue...")
    
 #   === Alarm File Handling ===
    def save_alarms(self):
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(self.alarms, f, indent=4)

        except Exception as e:
            print(f"❌ Error saving alarms: {e}")
            write_log(f"Error saving alarms: {e}")

    def load_alarms(self):
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r") as f:
                    self.alarms = json.load(f)
            except (json.JSONDecodeError, OSError) as e:
                print(f"⚠️  Warning: Could not load alarms ({e}). Starting fresh.")
                self.alarms = {"CPU": [], "Memory": [], "Disk": []}
                write_log(f"Alarm file load error: {e}")

alarm_manager = AlarmManager() # Create a shared global instance