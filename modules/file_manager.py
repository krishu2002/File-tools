import os
import shutil
import subprocess
import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox

def open_file_manager_window():
    win = ctk.CTkToplevel()
    win.title("Smart Tools - File Manager")
    win.geometry("800x600")
    win.resizable(True, True)

    current_path = os.path.expanduser("~")
    path_var = ctk.StringVar(value=current_path)

    # Path Entry and Browse Button
    path_frame = ctk.CTkFrame(win)
    path_frame.pack(fill="x", padx=10, pady=5)

    entry = ctk.CTkEntry(path_frame, textvariable=path_var, state="readonly")
    entry.pack(side="left", fill="x", expand=True, padx=5)

    def browse_folder():
        folder = filedialog.askdirectory(initialdir=path_var.get())
        if folder:
            load_directory(folder)

    ctk.CTkButton(path_frame, text="Browse", command=browse_folder, width=80).pack(side="left", padx=5)

    # File Listbox using tkinter
    listbox = tk.Listbox(win, height=25)
    listbox.pack(fill="both", expand=True, padx=10, pady=5)

    # File Manager Buttons (Refresh, Back, Delete, Rename)
    button_frame = ctk.CTkFrame(win)
    button_frame.pack(fill="x", padx=10, pady=5)

    def load_directory(path):
        try:
            listbox.delete(0, "end")
            path_var.set(path)
            entries = os.listdir(path)
            entries.sort()
            for entry in entries:
                full_path = os.path.join(path, entry)
                icon = "📁" if os.path.isdir(full_path) else "📄"
                listbox.insert("end", f"{icon} {entry}")
        except Exception as e:
            messagebox.showerror("Error", f"Cannot open folder:\n{e}")

    def refresh():
        load_directory(path_var.get())

    def go_back():
        parent = os.path.dirname(path_var.get())
        if parent and os.path.exists(parent):
            load_directory(parent)

    def open_selected(event=None):
        selection = listbox.curselection()
        if not selection:
            return
        index = selection[0]
        item_text = listbox.get(index)[2:]
        full_path = os.path.join(path_var.get(), item_text)

        if os.path.isdir(full_path):
            load_directory(full_path)
        else:
            try:
                if os.name == "nt":
                    os.startfile(full_path)
                else:
                    subprocess.Popen(["xdg-open", full_path])
            except Exception as e:
                messagebox.showerror("Error", f"Cannot open file:\n{e}")

    def delete_selected():
        selection = listbox.curselection()
        if not selection:
            return
        index = selection[0]
        item_text = listbox.get(index)[2:]
        full_path = os.path.join(path_var.get(), item_text)

        confirm = messagebox.askyesno("Delete", f"Delete this?\n{full_path}")
        if confirm:
            try:
                if os.path.isdir(full_path):
                    shutil.rmtree(full_path)
                else:
                    os.remove(full_path)
                refresh()
            except Exception as e:
                messagebox.showerror("Error", f"Delete failed:\n{e}")

    def rename_selected():
        selection = listbox.curselection()
        if not selection:
            return
        index = selection[0]
        old_name = listbox.get(index)[2:]
        old_path = os.path.join(path_var.get(), old_name)

        new_name = filedialog.asksaveasfilename(initialdir=path_var.get(), initialfile=old_name)
        if new_name:
            try:
                os.rename(old_path, new_name)
                refresh()
            except Exception as e:
                messagebox.showerror("Error", f"Rename failed:\n{e}")

    # Action Buttons
    ctk.CTkButton(button_frame, text="🔄 Refresh", command=refresh).pack(side="left", padx=5)
    ctk.CTkButton(button_frame, text="⬅️ Back", command=go_back).pack(side="left", padx=5)
    ctk.CTkButton(button_frame, text="🗑️ Delete", command=delete_selected).pack(side="left", padx=5)
    ctk.CTkButton(button_frame, text="✏️ Rename", command=rename_selected).pack(side="left", padx=5)

    # Double-click opens files/folders
    listbox.bind("<Double-1>", open_selected)

    # Initial load
    load_directory(current_path)
