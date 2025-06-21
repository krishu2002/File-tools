
# 📘 How to Use Smart Tools

This guide explains how to use each feature in your **Smart Tools** desktop app.

---

## 🖥️ 1. Launching the App

### 🔹 Steps:
1. Open terminal or double-click `main.py`.
2. A **splash screen** will appear.
3. After 3 seconds, the **Smart Tools Dashboard** will open.

---

## 🧰 2. Home Dashboard Overview

You'll see:
- Left side: Tool buttons
- Right side: Live **CPU**, **RAM**, and **Storage** stats

---

## 🔧 3. File Organizer

**Function:** Organizes files in a selected folder into subfolders by file type.

### How to use:
1. Click `📁 File Organizer`.
2. Choose a folder to organize.
3. Select:
   - File type: Images, Docs, Audio, etc.
   - Action: Copy or Move
4. Click `Organize`.

✅ Your files will be neatly sorted into folders.

---

## 🔍 4. File Finder

**Function:** Search for files by name, preview text, and manage them.

### How to use:
1. Click `🔍 File Finder`.
2. Enter the file name (partial names allowed).
3. Select root folder to search.
4. Click `Search`.

🔸 Click a file from the results to:
- Preview text (for `.txt`, `.py`, `.log`, etc.)
- See full path
- Use buttons to:
  - 📂 Open
  - 🗑️ Delete
  - 📄 Copy

---

## 📂 5. Create File / Folder

**Function:** Quickly create new files or folders.

### How to use:
1. Click `📂 Create File/Folder`.
2. Choose:
   - File or Folder
   - Enter name and location
3. Click `Create`.

✅ Your file/folder will be created instantly.

---

## 🗃️ 6. File Manager

**Function:** Mini explorer to browse, open, delete, or rename files/folders.

### How to use:
1. Click `🗃️ Open File Manager`.
2. Select a directory.
3. Files/folders will be listed.
4. Click to:
   - Open
   - Delete
   - Rename

---

## 📊 7. System Monitor (Always On)

- Located on right side of the dashboard
- Updates every second
- Shows:
  - 🧠 CPU Usage
  - 💽 RAM Usage
  - 📊 Disk Usage

---

## 🙋 Support

If you face issues:
- Make sure dependencies are installed:
  ```
  pip install customtkinter psutil
  ```
- Use Python 3.10+

Happy organizing! 🛠️
