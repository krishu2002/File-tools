import customtkinter as ctk
from PIL import Image
import time
import psutil
import os
import sys

# ─────────────────────────────
# DYNAMIC RESOURCE PATH FOR EXE
# ─────────────────────────────
def resource_path(relative_path):
    """Get absolute path to resource for PyInstaller"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# ──────────────────────
# 1. IMPORT MODULES
# ──────────────────────
from modules.file_organizer import open_file_organizer_window
from modules.file_finder import open_file_finder_window
from modules.file_maker import open_file_creator_window
from modules.file_manager import open_file_manager_window

# ──────────────────────
# 2. SET DARK UI THEME
# ──────────────────────
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# ──────────────────────
# 3. PATHS TO IMAGES
# ──────────────────────
ICON_PATH = resource_path("assets/logo.ico")   # For taskbar
LOGO_PATH = resource_path("assets/logo.png")   # For splash image

# ─────────────────────────────
# 4. SPLASH / LOADING SCREEN
# ─────────────────────────────
def show_loading_screen():
    splash = ctk.CTk()
    splash.title("Smart Tools - Loading")
    splash.geometry("400x300")
    splash.resizable(False, False)

    # Taskbar icon
    try:
        splash.iconbitmap(ICON_PATH)
    except Exception as e:
        print("Icon load failed:", e)

    # Logo image
    try:
        logo = ctk.CTkImage(light_image=Image.open(LOGO_PATH), size=(150, 150))
        ctk.CTkLabel(splash, image=logo, text="").pack(pady=5)
    except Exception as e:
        print("Logo not loaded:", e)
        ctk.CTkLabel(splash, text="Smart Tools", font=("Arial", 22)).pack(pady=10)

    ctk.CTkLabel(splash, text="Loading Smart Tools...", font=("Arial", 16)).pack(pady=10)

    progress = ctk.CTkProgressBar(splash, width=250)
    progress.pack(pady=20)
    progress.start()

    def finish():
        progress.stop()
        splash.destroy()
        open_home_screen()

    splash.after(3000, finish)
    splash.mainloop()

# ─────────────────────────────
# 5. MAIN DASHBOARD SCREEN
# ─────────────────────────────
def open_home_screen():
    app = ctk.CTk()
    app.title("Smart Tools")
    app.geometry("850x500")
    app.resizable(False, False)

    try:
        app.iconbitmap(ICON_PATH)
    except Exception as e:
        print("Icon load failed:", e)

    ctk.CTkLabel(app, text="🛠️ Smart Tools Dashboard", font=("Arial", 22)).pack(pady=20)

    main_frame = ctk.CTkFrame(app)
    main_frame.pack(padx=20, pady=10, fill="both", expand=True)

    # Left Tools Panel
    tool_frame = ctk.CTkFrame(main_frame)
    tool_frame.pack(side="left", fill="y", padx=10, pady=10)

    tools = {
        "📁 File Organizer": open_file_organizer_window,
        "🔍 File Finder": open_file_finder_window,
        "📂 Create File/Folder": open_file_creator_window,
        "🗃️ Open File Manager": open_file_manager_window
    }

    for label, command in tools.items():
        ctk.CTkButton(tool_frame, text=label, width=240, height=40, font=("Arial", 12), command=command).pack(pady=8)

    # Right Stats Panel
    stats_frame = ctk.CTkFrame(main_frame)
    stats_frame.pack(side="right", fill="both", padx=20, pady=10)

    ctk.CTkLabel(stats_frame, text="📊 System Monitor", font=("Arial", 18, "bold")).pack(pady=10)

    cpu_label = ctk.CTkLabel(stats_frame, text="🧠 CPU Usage: ...", font=("Arial", 14))
    ram_label = ctk.CTkLabel(stats_frame, text="💽 RAM Usage: ...", font=("Arial", 14))
    disk_label = ctk.CTkLabel(stats_frame, text="📊 Disk Usage: ...", font=("Arial", 14))

    cpu_label.pack(pady=5)
    ram_label.pack(pady=5)
    disk_label.pack(pady=5)

    def update_stats():
        cpu_label.configure(text=f"🧠 CPU Usage: {psutil.cpu_percent()}%")
        ram_label.configure(text=f"💽 RAM Usage: {psutil.virtual_memory().percent}%")
        disk_label.configure(text=f"📊 Disk Usage: {psutil.disk_usage('/').percent}%")
        app.after(1000, update_stats)

    update_stats()
    app.mainloop()

# ──────────────────────
# 6. START APP
# ──────────────────────
if __name__ == "__main__":
    show_loading_screen()
