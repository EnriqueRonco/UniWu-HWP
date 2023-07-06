from encodings import utf_8
import socket
import os
from datetime import datetime
import time

TCP_IP = "0.0.0.0"
TCP_PORT = 56565
BUFFER_SIZE = 1024
DATAPATH = "data/" # Where to store CSV files
CSV_HEADER = "Date,Temperature\n" # Header for the CSV files

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

conn, addr = s.accept()
while True:
    data = conn.recv(BUFFER_SIZE)
    if not data: break
    filename = datetime.today().strftime('%Y%m%d') # Filename for today's server date
    filepath = DATAPATH + filename + ".csv" # Entire filepath

    # If the file doesn't exist yet, create a new one for today with the CSV header
    if not os.path.exists(filepath):
        file = open(filepath, "w")
        file.write(CSV_HEADER)
        file.close()

    # Actual Epoch time    
    now = str(round(time.time()))

    # Data bytes decoded to UTF-8
    stringToWrite = now + ", " + data.decode('utf-8')

    # Append data to today's file
    file = open(filepath, 'a')
    file.write(stringToWrite)
    file.close()

conn.close()
