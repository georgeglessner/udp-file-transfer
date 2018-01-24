#! usr/bin/env python

'''
Reliable File Transfer using UDP
Author: George Glessner, Jacob Craffey
Python Version: 2.7
'''

import socket, sys

# Obtain IP Address, should be local host
host = raw_input('Please enter IP Address: ')
if (host != '127.0.0.1'):
    print 'Not local host'
    sys.exit(0)

# Obtain port address to connect to
port = int(raw_input('Please enter port: '))
if (port < 1 or port > 65535):
    print 'Invalid port'

# Create socket
socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Obtain filename
filename = raw_input('Please enter a filename to transfer: ')

# Send file
socket.sendto(filename, (host, port))

# Receive data
data = socket.recvfrom(1024)

# Close socket
socket.close()

# Print received message
print 'Received ', data[0]
