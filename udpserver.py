#! usr/bin/env python

'''
Reliable File Transfer using UDP
Author: George Glessner, Jacob Craffey
Python Version: 2.7
'''

import socket, sys

# All available interfaces
host = ''

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
    socket.sendto(data, (host, port))

# Close connection
socket.close()
