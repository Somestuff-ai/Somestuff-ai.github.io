#Initialise comports and assigns them device numbers 
import serial

# Define serial port parameters for each device
serial_connections = {}


# Initialize serial connections for each device

def set_serial_ports(serial_ports):
    global serial_connections
    for device, params in serial_ports.items():
        try:
            serial_connections[int(device)] = serial.Serial(params['port'], params['baudrate'], timeout=1)
        except serial.SerialException as e:
            print(f"Error: Could not open serial port {params['port']} for device {device}: {e}")