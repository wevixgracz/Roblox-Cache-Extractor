import os
import shutil
import tkinter as tk
from tkinter import filedialog

def get_user_directory():
    return os.path.join(os.path.expanduser("~"), "AppData\\Local\\Temp\\Roblox\\http")

def process_files(source_dir, destination_dir):
    for filename in os.listdir(source_dir):
        if filename.endswith(".ogg") or filename.endswith(".png"):
            continue
        file_path = os.path.join(source_dir, filename)
        with open(file_path, 'rb') as file:
            content = file.read()
            oggs_index = content.find(b'OggS')
            png_index = content.find(b'\x89PNG')
            if oggs_index != -1:
                content = content[oggs_index:]
                new_filename = os.path.splitext(filename)[0] + ".ogg"
            elif png_index != -1:
                content = content[png_index:]
                new_filename = os.path.splitext(filename)[0] + ".png"
            else:
                continue
        with open(os.path.join(destination_dir, new_filename), 'wb') as new_file:
            new_file.write(content)

def clear_source_dir(source_dir):
    for filename in os.listdir(source_dir):
        file_path = os.path.join(source_dir, filename)
        os.remove(file_path)

def execute_script():
    source_dir = get_user_directory()
    destination_dir = destination_dir_entry.get()
    process_files(source_dir, destination_dir)
    clear_source_dir(source_dir)

def browse_destination_dir():
    destination_dir = filedialog.askdirectory()
    destination_dir_entry.delete(0, tk.END)
    destination_dir_entry.insert(0, destination_dir)

root = tk.Tk()
root.title("Roblox Cache Extractor")

source_dir_label = tk.Label(root, text="Source Directory:")
source_dir_label.grid(row=0, column=0, padx=5, pady=5)
source_dir_entry = tk.Entry(root, width=50)
source_dir_entry.grid(row=0, column=1, padx=5, pady=5)
source_dir_entry.insert(0, get_user_directory())

destination_dir_label = tk.Label(root, text="Destination Directory:")
destination_dir_label.grid(row=1, column=0, padx=5, pady=5)
destination_dir_entry = tk.Entry(root, width=50)
destination_dir_entry.grid(row=1, column=1, padx=5, pady=5)
destination_dir_button = tk.Button(root, text="Browse", command=browse_destination_dir)
destination_dir_button.grid(row=1, column=2, padx=5, pady=5)

execute_button = tk.Button(root, text="Execute", command=execute_script)
execute_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

clear_button = tk.Button(root, text="Clear Source Directory", command=lambda: clear_source_dir(get_user_directory()))
clear_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

root.mainloop()