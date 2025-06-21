import os
import shutil
import subprocess
import customtkinter as ctk
from tkinter import filedialog, messagebox
import tkinter as tk  # Needed for Listbox


def open_file_finder_window():
    win = ctk.CTkToplevel()
    win.title("Smart Tools - File Finder")
    win.geometry("800x700")
    win.resizable(False, False)

    name_var = ctk.StringVar()
    path_var = ctk.StringVar()
    full_path_var = ctk.StringVar()
    results = []

    # ───── Functions ─────
    def browse_folder():
        folder = filedialog.askdirectory(title="Select Root Folder")
        if folder:
            path_var.set(folder)

    def search_files():
        search_name = name_var.get().lower()
        root_path = path_var.get()
        result_listbox.delete(0, "end")
        preview_box.configure(state="normal")
        preview_box.delete("0.0", "end")
        preview_box.configure(state="disabled")
        full_path_var.set("")
        results.clear()

        if not os.path.isdir(root_path):
            messagebox.showerror("Error", "Invalid folder path.")
            return

        for dirpath, _, filenames in os.walk(root_path):
            for file in filenames:
                if search_name in file.lower():
                    full = os.path.join(dirpath, file)
                    results.append(full)
                    result_listbox.insert("end", file)

        if not results:
            result_listbox.insert("end", "❌ No matching files found")

    def on_select_file(event):
        if not results:
            return
        selection = result_listbox.curselection()
        if not selection:
            return
        index = selection[0]
        if index >= len(results):
            return

        selected_path = results[index]
        full_path_var.set(selected_path)

        preview_box.configure(state="normal")
        preview_box.delete("0.0", "end")
        try:
            if selected_path.lower().endswith((".txt", ".py", ".log", ".md")):
                with open(selected_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read(5000)
                    preview_box.insert("end", content)
            else:
                preview_box.insert("end", "(Preview not supported for this file type.)")
        except Exception as e:
            preview_box.insert("end", f"Error reading file:\n{e}")
        preview_box.configure(state="disabled")

    def open_file_location():
        path = full_path_var.get()
        if not os.path.isfile(path):
            messagebox.showwarning("Warning", "No file selected.")
            return
        try:
            if os.name == "nt":
                subprocess.Popen(f'explorer /select,"{path}"')
            else:
                subprocess.Popen(["xdg-open", os.path.dirname(path)])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open file location:\n{e}")

    def open_file():
        path = full_path_var.get()
        if not os.path.isfile(path):
            messagebox.showwarning("No File", "No valid file selected.")
            return
        try:
            os.startfile(path) if os.name == "nt" else subprocess.Popen(["xdg-open", path])
        except Exception as e:
            messagebox.showerror("Error", f"Can't open file:\n{e}")

    def delete_file():
        path = full_path_var.get()
        if not os.path.isfile(path):
            messagebox.showwarning("No File", "No valid file selected.")
            return
        confirm = messagebox.askyesno("Delete", f"Are you sure you want to delete this file?\n\n{path}")
        if confirm:
            try:
                os.remove(path)
                messagebox.showinfo("Deleted", "File deleted successfully.")
                search_files()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete file:\n{e}")

    def copy_file():
        path = full_path_var.get()
        if not os.path.isfile(path):
            messagebox.showwarning("No File", "No valid file selected.")
            return
        target = filedialog.askdirectory(title="Select Destination Folder")
        if target:
            try:
                shutil.copy2(path, target)
                messagebox.showinfo("Copied", f"File copied to:\n{target}")
            except Exception as e:
                messagebox.showerror("Error", f"Copy failed:\n{e}")

    # ───── Layout ─────
    frame = ctk.CTkFrame(win)
    frame.pack(padx=20, pady=20, fill="both", expand=True)

    ctk.CTkLabel(frame, text="🔍 File Finder", font=("Arial", 20)).pack(pady=10)

    # Search Fields
    row1 = ctk.CTkFrame(frame)
    row1.pack(pady=5)
    ctk.CTkLabel(row1, text="Search File Name:").pack(side="left", padx=5)
    ctk.CTkEntry(row1, textvariable=name_var, width=250).pack(side="left", padx=5)

    row2 = ctk.CTkFrame(frame)
    row2.pack(pady=5)
    ctk.CTkLabel(row2, text="Search In Folder:").pack(side="left", padx=5)
    ctk.CTkEntry(row2, textvariable=path_var, width=300).pack(side="left", padx=5)
    ctk.CTkButton(row2, text="Browse", command=browse_folder).pack(side="left", padx=5)

    ctk.CTkButton(frame, text="Search", command=search_files).pack(pady=10)

    # Result Listbox
    list_frame = ctk.CTkFrame(frame)
    list_frame.pack(fill="both", expand=False)

    scrollbar = tk.Scrollbar(list_frame)
    scrollbar.pack(side="right", fill="y")

    result_listbox = tk.Listbox(list_frame, height=10, yscrollcommand=scrollbar.set, font=("Consolas", 11))
    result_listbox.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=result_listbox.yview)

    result_listbox.bind("<<ListboxSelect>>", on_select_file)

    # Full Path (readonly)
    ctk.CTkLabel(frame, text="Full Path:").pack()
    path_entry = ctk.CTkEntry(frame, textvariable=full_path_var, width=750)
    path_entry.pack(pady=5)
    path_entry.configure(state="readonly")

    # Preview Box (readonly)
    ctk.CTkLabel(frame, text="File Preview (text files):").pack()
    preview_box = ctk.CTkTextbox(frame, height=180, wrap="word")
    preview_box.pack(pady=5, fill="both", expand=True)
    preview_box.configure(state="disabled")

    # Action Buttons
    btn_row = ctk.CTkFrame(frame)
    btn_row.pack(pady=10)

    ctk.CTkButton(btn_row, text="📂 Open File", command=open_file).pack(side="left", padx=10)
    ctk.CTkButton(btn_row, text="🗑️ Delete File", command=delete_file).pack(side="left", padx=10)
    ctk.CTkButton(btn_row, text="📄 Copy File", command=copy_file).pack(side="left", padx=10)
    ctk.CTkButton(btn_row, text="📁 Open Location", command=open_file_location).pack(side="left", padx=10)

    win.mainloop()
