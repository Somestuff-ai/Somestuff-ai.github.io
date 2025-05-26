from initialise import serial_connections
from CS043_Click import take_cs043_reading
import time
import csv
from datetime import datetime, timedelta
import serial
import customtkinter as ctk

csv_file_path = ""
avg_ISOTECH_T = []
avg_WS504_T = []
avg_EUT_Ohm = []
diff = []
condition = []

start_time = datetime.now()

# Define functions for script commands

def run_temperature_test(temperature, elapsed_time_check, sleep_seconds):
    global start_time
    global step

    generate_csv_headers()

    try:
        venus_send_command(temperature)
    except Exception as e:
        print(f"Error: Failed to send command to Venus device: {e}")
        return
    
    
    elapsed_time_check_seconds = time_to_seconds(elapsed_time_check)
    while True:

        WS504_T = fur_send_enquiry(3, 'Temp', '01L002')
        print(WS504_T)

        EUT_Ohm = agilent_send_enquiry()
        if response is None:
            print ("failed to get a valid response from instrument check serial connection")
        print (EUT_Ohm)

        ISOTECH_T = tt10_send_enquiry()
        print(ISOTECH_T)

        current_time = datetime.now()
        elapsed_time = current_time - start_time
        current_time = current_time.strftime("%H:%M:%S")

        with open(csv_file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([current_time, elapsed_time, ISOTECH_T, WS504_T,EUT_Ohm])
        
        if elapsed_time >= timedelta(seconds=elapsed_time_check_seconds):
            break

        time.sleep(sleep_seconds)    

    take_cs043_reading()
    print("calling 20 point readings")
    time.sleep(1)
    end_point_20rdgs(temperature)
    
    return

def time_to_seconds(time_str):
     # Convert time string in HH:MM:SS format to seconds
    h, m, s = map(int, time_str.split(':'))
    return h * 3600 + m * 60 + s   


def end_point_20rdgs(temperature):
    global avg_ISOTECH_T, avg_WS504_T, avg_EUT_mA, diff, condition
    sum_ISOTECH_T = 0
    sum_WS504_T = 0
    sum_EUT_Ohm = 0
    
    print("Starting 20 point Readings")

    with open(csv_file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([])
        writer.writerow(["End Point Readings:"])

    for i in range (20):    
        ISOTECH_T = float(tt10_send_enquiry())
        sum_ISOTECH = sum_ISOTECH + ISOTECH_T
        print (sum_ISOTECH)
        
        WS504_T = float(fur_send_enquiry(3, 'Temp', '01L002'))
        sum_WS504_T = sum_WS504_T + WS504_T
        print (sum_WS504_T)

        EUT_Ohm = agilent_send_enquiry()
        sum_EUT_Ohm = sum_EUT_Ohm + EUT_Ohm
        print (sum_EUT_Ohm)


        current_time = datetime.now()
        elapsed_time = current_time - start_time
        current_time = current_time.strftime("%H:%M:%S")  

        with open(csv_file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([current_time, elapsed_time, ISOTECH_T, WS504_T,EUT_Ohm])  
     

    avg_ISOTECH_T_value = round(sum_ISOTECH_T / 20, 3)
    print (avg_ISOTECH_T_value)

    avg_WS504_T_value = round(sum_WS504_T / 20, 3)
    print(avg_WS504_T_value)

    avg_EUT_Ohm_value = round(sum_EUT_Ohm/20, 3)
    print (avg_EUT_Ohm_value)

    diff_value = round(abs( avg_ISOTECH_T_value - avg_WS504_T_value), 3)
    print(diff_value)

    if diff_value > 0.1:
        condition_value = "Fail"
    else:
        condition_value = "Pass"

    # Append averages, differences, and conditions to lists
    avg_ISOTECH_T.append(avg_ISOTECH_T_value)
    avg_WS504_T.append(avg_WS504_T_value)
    avg_EUT_Ohm.append(avg_EUT_Ohm_value)
    diff.append(diff_value)
    condition.append(condition_value)

    # Return data collected in this function call, if needed
    return




#BCC Check Sum Calculations
def command_check_sum(command):
    ETX = 3
    EOT = 4

    CommsCommand = command + chr(ETX)

    # Calculate the checksum BCC for CommsCommand
    BCC = 0
    for char in CommsCommand:
        BCC ^= ord(char)

    # The final string comprises an <EOT> character, the command then the BCC
    CommsCommand = chr(EOT) + CommsCommand + chr(BCC)
    return CommsCommand
   

def enquiry_check_sum(enquiry):
    ENQ = 5
    EOT = 4

    CommsEnquiry = enquiry + chr(ENQ)

    # Calculate the checksum BCC for CommsCommand
    BCC = 0
    for char in CommsEnquiry:
        BCC ^= ord(char)

    # The final string comprises an <EOT> character, the command then the BCC
    CommsEnquiry = chr(EOT) + CommsEnquiry + chr(BCC)
    return CommsEnquiry
        

# Functions to send enquiries and read responses 
def fur_send_enquiry(device, reading, enquiry):
    global response
    enquiry = enquiry_check_sum(enquiry)
    ser = serial_connections[device]
    if not ser.is_open:
        ser.open()
    enq = bytearray(enquiry, 'ascii')
    ser.write(enq)
    res = ''
    response = ser.read_until(b'\x03')  # Read until <ETX> character (ASCII code 3) is encountered#
    res += response.decode('ascii')

    if device == 1:
        if reading == 'Temp':
            start_index = res.rfind('a') + 1
            end_index = res.find('b',start_index)            
    elif device == 3:
        if reading == 'Temp':
            start_index = res.find('k', res.find('Aux. Press.')) + 1
            end_index = res.find('l',start_index)
        elif reading == 'mA':
            start_index = res.find('n', res.find('EUT mA')) + 1
            end_index = res.find('o', start_index)

    substr = res[start_index:end_index]
    substr = float(substr)
    response = substr

    ser.close()

    return response

def tt10_send_enquiry():
    ser = serial_connections[14] 
    enq = b'\x5c\xfc'
    if not ser.is_open:
        ser.open()

    ser.write(enq)

    time.sleep(1)
    response = ser.read_all()

    substr = response.decode('utf-8')
    response = substr[2:8]

    ser.close()

    return response

def venus_send_command(temperature):

    if temperature == 0:
        ser = serial_connections[2]
        command = b'\x01\x10\x80\x04\x00\x02\x04\x00\x00\x00\x00\x93\x9A'# Command for 0°C set point
        if not ser.is_open:
            ser.open()

        ser.write(command)


        ser.close()        

    elif temperature == 10:
        ser = serial_connections[2]
        command = b'\x01\x10\x80\x04\x00\x02\x04\x41\x20\x00\x00\x86\x6C' # Command for 10°C set point
        if not ser.is_open:
            ser.open()

        ser.write(command)


        ser.close()

    elif temperature == 20:
        ser = serial_connections[2]
        command = b'\x01\x10\x80\x04\x00\x02\x04\x41\xA0\x00\x00\x87\x84' #Command for 20°C set point
        if not ser.is_open:
            ser.open()

        ser.write(command)


        ser.close()

    elif temperature == 35:
        ser = serial_connections[2]
        command = b'\x01\x10\x80\x04\x00\x02\x04\x42\x0C\x00\x00\x47\xE1' #Command for 35°C set point
        if not ser.is_open:
            ser.open()

        ser.write(command)


        ser.close()    

    elif temperature == 50:
        ser = serial_connections[2]
        command = b'\x01\x10\x80\x04\x00\x02\x04\x42\x48\x00\x00\x07\xF4' #Command for 50°C set point
        if not ser.is_open:
            ser.open()

        ser.write(command)


        ser.close()  

def agilent_send_enquiry():
    ser = serial_connections[7]
    commands = [
    b'SYST:REMOTE\r\n',
    b'*CLS\r\n',
    b'func "FRES"\r\n',
    b'conf:FRES DEF,DEF\r\n',
    b'READ?\r\n'
] 
    try:
        if not ser.is_open:
            ser.open()

        for command in commands:
            ser.write(command)
            time.sleep(1)

        ser.timeout = 1.0
        response_str = ''
        while True:
            
            response_bytes = ser.read(1000)
            response_str = response_bytes.decode().strip()

            if response_str:  # Continue only if response is not empty
                try:
                    response = float(response_str)
                    break  # Break the loop if a valid numeric response is received
                except ValueError:
                    print(f"Error: Received a non-numeric response: {response_str}")
                    response_str = ''  # Reset response_str to continue the loop
            else:
                print("Error: Received an empty or invalid response")
                response_str = ''  # Reset response_str to continue the loop

    except serial.SerialException as e:
        print(f"Serial communication error: {e}")
        response = None

    finally:
        if ser.is_open:
            ser.close()

    return response



 
# Functions to send commands
def fur_send_command(device, command):
    command = command_check_sum(command)
    ser = serial_connections[device]
    if not ser.is_open:
        ser.open()

    comm  = bytearray(command, 'ascii')
    ser.write(comm)

    ser.close()

    return




def set_csv_file_path(path):
    global csv_file_path
    csv_file_path = path

def generate_csv_headers():
    headers = ["Time", "Elapsed", "RS80 Temp", "WS504 Temp", "EUT Ohm"]
    with open(csv_file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([])
        writer.writerow(headers)

def output_avgs():
    global avg_ISOTECH_T, avg_WS504_T, avg_EUT_Ohm, diff, condition

    try:
        with open(csv_file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([])
            writer.writerow(["Average RS80 Temp", "Average WS504 Temp", "Average EUT Ohm", "Check Difference", "Pass/Fail"])

            # Iterate through stored averages, differences, and conditions
            for i in range(len(avg_ISOTECH_T)):
                try:
                    writer.writerow([avg_ISOTECH_T[i], avg_WS504_T[i], avg_EUT_Ohm[i], diff[i], condition[i]])
                except Exception as e:
                    print(f"Error writing row {i}: {e}")
                    return

    except Exception as e:
        print(f"Error opening/writing to file: {e}")
        return



    avg_dialogue = ctk.CTk()
    avg_dialogue.title("Averages and Pass/Fail")
    avg_dialogue.geometry("600x400")

    # Create a frame to hold the table
    table_frame = ctk.CTkFrame(avg_dialogue)
    table_frame.pack(expand=True, fill='both', padx=10, pady=10)

    headers = ["Average ISOTECH Temp", "Average WS504 Temp", "Average EUT Ohm", "Check Difference", "Pass/Fail"]

    # Create header row
    for col, header in enumerate(headers):
        header_label = ctk.CTkLabel(table_frame, text=header)
        header_label.grid(row=0, column=col, sticky='nsew', padx=1, pady=1)

    # Create data rows
    for row in range(len(avg_ISOTECH_T)):
        avg_values = [avg_ISOTECH_T[row], avg_WS504_T[row], avg_EUT_Ohm[row], diff[row], condition[row]]
        for col, value in enumerate(avg_values):
            cell_label = ctk.CTkLabel(table_frame, text=str(value))
            cell_label.grid(row=row + 1, column=col, sticky='nsew', padx=1, pady=1)

    # Configure column weights
    for col in range(len(headers)):
        table_frame.grid_columnconfigure(col, weight=1)

    # Configure row weights
    for row in range(len(avg_ISOTECH_T) + 1):
        table_frame.grid_rowconfigure(row, weight=1)

    avg_dialogue.mainloop()