'''
Reliable File Transfer using UDP
Author: George Glessner, Jacob Craffey
Python Version: 2.7
'''
# ----- sender.py ------

#!/usr/bin/env python

from socket import *
import sys

s = socket(AF_INET,SOCK_DGRAM)

# Obtain IP Address, should be local host
host = raw_input('Please enter IP Address: ')
if (host != '127.0.0.1'):
    print 'Not local host'
    sys.exit(0)

# Obtain port address to connect to
port = int(raw_input('Please enter port: '))
if (port < 1 or port > 65535):
    print 'Invalid port'
    sys.exit(0)

buf =1024
addr = (host,port)

# Obtain filename
file_name = raw_input('Please enter a filename to transfer: ')

s.sendto(file_name,addr)

f=open(file_name,"rb")
data = f.read(buf)
while (data):
    if(s.sendto(data,addr)):
        print "sending ..."
        data = f.read(buf)
s.close()
f.close()