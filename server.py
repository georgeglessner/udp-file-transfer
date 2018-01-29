'''
Reliable File Transfer using UDP
Author: George Glessner, Jacob Craffey
Python Version: 2.7
'''
# ----- receiver.py -----
#!/usr/bin/env python

from socket import *
import sys
import select

host= ''

# Obtain port address to connect to
try:
    port = int(raw_input('Please Enter Port: '))
except ValueError:
    print 'Invalid Port'
    sys.exit(0)

if (port < 1 or port > 65535):
    print 'Invalid Port'
    sys.exit(0)

    
s = socket(AF_INET,SOCK_DGRAM)
s.bind((host,port))

addr = (host,port)
buf=1024

data,addr = s.recvfrom(buf)
file_name = data.strip()
print "Received File:", file_name
try:
    f=open(file_name,"rb")
    data = f.read(buf)
    while (data):
        if(s.sendto(data,addr)):
            print "sending ..."
            data = f.read(buf)
    f.close()
except:
    print file_name + ' is not a valid file'
