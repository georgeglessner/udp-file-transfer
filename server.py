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
port = int(raw_input('Please enter port: '))
if (port < 1 or port > 65535):
    print 'Invalid port'
    sys.exit(0)
    
s = socket(AF_INET,SOCK_DGRAM)
s.bind((host,port))

addr = (host,port)
buf=1024

data,addr = s.recvfrom(buf)
print "Received File:",data.strip()
f = open('client_file','wb')

data,addr = s.recvfrom(buf)
try:
    while(data):
        f.write(data)
        s.settimeout(10)
        data,addr = s.recvfrom(buf)
except timeout:
    f.close()
    s.close()
    print "File Downloaded"