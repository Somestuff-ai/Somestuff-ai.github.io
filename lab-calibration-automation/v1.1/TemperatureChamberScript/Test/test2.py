import serial
import time
import csv
from datetime import datetime, timedelta


csv_file_path = "data.csv"
headers = ["Time", "Elapsed", "RS80 Temp", "WS504 Temp", "EUT mA", "Oven T"]
with open(csv_file_path, mode='a', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(headers)
step = 1

# Define serial port parameters for each device
SERIAL_PORTS = {
    1: {'port': 'COM3', 'baudrate': 9600},
    7: {'port': 'COM11', 'baudrate': 9600},
    14: {'port': 'COM14', 'baudrate': 2400}
}

# Initialize serial connections for each device
serial_connections = {} 
for device, params in SERIAL_PORTS.items():
    serial_connections[device] = serial.Serial(params['port'], params['baudrate'], timeout=1)

# Define functions for script commands

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
        


def send_command(device, command):
    # Send command over serial for specified device
    serial_connections[device].write(command.encode(encoding = "ascii"))



# Function to read response from the relevant furness comport
def fur_send_enquiry(device, reading, enquiry):
    global response
    enquiry = enquiry_check_sum(enquiry)
    ser = serial_connections[device]
    enq = bytearray(enquiry, 'ascii')
    ser.write(enq)
    res = ''
    response = ser.read_until(b'\x03')  # Read until <ETX> character (ASCII code 3) is encountered#
    res += response.decode('ascii')

    if device == 1:
        if reading == 'Temp':
            start_index = res.find('a') + 1
            end_index = res.find('b',start_index)            
    elif device == 7:
        if reading == 'Temp':
            start_index = res.find('k', res.find('Aux. Press.')) + 1
            end_index = res.find('l',start_index)
        elif reading == 'mA':
            start_index = res.find('n', res.find('EUT mA')) + 1
            end_index = res.find('o', start_index)

    substr = res[start_index:end_index]
    substr = float(substr)
    response = substr
    return response

def fur_send_command(device, command):
    command = command_check_sum(command)
    ser = serial_connections[device]
    comm  = bytearray(command, 'ascii')
    ser.write(comm)

    return


def tt10_send_enquiry():
    ser = serial_connections[device]
    enq = b'\x5c\xfc'
    ser.write(enq)

    time.sleep(1)
    response = ser.read_all()

    substr = response.decode('utf-8')
    response = substr[2:8]

    return response
    

def set_temp(temperature):
    # Send command to set temperature
    if temperature == 10:
        # command = f"\x0401v000a{temperature}\x03$"
        # send_command(1, command)
        command = f"01v000a{temperature}"
     





    
def time_to_seconds(time_str):
     # Convert time string in HH:MM:SS format to seconds
    h, m, s = map(int, time_str.split(':'))
    return h * 3600 + m * 60 + s   



def run_temperature_test(temperature, elapsed_time_check, sleep_seconds):
 
    global start_time

    fur_send_command(1, f'01v000a{temperature}')

    #set_temp(temperature)  # Temperature: 10, Elapsed time: 10 seconds, Log delay: 10 seconds
    
    start_time = datetime.now()
    elapsed_time_check_seconds = time_to_seconds(elapsed_time_check)
    while True:

        # Oven_T = fur_send_command(1,'Temp','\x0401M200\x05{' )
        Oven_T = fur_send_enquiry(1,'Temp','01M200' )
        print (Oven_T)

        # WS504_T = fur_send_enquiry(7, 'Temp', '\x0401L002\x05z')
        WS504_T = fur_send_enquiry(7, 'Temp', '01L002')
        print(WS504_T)

        # EUT_mA = fur_send_enquiry(7, 'mA','\x0401L002\x05z')
        EUT_mA = fur_send_enquiry(7, 'mA','01L002')
        print (EUT_mA)

        ISOTECH_T = tt10_send_enquiry()
        print(ISOTECH_T)

        current_time = datetime.now()
        elapsed_time = current_time - start_time
        current_time = current_time.strftime("%H:%M:%S")

        with open(csv_file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([current_time, elapsed_time, ISOTECH_T, WS504_T,EUT_mA, Oven_T])
        
        if elapsed_time >= timedelta(seconds=elapsed_time_check_seconds):
            break

        time.sleep(sleep_seconds)    

        
    end_point_20rdgs(temperature)

    return


def end_point_20rdgs(temperature):

    with open(csv_file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([])
        writer.writerow(["End Point Readings:"])

    for i in range (20):    
        ISOTECH_T = tt10_send_enquiry()
        sum_ISOTECH = sum_ISOTECH + ISOTECH_T
        
        WS504_T = fur_send_enquiry(7, 'Temp', '01L002')
        sum_WS504_T = sum_WS504_T + WS504_T


        EUT_mA = fur_send_enquiry(7, 'mA','01L002')
        sum_EUT_mA = sum_EUT_mA + EUT_mA


        Oven_T = fur_send_enquiry(1,'Temp','01M200' )
    

        current_time = datetime.now()
        elapsed_time = current_time - start_time
        current_time = current_time.strftime("%H:%M:%S")  

        with open(csv_file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([current_time, elapsed_time, ISOTECH_T, WS504_T,EUT_mA, Oven_T])  
        
  
    
    diff = round(abs( avg_ISOTECH_T - avg_WS504_T), 3)

    avg_ISOTECH_T = round(sum_ISOTECH/20, 3)
    avg_WS504_T = round(sum_WS504_T/20, 3)
    avg_EUT_mA = round(sum_EUT_mA/20, 3)

    sum_ISOTECH = 0
    sum_WS504_T = 0
    sum_EUT_mA = 0

    # store averags based on step value
    if step == 1:
        avg_ISOTECH_1 = avg_ISOTECH_T
        avg_WS504_1 = avg_WS504_T
        avg_EUT_mA_1 = avg_EUT_mA
    elif step == 2:
        avg_ISOTECH_2 = avg_ISOTECH_T
        avg_WS504_2 = avg_WS504_T
        avg_EUT_mA_2 = avg_EUT_mA  
    elif step == 3:
        avg_ISOTECH_3 = avg_ISOTECH_T
        avg_WS504_3 = avg_WS504_T
        avg_EUT_mA_3 = avg_EUT_mA
    elif step == 4:
        avg_ISOTECH_4 = avg_ISOTECH_T
        avg_WS504_4 = avg_WS504_T
        avg_EUT_mA_4 = avg_EUT_mA
        with open(csv_file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([])
            writer.writerow(["Average RS80", "Average EUTmA", "Check Difference", "Pass/Fail"]) 
            
             

    step+=1

    return      
                             
 

def main():

    run_temperature_test(10,"00:00:10", 1) # Example: Temperature: 10, Elapsed time check: 10 seconds, Sleep: 1 second
    run_temperature_test(20,"00:00:10",1 )
    


    #set_temp(20, 20, 10)  # Temperature: 20, Elapsed time: 20 seconds, Log delay: 10 seconds
   # set_temp(30, 30, 10)  # Temperature: 30, Elapsed time: 30 seconds, Log delay: 10 seconds
    #set_temp(20, 40, 10)  # Temperature: 20,


if __name__ == "__main__":
    main()
