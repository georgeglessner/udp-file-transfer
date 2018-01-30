'''
Reliable File Transfer using UDP
Author: George Glessner, Jacob Craffey
Python Version: 2.7
'''
# ----- client.py ------

#!/usr/bin/env python

from socket import *
import sys
import os

s = socket(AF_INET, SOCK_DGRAM)

# Obtain IP Address, should be local host
host = raw_input('Please enter IP Address: ')
if (host != '127.0.0.1'):
    print 'Not local host'
    sys.exit(0)

# Obtain port address to connect to
try:
    port = int(raw_input('Please Enter Port: '))
except ValueError:
    print 'Invalid Port'
    sys.exit(0)

if (port < 1 or port > 65535):
    print 'Invalid Port'
    sys.exit(0)

buf = 1000
addr = (host, port)

# Obtain filename
file_name = raw_input('Please enter a filename to transfer: ')
if not os.path.exists('./' + str(file_name)):
    print "Invalid file"
    sys.exit(0)

# send file request to server
s.sendto(file_name, addr)
packetList = []

while 1:
    # receive data from server
    packetData, addr = s.recvfrom(buf)
    header = packetData.split('|', 1)
    packetList.append(header[1])

    # send ack to server
    s.sendto(str(header[0]), addr)
    if header[0] == '99999':
        print "Sending last ACK"
    else:
        print "Sending ACK for packet ", header[0]

    # last packet
    if header[0] == '99999':
        break

fileStr = ''
for packet in packetList:
    fileStr += packet
f = open('client_file', "wb")
f.write(fileStr)
print "File complete"


s.close()
