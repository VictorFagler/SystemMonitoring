# System Monitoring Application

A Python application that monitors CPU, memory, and disk usage. Users can create alarms for thresholds and view live system stats.

## Features
- Start and view system monitoring
- Configure, view, and remove alarms
- Live monitoring with alarm notifications
- Supports saving alarms to disk (JSON)
- Optional GUI for real-time stats

## Installation
```bash
git clone <repo_url>
cd <repo_folder>
python -m venv venv
source venv/bin/activate  # or venv\Scripts\Activate.ps1 on Windows
pip install -r requirements.txt
python main.py
Usage
Use the menu to start monitoring, configure alarms, and view stats. Alarms trigger warnings if thresholds are exceeded.
