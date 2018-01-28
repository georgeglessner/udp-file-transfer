#! usr/bin/env python

'''
Reliable File Transfer using UDP
Author: George Glessner, Jacob Craffey
Python Version: 2.7
'''

import socket, sys
import os

# All available interfaces
host = ''
buffer = 1024

# Obtain port address to connect to
port = int(raw_input('Please enter port: '))
if (port < 1 or port > 65535):
    print 'Invalid port'
    sys.exit(0)

# Create socket
socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind to socket
socket.bind((host, port))

# Listen to port
while 1:
    data, (host, port) = socket.recvfrom(1024)
    print 'Received', data
    if not data:
        break

    # Checks if file exists in current directory
    if os.path.isfile(data):
        print 'File exists'
        f = open(data, "r")
        data = f.read(buffer)
        if socket.sendto(data, (host, port)):
            print "sending..."
            data = f.read(buffer)
        f.close()
    else:
        data = 'File not found'
        print data


    # Send data back to client
    
# Close connection
socket.close()
