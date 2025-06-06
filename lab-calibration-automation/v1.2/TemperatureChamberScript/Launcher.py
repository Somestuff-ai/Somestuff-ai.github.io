import os
import subprocess
import tkinter.filedialog as filedialog
import customtkinter as ctk
import glob
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to find the base directory
def find_base_dir():
    current_dir = os.getcwd()  # Get the current working directory
    while current_dir != '/':   # Iterate until reaching the root directory
        if 'TemperatureChamberScript' in os.listdir(current_dir):
            return os.path.abspath(current_dir)
        current_dir = os.path.dirname(current_dir)  # Move up one directory level
    return None  # Return None if the base directory is not found

# Function to find config files
def find_config_files(base_dir):
    try:
        search_pattern = os.path.join(base_dir, "**", "*.json")
        logging.info(f"Searching for config files with pattern: {search_pattern}")
        
        config_files = glob.glob(search_pattern, recursive=True)
        
        logging.info(f"Found config files: {config_files}")
        
        return config_files
    except Exception as e:
        logging.error(f"Error finding config files: {e}")
        return []

# Function to run the appropriate script based on the selected setup and config file
def run_script():
    setup_selected = setup_var.get()
    config_selected = config_var.get()
    script_path = ""

    if setup_selected == "setup_Block_560(mA)":
        script_path = glob.glob(os.path.join(base_dir.get(), "**", "Block w FCO560(mA)", "main.py"), recursive=True)
    elif setup_selected == "setup_Oven_560(mA)":
        script_path = glob.glob(os.path.join(base_dir.get(), "**", "Oven w FCO560(mA)", "main.py"), recursive=True)
    elif setup_selected == "setup_Block_560_Agilent(mA)":
        script_path = glob.glob(os.path.join(base_dir.get(), "**", "Block w FCO560 and Agilent DMM(mA)", "main.py"), recursive=True)
    elif setup_selected == "setup_Block_560_Agilent(Ω)":
        script_path = glob.glob(os.path.join(base_dir.get(), "**", "Block w FCO560 and Agilent DMM(Ω)", "main.py"), recursive=True)
    elif setup_selected == "setup_Oven_560_Agilent(mA)":
        script_path = glob.glob(os.path.join(base_dir.get(), "**", "Oven w FCO560 and Agilent DMM(mA)", "main.py"), recursive=True)
    elif setup_selected == "setup_Oven_560_Agilent(Ω)":
        script_path = glob.glob(os.path.join(base_dir.get(), "**", "Oven w FCO560 and Agilent DMM(Ω)", "main.py"), recursive=True)
    
    if script_path:
        script_path = script_path[0]  # Take the first match if there are multiple
        command = ["python", script_path, config_selected, csv_file_path.get()]
        logging.info(f"Running script with command: {command}")
        subprocess.run(command)
    else:
        logging.error("Script path not found for the selected setup.")

# Function to handle setup selection
def select_setup():
    refresh_config_files()
    check_conditions()

# Function to handle config file selection
def select_config():
    check_conditions()

# Function to open a file dialog to select the save location
def select_csv_location():
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if file_path:
        csv_file_path.set(file_path)
    check_conditions()

# Function to refresh config files based on the selected base directory
def refresh_config_files():
    for widget in config_frame.winfo_children():
        widget.destroy()
    
    # Add subheading for Temperature Profile
    profile_label = ctk.CTkLabel(config_frame, text="Temperature Profile:", font=("Arial", 12, "bold"))
    profile_label.pack(pady=5)
    
    config_files = find_config_files(base_dir.get())
    for config in config_files:
        config_name = os.path.basename(config).replace(".json", "")
        config_rb = ctk.CTkRadioButton(config_frame, text=config_name, variable=config_var, value=config, command=select_config)
        config_rb.pack(pady=5, anchor="w")
    
    check_conditions()

# Initialize the main window
app = ctk.CTk()
app.title("Temperature Calibration v1.2")
app.geometry("400x600")  # Set fixed dimensions
app.resizable(False, False)  # Disable window resizing

