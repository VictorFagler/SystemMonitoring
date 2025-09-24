import tkinter as tk
from monitor import *
from alarms import *




############################## MONITORING ################################

monitoring = False  # startläge: avstängd

def monitoring_loop():
    if monitoring:
        cpu, mem_used, mem_total, mem_percent, disk_used, disk_total, disk_percent = start_monitoring()
        cpu_label.config(text=f"CPU Usage: {cpu}%")
        mem_label.config(text=f"Memory: {mem_used} GB / {mem_total} GB ({mem_percent}%)")
        disk_label.config(text=f"Disk: {disk_used} GB / {disk_total} GB ({disk_percent}%)")
        root.after(1000, monitoring_loop)

def toggle_monitoring():
#Starta/stoppa övervakning
    global monitoring
    if monitoring:
        monitoring = False  
        start_stop_button.config(text="1. Start monitoring")
    else:           
        monitoring = True
        start_stop_button.config(text="1. Stop monitoring")
        monitoring_loop()   

def on_list_active_monitoring():
    list_active_monitoring()

################################ ALARMS ###################################


def configure_alarm(area):
    alarm_window = tk.Toplevel(root)
    alarm_window.title(f"Konfigurera larm: {area}")
    alarm_window.geometry("320x170")

    tk.Label(alarm_window, text=f"{area} Alarm Name:").pack(pady=5)
    name_entry = tk.Entry(alarm_window)
    name_entry.pack(pady=5)

    tk.Label(alarm_window, text="Threshold (%):").pack(pady=5)
    threshold_entry = tk.Entry(alarm_window)
    threshold_entry.pack(pady=5)

    msg = tk.Label(alarm_window, text="", fg="red")
    msg.pack()

    def save_alarm_gui():
        name = name_entry.get().strip()
        threshold = threshold_entry.get().strip()
        if not name or not threshold:
            msg.config(text="Fyll i både namn och threshold")
            return
        try:
            thr_value = float(threshold)
        except ValueError:
            msg.config(text="Threshold måste vara ett tal (t.ex. 75 eller 75.0)")
            return

        create_alarm(area, name, thr_value)  # anropa alarms.py
        alarm_window.destroy()

    tk.Button(alarm_window, text="Spara", command=save_alarm_gui).pack(pady=10)

def build_alarm_menu():
    # töm frame
    for widget in button_frame.winfo_children():
        widget.destroy()

    tk.Label(button_frame, text="Konfigurera larm", font=('Arial', 14)).pack(pady=10)
    tk.Button(button_frame, text="CPU användning", command=lambda: configure_alarm("CPU"), anchor='w').pack(fill='x')
    tk.Button(button_frame, text="Minnesanvändning", command=lambda: configure_alarm("Memory"), anchor='w').pack(fill='x')
    tk.Button(button_frame, text="Diskanvändning", command=lambda: configure_alarm("Disk"), anchor='w').pack(fill='x')
    tk.Button(button_frame, text="Tillbaka till huvudmeny", command=build_main_menu, anchor='w').pack(fill='x')

def show_alarms():
    alarm_window = tk.Toplevel(root)
    alarm_window.title("Aktiva alarms")
    alarm_window.geometry("400x250")

    alarms_list = get_alarms()

    if not alarms_list:
        tk.Label(alarm_window, text="Inga alarms skapade ännu.").pack(pady=20)
        return

    listbox = tk.Listbox(alarm_window, width=60)
    listbox.pack(padx=10, pady=10, fill='both', expand=True)

    for i, alarm in enumerate(alarms_list, start=1):
        text = f"{i}. [{alarm['area']}] {alarm['name']} — threshold: {alarm['threshold']}"
        listbox.insert('end', text)


def on_start_monitoring_mode():
    start_monitoring_mode()



############################# GUI ######################################
root = tk.Tk()
root.title("System Monitoring")
root.geometry("500x400")
label = tk.Label(root, text="System Monitoring", font=('Arial', 18))
label.pack(padx=20, pady=20)

# Frame för knappar
button_frame = tk.Frame(root)
button_frame.pack(pady=20) 

# Main Menu
def build_main_menu():
    for widget in button_frame.winfo_children():
        widget.destroy()

    global start_stop_button
    start_stop_button = tk.Button(button_frame, text="1. Start monitoring", command=toggle_monitoring, anchor='w')
    start_stop_button.pack(fill='x')

    tk.Button(button_frame, text="2. List active monitoring", command=on_list_active_monitoring, anchor='w').pack(fill='x')
    tk.Button(button_frame, text="3. Create alarm", command=build_alarm_menu, anchor='w').pack(fill='x')
    tk.Button(button_frame, text="4. Show alarms", command=show_alarms, anchor='w').pack(fill='x')
    tk.Button(button_frame, text="5. Start monitoring mode", command=on_start_monitoring_mode, anchor='w').pack(fill='x')
    tk.Button(button_frame, text="0. Exit", command=root.destroy, anchor='w').pack(fill='x')



# Frame för status
status_frame = tk.Frame(root)
status_frame.pack(pady=20)
cpu_label = tk.Label(status_frame, text="CPU: ")
cpu_label.pack()
mem_label = tk.Label(status_frame, text="Memory: ")
mem_label.pack()
disk_label = tk.Label(status_frame, text="Disk: ")
disk_label.pack()


build_main_menu()
root.mainloop()