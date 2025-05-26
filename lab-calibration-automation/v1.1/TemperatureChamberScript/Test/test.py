# import serial
# import csv
# import time


# #calls to function to set temp 
 
# #function takes in temperature, time an delay as arguments
# # Opens serial port

# start = ti
# ser = serial.Serial ('COM3',9600) 


# command = bytearray('\x0401v000a10\x03$', 'ascii') #uses XOR checksum sets temperature to 10
# ser.write(command)

# ser = serial.Serial ('COM14', 9600, timeout = 1)

# with open('serialnumnber_data.csv', 'a', newline='') as csvfile:
#     writer = csv.writer(csvfile) # creates writer object
#     writer.writerow(["Time", "Elpased", "RS80", "WS504", "EUT mA", "Oven T"])
#     ISOTECH_command = '\ü'
#     ser.write(ISOTECH_command)
#     isotech_data = ser.readline()
#     ISOTECH = float(isotech_data[2:8])



   
ETX = 3
EOT = 4
ENQ = 5

CommsCommand = "01M200" + chr(ENQ)

# Calculate the checksum BCC for CommsCommand
BCC = 0
for char in CommsCommand:
    BCC ^= ord(char)

# The final string comprises an <EOT> character, the command then the BCC
CommsCommand = chr(EOT) + CommsCommand + chr(BCC)
print (CommsCommand)