# Variables to store radio button states
setup_var = ctk.StringVar(value="")  # Empty default value
config_var = ctk.StringVar(value="")  # Empty default value
csv_file_path = ctk.StringVar(value="")  # Empty default value
base_dir = ctk.StringVar(value=find_base_dir() or "")  # Automatically find base directory

# Create Run button (initially disabled)
run_button = ctk.CTkButton(app, text="Run", state="disabled", command=run_script)
run_button.pack(pady=20)

# Function to check if all conditions are met to enable the Run button
def check_conditions():
    if setup_var.get() and config_var.get() and csv_file_path.get() and base_dir.get():
        run_button.configure(state="normal")
    else:
        run_button.configure(state="disabled")

# Create Block w 560 radio button
setup_frame = ctk.CTkFrame(app)
setup_frame.pack(pady=10)

setup_label = ctk.CTkLabel(setup_frame, text="Select setup:")
setup_label.pack(pady=5)

setup_Block_560_mA_rb = ctk.CTkRadioButton(setup_frame, text="Block + FCO560(mA)", variable=setup_var, value="setup_Block_560(mA)", command=select_setup)
setup_Block_560_mA_rb.pack(pady=5, anchor="w")

# Create Block w 560 and Agilent (mA) button
setup_Block_560_Agil_mA_rb = ctk.CTkRadioButton(setup_frame, text="Block + Agilent(mA)", variable=setup_var, value="setup_Block_560_Agilent(mA)", command=select_setup)
setup_Block_560_Agil_mA_rb.pack(pady=5, anchor="w")

# Create Block w 560 and Agilent (Ohm) button
setup_Block_560_Agil_Ohm_rb = ctk.CTkRadioButton(setup_frame, text="Block + Agilent(Ω)", variable=setup_var, value="setup_Block_560_Agilent(Ω)", command=select_setup)
setup_Block_560_Agil_Ohm_rb.pack(pady=5, anchor="w")

# Create Oven w 560(mA) radio button
setup_Oven_560_mA_rb = ctk.CTkRadioButton(setup_frame, text="Oven + FCO560(mA)", variable=setup_var, value="setup_Oven_560(mA)", command=select_setup)
setup_Oven_560_mA_rb.pack(pady=5, anchor="w")

# Create Oven w 560 and Agilent (mA) button
setup_Oven_560_Agil_mA_rb = ctk.CTkRadioButton(setup_frame, text="Oven + Agilent(mA)", variable=setup_var, value="setup_Oven_560_Agilent(mA)", command=select_setup)
setup_Oven_560_Agil_mA_rb.pack(pady=5, anchor="w")

# Create Oven w 560 and Agilent (Ohm) button
setup_Oven_560_Agil_Ohm_rb = ctk.CTkRadioButton(setup_frame, text="Oven + Agilent(Ω)", variable=setup_var, value="setup_Oven_560_Agilent(Ω)", command=select_setup)
setup_Oven_560_Agil_Ohm_rb.pack(pady=5, anchor="w")

# Create Config File Selection radio buttons
config_frame = ctk.CTkFrame(app)
config_label = ctk.CTkLabel(config_frame, text="Select Config File:")
config_label.pack(pady=10)
config_frame.pack(pady=10)

refresh_config_files()  # Initial configuration file listing

# Create entry for CSV file name and button to open file dialog
csv_frame = ctk.CTkFrame(app)
csv_frame.pack(pady=10)

csv_label = ctk.CTkLabel(csv_frame, text="CSV File Name:")
csv_label.pack(pady=5)

csv_entry = ctk.CTkEntry(csv_frame, textvariable=csv_file_path)
csv_entry.pack(pady=5)

csv_button = ctk.CTkButton(csv_frame, text="Select Save Location", command=select_csv_location)
csv_button.pack(pady=5)

# Run the main event loop
app.mainloop()
