import tkinter as tk
from monitor import *
from alarms import *
root = tk.Tk()
root.title("System Monitoring")
root.geometry("500x400")
label = tk.Label(root, text="System Monitoring", font=('Arial', 18))
label.pack(padx=20, pady=20)

def start_monitoring_loop():
    cpu, mem_used, mem_total, mem_percent, disk_used, disk_total, disk_percent = start_monitoring()
    cpu_label.config(text=f"CPU Usage: {cpu}%")
    mem_label.config(text=f"Memory: {mem_used} GB / {mem_total} GB ({mem_percent}%)")
    disk_label.config(text=f"Disk: {disk_used} GB / {disk_total} GB ({disk_percent}%)")
    root.after(1000, start_monitoring_loop)

def on_list_active_monitoring():
    list_active_monitoring()

def on_create_alarm():
    create_alarm()

def on_show_alarms():
    show_alarms()

def on_start_monitoring_mode():
    start_monitoring_mode()

# Frame för knappar
button_frame = tk.Frame(root)
button_frame.pack(pady=20)  # extra avstånd runt hela frame

tk.Button(button_frame, text="1. Start monitoring", command=start_monitoring_loop, anchor='w').pack(fill='x')
tk.Button(button_frame, text="2. List active monitoring", command=on_list_active_monitoring, anchor='w').pack(fill='x')
tk.Button(button_frame, text="3. Create alarm", command=on_create_alarm, anchor='w').pack(fill='x')
tk.Button(button_frame, text="4. Show alarms", command=on_show_alarms, anchor='w').pack(fill='x')
tk.Button(button_frame, text="5. Start monitoring mode", command=on_start_monitoring_mode, anchor='w').pack(fill='x')
tk.Button(button_frame, text="0. Exit", command=root.destroy, anchor='w').pack(fill='x')


# Frame för status
status_frame = tk.Frame(root)
status_frame.pack(pady=20)
cpu_label = tk.Label(status_frame, text="CPU: ")
cpu_label.pack()
mem_label = tk.Label(status_frame, text="Memory Usage: ")
mem_label.pack()
disk_label = tk.Label(status_frame, text="Disk Usage: ")
disk_label.pack()
status_label = tk.Label(status_frame, text="")
status_label.pack(pady=20)

root.mainloop()