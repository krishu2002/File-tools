import os
import customtkinter as ctk
from tkinter import filedialog, messagebox


def open_file_creator_window():
    win = ctk.CTkToplevel()
    win.title("Smart Tools - File/Folder Creator")
    win.geometry("500x450")
    win.resizable(False, False)

    # ───── Variables ─────
    path_var = ctk.StringVar()
    name_var = ctk.StringVar()
    extension_var = ctk.StringVar(value=".txt")  # default extension

    # ───── Functions ─────
    def browse_path():
        folder = filedialog.askdirectory(title="Select Destination Folder")
        if folder:
            path_var.set(folder)

    def create_folder():
        folder_path = os.path.join(path_var.get(), name_var.get())
        try:
            os.makedirs(folder_path)
            messagebox.showinfo("Success", f"Folder created at:\n{folder_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create folder:\n{e}")

    def create_file():
        filename = name_var.get() + extension_var.get()
        file_path = os.path.join(path_var.get(), filename)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("")  # create empty file
            messagebox.showinfo("Success", f"File created at:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create file:\n{e}")

    # ───── Layout ─────
    frame = ctk.CTkFrame(win)
    frame.pack(padx=20, pady=20, fill="both", expand=True)

    ctk.CTkLabel(frame, text="📁 File / Folder Creator", font=("Arial", 20)).pack(pady=10)

    ctk.CTkLabel(frame, text="Destination Path:").pack(pady=(10, 0))
    row1 = ctk.CTkFrame(frame)
    row1.pack(pady=5)
    ctk.CTkEntry(row1, textvariable=path_var, width=300).pack(side="left", padx=5)
    ctk.CTkButton(row1, text="Browse", command=browse_path).pack(side="left")

    ctk.CTkLabel(frame, text="Name:").pack(pady=(10, 0))
    ctk.CTkEntry(frame, textvariable=name_var, width=250).pack(pady=5)

    # Optional file extension
    ctk.CTkLabel(frame, text="File Extension (for files):").pack(pady=(10, 0))
    ctk.CTkComboBox(frame, values=[".txt", ".py", ".md", ".log", ".html"], variable=extension_var, width=100).pack()

    # Buttons
    btn_frame = ctk.CTkFrame(frame)
    btn_frame.pack(pady=20)

    ctk.CTkButton(btn_frame, text="📄 Create File", command=create_file).pack(side="left", padx=10)
    ctk.CTkButton(btn_frame, text="📂 Create Folder", command=create_folder).pack(side="left", padx=10)

    win.mainloop()
