import socket
from time import sleep

TCP_IP = "10.11.1.2"
TCP_PORT = 56565

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

while True:
    # Add all file lines to an array
    mylines = []
    file = open("/sys/bus/w1/devices/28-01143d293faa/w1_slave", "r");
    for myline in file:
        mylines.append(myline)
    file.close()
    
    # Send our desired parameter, always in the second line, after the =
    lineToSend = mylines[1].split("=")[1]
    s.send(lineToSend)
    
    # Wait 5 seconds and repeat
    sleep(5)

s.close()