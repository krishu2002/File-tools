import customtkinter as ctk
import time
import psutil
from modules.file_organizer import open_file_organizer_window
from modules.file_finder import open_file_finder_window
from modules.file_maker import open_file_creator_window
from modules.file_manager import open_file_manager_window

# ──────────────────────
# 1. SET DARK UI THEME
# ──────────────────────
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


# ─────────────────────────────
# 2. SPLASH / LOADING SCREEN
# ─────────────────────────────
def show_loading_screen():
    splash = ctk.CTk()
    splash.title("Smart Tools - Loading")
    splash.geometry("400x250")
    splash.resizable(False, False)

    label = ctk.CTkLabel(splash, text="Smart Tools", font=("Arial", 24))
    label.pack(pady=40)

    progress = ctk.CTkProgressBar(splash, width=250)
    progress.pack(pady=20)
    progress.start()

    def finish_loading():
        progress.stop()
        splash.destroy()
        open_home_screen()

    splash.after(3000, finish_loading)
    splash.mainloop()


# ─────────────────────────────
# 3. MAIN DASHBOARD SCREEN
# ─────────────────────────────
def open_home_screen():
    app = ctk.CTk()
    app.title("Smart Tools")
    app.geometry("850x500")
    app.resizable(False, False)

    # ───── Title ─────
    title_label = ctk.CTkLabel(app, text="🛠️ Smart Tools Dashboard", font=("Arial", 22))
    title_label.pack(pady=20)

    # ───── Main Frame ─────
    main_frame = ctk.CTkFrame(app)
    main_frame.pack(padx=20, pady=10, fill="both", expand=True)

    # ───── Left Side: Tools Buttons ─────
    button_frame = ctk.CTkFrame(main_frame)
    button_frame.pack(side="left", fill="y", padx=10, pady=10)

    tools = {
        "📁 File Organizer": open_file_organizer_window,
        "🔍 File Finder": open_file_finder_window,
        "📂 Create File/Folder": open_file_creator_window,
        "🗃️ Open File Manager": open_file_manager_window
    }

    for label, command in tools.items():
        btn = ctk.CTkButton(button_frame, text=label, width=240, height=40, font=("Arial", 12), command=command)
        btn.pack(pady=8)

    # ───── Right Side: System Monitor ─────
    stats_frame = ctk.CTkFrame(main_frame)
    stats_frame.pack(side="right", fill="both", padx=20, pady=10)

    ctk.CTkLabel(stats_frame, text="📊 System Monitor", font=("Arial", 18, "bold")).pack(pady=10)

    cpu_label = ctk.CTkLabel(stats_frame, text="🧠 CPU Usage: ...", font=("Arial", 14))
    ram_label = ctk.CTkLabel(stats_frame, text="💽 RAM Usage: ...", font=("Arial", 14))
    disk_label = ctk.CTkLabel(stats_frame, text="📊 Disk Usage: ...", font=("Arial", 14))

    cpu_label.pack(pady=5)
    ram_label.pack(pady=5)
    disk_label.pack(pady=5)

    # ───── Update System Info Every Second ─────
    def update_stats():
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent

        cpu_label.configure(text=f"🧠 CPU Usage: {cpu}%")
        ram_label.configure(text=f"💽 RAM Usage: {ram}%")
        disk_label.configure(text=f"📊 Disk Usage: {disk}%")

        app.after(1000, update_stats)

    update_stats()

    app.mainloop()


# ──────────────────────
# 4. START APP
# ──────────────────────
if __name__ == "__main__":
    show_loading_screen()
