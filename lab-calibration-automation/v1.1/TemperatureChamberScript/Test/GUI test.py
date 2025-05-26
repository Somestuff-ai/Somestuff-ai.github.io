import customtkinter as ctk
import subprocess
from tkinter import filedialog

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

# Function to run the main script with the selected config file and csv file path
def run_script():
    # adding script paths 
    
    # setup_selected = setup_var.get()
    # config_selected = config_var.get()

    # # if setup_selected == "setup_560":
    # #     script_path = 


    config_file = config_var.get()
    csv_path = csv_file_path.get()
    command = ["python", "main.py", config_file, csv_path]
    subprocess.run(command)

# Function to handle setup selection
def select_setup():
    if setup_var.get() == "setup_0_50":
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

# Create setup 0-50 radio button
setup_frame = ctk.CTkFrame(app)
setup_frame.pack(pady=10)

setup_label = ctk.CTkLabel(setup_frame, text="Select setup:")
setup_label.pack(pady=5)

setup_0_50_rb = ctk.CTkRadioButton(setup_frame, text="setup 0-50", variable=setup_var, value="setup_0_50", command=select_setup)
setup_0_50_rb.pack(pady=5)

# Create Config File Selection radio buttons
config_frame = ctk.CTkFrame(app)
config_label = ctk.CTkLabel(config_frame, text="Select Config File:")

config_files = ["Block 0 to 50.json"]  # Example config files
for config in config_files:
    config_rb = ctk.CTkRadioButton(config_frame, text=config, variable=config_var, value=config, command=select_config)
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