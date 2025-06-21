import customtkinter as ctk
import psutil
import threading
import time


def open_system_info_window():
    win = ctk.CTkToplevel()
    win.title("Smart Tools - System Info")
    win.geometry("400x350")
    win.resizable(False, False)

    ctk.CTkLabel(win, text="🧠 System Monitor", font=("Arial", 22)).pack(pady=15)

    cpu_label = ctk.CTkLabel(win, text="CPU Usage: 0%")
    cpu_label.pack()
    cpu_bar = ctk.CTkProgressBar(win, width=300)
    cpu_bar.pack(pady=5)

    ram_label = ctk.CTkLabel(win, text="RAM Usage: 0%")
    ram_label.pack()
    ram_bar = ctk.CTkProgressBar(win, width=300)
    ram_bar.pack(pady=5)

    disk_label = ctk.CTkLabel(win, text="Storage Usage: 0%")
    disk_label.pack()
    disk_bar = ctk.CTkProgressBar(win, width=300)
    disk_bar.pack(pady=5)

    def update_loop():
        while True:
            cpu = psutil.cpu_percent()
            ram = psutil.virtual_memory().percent
            disk = psutil.disk_usage("/").percent

            cpu_bar.set(cpu / 100)
            cpu_label.configure(text=f"CPU Usage: {cpu}%")

            ram_bar.set(ram / 100)
            ram_label.configure(text=f"RAM Usage: {ram}%")

            disk_bar.set(disk / 100)
            disk_label.configure(text=f"Storage Usage: {disk}%")

            time.sleep(1)

    # Run update in background thread to keep UI responsive
    threading.Thread(target=update_loop, daemon=True).start()

    win.mainloop()
