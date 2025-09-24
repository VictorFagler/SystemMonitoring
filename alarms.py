# alarms.py
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
