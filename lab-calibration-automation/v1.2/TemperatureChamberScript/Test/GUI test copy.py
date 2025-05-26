import os
import subprocess
import tkinter.filedialog as filedialog
import customtkinter as ctk
import glob
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# Define the base directory
base_dir = "TemperatureChamberScript"

# Function to find config files
def find_config_files():
    # try:
    #     config_files = glob.glob(os.path.join(base_dir, "**", "*.json"), recursive=True)
    #     return config_files
    # except Exception as e:
    #     logging.error(f"Error finding config files: {e}")
    #     return []    
    try:
        search_pattern = os.path.join(base_dir, "**", "*.json")
        logging.info(f"Searching for config files with pattern: {search_pattern}")
        
        config_files = glob.glob(search_pattern, recursive=True)
        
        logging.info(f"Found config files: {config_files}")
        
        return config_files
    except Exception as e:
        logging.error(f"Error finding config files: {e}")
        return []

# Debug: Print the base directory and check if it exists
print(f"Base directory: {base_dir}")
print(f"Absolute base directory: {os.path.abspath(base_dir)}")
print(f"Base directory contents: {os.listdir(base_dir) if os.path.exists(base_dir) else 'Directory does not exist'}")

# Find config files and print them
config_files = find_config_files()
print(f"Config files found: {config_files}")

# Function to run the appropriate script based on the selected setup and config file
def run_script():
    setup_selected = setup_var.get()
    config_selected = config_var.get()

    if setup_selected == "setup_560":
        # Find the script in the Temperature Chamber Script folder
        script_path = glob.glob(os.path.join(base_dir, "**", "Oven w FCO560 and Agilent DMM", "main.py"), recursive=True)
        if script_path:
            script_path = script_path[0]  # Take the first match if there are multiple
    else:
        # Default script for other setups and config files
        script_path = "main.py"

    command = ["python", script_path, config_selected, csv_file_path.get()]
    subprocess.run(command)

# Function to handle setup selection
def select_setup():
    if setup_var.get() == "setup_0_50":
        config_label.pack(pady=10)
        config_frame.pack(pady=10)
    elif setup_var.get() == "setup_560":
        config_label.pack(pady=10)
        config_frame.pack(pady=10)
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

# Initialize the main window
app = ctk.CTk()
app.title("Temperature Calibration")
app.geometry("400x400")

# Variables to store radio button states
setup_var = ctk.StringVar(value="")  # Empty default value
config_var = ctk.StringVar(value="")  # Empty default value
csv_file_path = ctk.StringVar(value="")  # Empty default value

# Function to check if all conditions are met to enable the Run button
def check_conditions():
    if setup_var.get() and config_var.get() and csv_file_path.get():
        run_button.configure(state="normal")
    else:
        run_button.configure(state="disabled")

# Create setup 0-50 radio button
setup_frame = ctk.CTkFrame(app)
setup_frame.pack(pady=10)

setup_label = ctk.CTkLabel(setup_frame, text="Select setup:")
setup_label.pack(pady=5)

setup_0_50_rb = ctk.CTkRadioButton(setup_frame, text="setup 0-50", variable=setup_var, value="setup_0_50", command=select_setup)
setup_0_50_rb.pack(pady=5)

# Create setup 560 radio button
setup_560_rb = ctk.CTkRadioButton(setup_frame, text="setup 560", variable=setup_var, value="setup_560", command=select_setup)
setup_560_rb.pack(pady=5)

# Create Config File Selection radio buttons
config_frame = ctk.CTkFrame(app)
config_label = ctk.CTkLabel(config_frame, text="Select Config File:")

config_files = find_config_files()  # Find config files dynamically
for config in config_files:
    config_rb = ctk.CTkRadioButton(config_frame, text=os.path.basename(config), variable=config_var, value=config, command=select_config)
    config_rb.pack(pady=5)

# Create entry for CSV file name and button to open file dialog
csv_frame = ctk.CTkFrame(app)
csv_frame.pack(pady=10)

csv_label = ctk.CTkLabel(csv_frame, text="CSV File Name:")
csv_label.pack(pady=5)

csv_entry = ctk.CTkEntry(csv_frame, textvariable=csv_file_path)
csv_entry.pack(pady=5)

csv_button = ctk.CTkButton(csv_frame, text="Select Save Location", command=select_csv_location)
csv_button.pack(pady=5)

# Create Run button (initially disabled)
run_button = ctk.CTkButton(app, text="Run", state="disabled", command=run_script)
run_button.pack(pady=20)

# Run the main event loop
app.mainloop()