import serial
from datetime import datetime, timedelta
import time
from initialise import csv_file_path, serial_connections, device

# char = "\ü"
# hex_representation = char.encode("utf-8").hex()
# print(hex_representation)

# serial_command = "^A^P€^D^@^B^D^@^@^@^@“š"
# hex_bytes = bytes(serial_command.encode('utf-8'))

# print(hex_bytes.hex())


step = 5
def venus_send_command():

    if step == 1:
        ser = serial_connections[2]
        command = b'\x01\x10\x80\x04\x00\x02\x04\x00\x00\x00\x00\x93\x9A'# Command for 0°C set point
        if not ser.is_open:
            ser.open()

        ser.write(command)


        ser.close()        

    elif step == 2:
        ser = serial_connections[2]
        command = b'\x01\x10\x80\x04\x00\x02\x04\x41\x20\x00\x00\x86\x6C' # Command for 10°C set point
        if not ser.is_open:
            ser.open()

        ser.write(command)


        ser.close()

    elif step == 3:
        ser = serial_connections[2]
        command = b'\x01\x10\x80\x04\x00\x02\x04\x41\xA0\x00\x00\x87\x84' #Command for 20°C set point
        if not ser.is_open:
            ser.open()

        ser.write(command)


        ser.close()

    elif step == 4:
        ser = serial_connections[2]
        command = b'\x01\x10\x80\x04\x00\x02\x04\x42\x0C\x00\x00\x47\xE1' #Command for 35°C set point
        if not ser.is_open:
            ser.open()

        ser.write(command)


        ser.close()    

    elif step == 5:
        ser = serial_connections[2]
        command = b'\x01\x10\x80\x04\x00\x02\x04\x42\x48\x00\x00\x07\xF4' #Command for 50°C set point
        if not ser.is_open:
            ser.open()

        ser.write(command)


        ser.close()  

    elif step == 6:
        ser = serial_connections[2]
        command = b'\x01\x10\x80\x04\x00\x02\x04\x41\xA0\x00\x00\x87\x84' #Command for 50°C set point
        if not ser.is_open:
            ser.open()

        ser.write(command)


        ser.close()        


venus_send_command()



def agilent_send_enquiry():

    ser = serial_connections[device]

    commands = [
    b'SYST:REMOTE\r\n',
    b'*CLS\r\n',
    b'func "FRES"\r\n',
    b'conf:FRES DEF,DEF\r\n',
    b'READ?\r\n'
] 
    for command in commands:
        ser.write(command)  

    time.sleep(1)  

    response = ser.read(1000)

    ser.close()






    # def get_user_inputs():
#     root = tk.Tk()
#     root.withdraw()  # Hide the main window

#     inputs = []
#     for i in range(1,4):
#         temperature = simpledialog.askinteger("Input", f"Enter temperature for measurement {i}:")
#         time_elapsed = simpledialog.askstring("Input", f"Enter time elapsed for measurement {i} (HH:MM:SS format):")
#         sleep_time = simpledialog.askinteger("Input", f"Enter sleep time for measurement {i} (in seconds):")
#         inputs.append((temperature, time_elapsed, sleep_time))

#     return inputs