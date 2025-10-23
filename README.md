# System Monitoring Application

A Python application that monitors CPU, memory, and disk usage. Users can create alarms for thresholds and view live system stats.

## Features
- Start and view system monitoring
- Configure, view, and remove alarms
- Live monitoring with alarm notifications
- Supports saving alarms to disk (JSON)

## Usage
After running `python main.py`, use the menu to navigate the program:

1. **Start/Stop Monitoring** – Start or stop live monitoring of CPU, memory, and disk usage.
2. **List Active Monitoring** – Display current system stats while monitoring runs in the background.
3. **Create Alarm** – Configure alarms for CPU, memory, or disk thresholds (1–100%).
4. **Show/Delete Alarms** – View active alarms and remove them if needed.
5. **Start Monitoring Mode** – Run monitoring mode where alarms are automatically triggered if thresholds are exceeded.
0. **Exit** – Quit the application.

Press Enter to return to the main menu at any point.

## Installation
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\Activate.ps1 on Windows
pip install -r requirements.txt
python main.py