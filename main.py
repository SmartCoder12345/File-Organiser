"""
Author: #Smart_Coder
--> File Organiser
"""

import customtkinter as ctk
import os
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox

# Set appearance mode to dark and default color theme to dark-blue
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

def add_label_in_frame(frame: ctk.CTkScrollableFrame, text: str) -> None:
    """
    Add a label in a frame with a given text.
    :param frame: Scrollable Frame
    :param text: Text to be displayed in the label.
    :return: None
    """
    label = ctk.CTkLabel(frame, text=text, font=("Helvetica", 20), wraplength=550)
    label.pack(pady=5)

def clear_clutter(folder_path: str, frame: ctk.CTkScrollableFrame) -> None:
    """
    Clear clutter from a folder.
    :param folder_path: Path of the Folder
    :param frame: A Scrollable Frame
    :return: None
    """
    sure = messagebox.askyesno("File Organiser", f"Are you sure that You want to Organiser this folder {folder_path}")

    if not sure:
        return None

    add_label_in_frame(frame, "Starting Declutter Process...")
    add_label_in_frame(frame, f"Folder Path: {folder_path}")

    # Get a list of all files in the folder
    folder_content = os.listdir(folder_path)

    add_label_in_frame(frame, f"Folder Content: {folder_content}")

    add_label_in_frame(frame, "Identifying extensions...")
    file_extensions = set()

    for file in folder_content:
        if os.path.isfile(os.path.join(folder_path, file)):
            _, extension = os.path.splitext(file)
            file_extensions.add(extension)

    add_label_in_frame(frame, f"File Extensions Identified !!")
    add_label_in_frame(frame, f"File Extensions: {file_extensions}")

    add_label_in_frame(frame, f"Renaming files based on their extensions...")
    # Rename files based on their extensions
    for ext in file_extensions:
        i = 0
        for file in folder_content:
            if file.endswith(ext):
                i += 1
                new_name = f"{i}{ext}"
                os.rename(os.path.join(folder_path, file), os.path.join(folder_path, new_name))
                add_label_in_frame(frame, f"{file} is renamed to {new_name}.")

    add_label_in_frame(frame, f"Files Renamed !!")
    add_label_in_frame(frame, "Process Completed !!")

def check_if_folder(folder_path: str) -> bool:
    """
    Checks if the given folder path is a valid folder.
    :param folder_path: Path of the Folder.
    :return: True if the folder exists, False otherwise.
    """

    return os.path.isdir(folder_path)

def check_folder_periodically(entry, start_declutter_button):
    """
    Periodically checks if the folder exists and enables/disables the start declutter button accordingly.
    """
    if check_if_folder(entry.get()):
        start_declutter_button.configure(state="normal")
    else:
        start_declutter_button.configure(state="disabled")
    # Schedule the function to run again after 5 seconds (adjust the interval as needed)
    entry.after(500, check_folder_periodically, entry, start_declutter_button)


def main() -> None:
    """
    This is the main function of this Program.
    :return: It returns None.
    """
    # Create the main window
    root = ctk.CTk()
    root.title("File Organiser")
    root.geometry("650x420")
    root.resizable(False, False)
    root.iconbitmap("asset/icon.ico")

    label = ctk.CTkLabel(root, text="Your Folder Path:", font=("Arial", 20))
    label.grid(row=0, column=0, pady=20, padx=10)

    entry = ctk.CTkEntry(root, width=300, font=("Arial", 20))
    entry.grid(row=0, column=1)

    add_path_button = ctk.CTkButton(root, text="Add Folder Path", command=lambda: entry.insert(0, filedialog.askdirectory()), font=("Arial", 15))
    add_path_button.grid(row=0, column=2, padx=15)

    frame = ctk.CTkScrollableFrame(root, width=600, height=250)

    start_declutter_button = ctk.CTkButton(root, text="Start Declutter", command=lambda: clear_clutter(entry.get(), frame), font=("Arial", 15), state="disabled")
    start_declutter_button.grid(row=1, column=0, pady=10)

    frame.grid(row=2, column=0, columnspan=3, padx=10, pady=20)

    # Start checking the folder periodically after the mainloop has started
    check_folder_periodically(entry, start_declutter_button)

    # Start the main loop
    root.mainloop()

if __name__ == '__main__':
    main()