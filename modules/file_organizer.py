import os
import shutil
import subprocess
import customtkinter as ctk
from tkinter import filedialog, messagebox


def open_file_organizer_window():
    win = ctk.CTkToplevel()
    win.title("Smart Tools - File Organizer")
    win.geometry("600x600")
    win.resizable(False, False)

    # ───── Variables ─────
    source_var = ctk.StringVar()
    dest_var = ctk.StringVar()
    what_var = ctk.StringVar(value="both")
    action_var = ctk.StringVar(value="cut")
    filter_var = ctk.StringVar()
    log_var = ctk.StringVar()
    total_var = ctk.StringVar(value="")

    # ───── Browse Functions ─────
    def browse_source():
        folder = filedialog.askdirectory(title="Select Source Folder")
        if folder:
            source_var.set(folder)

    def browse_dest():
        folder = filedialog.askdirectory(title="Select Destination Folder")
        if folder:
            dest_var.set(folder)

    def reset_fields():
        source_var.set("")
        dest_var.set("")
        filter_var.set("")
        log_box.delete("0.0", "end")
        total_var.set("")

    def open_destination():
        path = dest_var.get()
        if os.path.isdir(path):  # More accurate than os.path.exists
            try:
                if os.name == "nt":  # Windows
                    os.startfile(path)
                elif os.name == "posix":  # macOS/Linux
                    subprocess.Popen(["xdg-open", path])
                else:
                    messagebox.showinfo("Info", f"Manual: Please open this path:\n{path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open folder:\n{e}")
        else:
            messagebox.showwarning("Invalid Path", "Destination folder not set or invalid.")


    # ───── Organize Function ─────
    def organize():
        src = source_var.get()
        dst = dest_var.get()
        what = what_var.get()
        action = action_var.get()
        ext_filter = filter_var.get().lower().split(",") if filter_var.get() else []

        if not os.path.isdir(src) or not os.path.isdir(dst):
            messagebox.showerror("Error", "Please select valid source and destination paths.")
            return

        total_moved = 0
        log_box.delete("0.0", "end")
        progress_bar.set(0)

        try:
            items = os.listdir(src)
            total = len(items)
            for idx, item in enumerate(items):
                full_path = os.path.join(src, item)
                moved = False

                if os.path.isfile(full_path) and what in ["files", "both"]:
                    ext = os.path.splitext(item)[1][1:].lower()
                    if ext_filter and ext not in ext_filter:
                        continue

                    folder_name = ext.upper() or "NOEXT"
                    target_dir = os.path.join(dst, folder_name)
                    os.makedirs(target_dir, exist_ok=True)

                    target_path = os.path.join(target_dir, item)
                    if os.path.exists(target_path):
                        log_box.insert("end", f"⛔ Skipped (exists): {item}\n")
                        continue

                    if action == "cut":
                        shutil.move(full_path, target_path)
                    else:
                        shutil.copy2(full_path, target_path)

                    log_box.insert("end", f"✅ Moved: {item} → {folder_name}/\n")
                    moved = True

                elif os.path.isdir(full_path) and what in ["folders", "both"]:
                    target_dir = os.path.join(dst, "FOLDERS")
                    os.makedirs(target_dir, exist_ok=True)

                    target_path = os.path.join(target_dir, item)
                    if os.path.exists(target_path):
                        log_box.insert("end", f"⛔ Skipped folder (exists): {item}\n")
                        continue

                    if action == "cut":
                        shutil.move(full_path, target_path)
                    else:
                        shutil.copytree(full_path, target_path, dirs_exist_ok=True)

                    log_box.insert("end", f"📁 Moved Folder: {item} → FOLDERS/\n")
                    moved = True

                if moved:
                    total_moved += 1

                progress_bar.set((idx + 1) / total)

            total_var.set(f"✅ Total items organized: {total_moved}")
            log_box.insert("end", "\n🎉 Organizing complete!")

        except Exception as e:
            messagebox.showerror("Error", f"Something went wrong: {e}")

    # ───── UI Layout ─────
    frame = ctk.CTkFrame(win)
    frame.pack(padx=20, pady=20, fill="both", expand=True)

    ctk.CTkLabel(frame, text="📁 File Organizer", font=("Arial", 20)).pack(pady=10)

    # ───── Input Rows ─────
    def make_row(label_text, var, button_text, browse_cmd):
        row = ctk.CTkFrame(frame, fg_color="transparent")
        row.pack(pady=5, fill="x")
        ctk.CTkLabel(row, text=label_text, width=130).pack(side="left")
        ctk.CTkEntry(row, textvariable=var, width=300).pack(side="left", padx=5)
        ctk.CTkButton(row, text=button_text, width=60, command=browse_cmd).pack(side="left")

    make_row("Source Path (From):", source_var, "Browse", browse_source)
    make_row("Destination Path (To):", dest_var, "Browse", browse_dest)

    # ───── Dropdowns and Filter ─────
    row_options = ctk.CTkFrame(frame)
    row_options.pack(pady=5)
    ctk.CTkLabel(row_options, text="What to Organize:").pack(side="left", padx=5)
    ctk.CTkOptionMenu(row_options, variable=what_var, values=["files", "folders", "both"]).pack(side="left", padx=5)
    ctk.CTkLabel(row_options, text="Action:").pack(side="left", padx=5)
    ctk.CTkOptionMenu(row_options, variable=action_var, values=["cut", "copy"]).pack(side="left", padx=5)

    row_filter = ctk.CTkFrame(frame)
    row_filter.pack(pady=5)
    ctk.CTkLabel(row_filter, text="Extension Filter (e.g. jpg,pdf):").pack(side="left", padx=5)
    ctk.CTkEntry(row_filter, textvariable=filter_var, width=200).pack(side="left", padx=5)

    # ───── Buttons ─────
    btn_row = ctk.CTkFrame(frame, fg_color="transparent")
    btn_row.pack(pady=10)
    ctk.CTkButton(btn_row, text="Organize Files", command=organize).pack(side="left", padx=10)
    ctk.CTkButton(btn_row, text="Open Folder", command=open_destination).pack(side="left", padx=10)
    ctk.CTkButton(btn_row, text="Reset", command=reset_fields).pack(side="left", padx=10)

    # ───── Status and Log ─────
    progress_bar = ctk.CTkProgressBar(frame, height=10)
    progress_bar.pack(pady=10, fill="x")
    progress_bar.set(0)

    ctk.CTkLabel(frame, textvariable=total_var, text_color="lightgreen", font=("Arial", 12)).pack(pady=5)

    log_box = ctk.CTkTextbox(frame, height=200, font=("Courier", 11))
    log_box.pack(pady=10, fill="both", expand=True)

    win.mainloop()
