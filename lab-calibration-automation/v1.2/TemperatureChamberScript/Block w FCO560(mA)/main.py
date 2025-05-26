#main function to start temperature calibration using Oven, Oven Controller, FCO56 and WS504

import sys
import json
from functions import run_temperature_test, output_avgs, set_csv_file_path
from initialise import set_serial_ports

def main():
    if len(sys.argv) != 3:
        print("Usage: python main.py <config_file> <csv_file_path>")
        sys.exit(1)

    config_file = sys.argv[1]
    csv_file_path = sys.argv[2]

    # Set the CSV file path
    set_csv_file_path(csv_file_path)

    # Read the config file
    try:
        with open(config_file, 'r') as f:
            config_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Config file '{config_file}' not found.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Failed to decode JSON from '{config_file}': {e}")
        sys.exit(1)


    #Set the serial ports configuration
    try:
        set_serial_ports(config_data['serial_ports'])
    except Exception as e:
        print(f"Error: Failed to set serial ports: {e}")
        sys.exit(1)


    # Run temperature tests based on config data
    for test in config_data['tests']:
        try:
            run_temperature_test(test['temperature'], test['time_elapsed'], test['sleep_time'])
        except Exception as e:
            print(f"Error: Failed to run temperature test: {e}")
            continue
        
    output_avgs()

if __name__ == "__main__":
    main()