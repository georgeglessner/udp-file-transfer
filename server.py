'''
Reliable File Transfer using UDP
Author: George Glessner, Jacob Craffey
Python Version: 2.7
'''
# ----- server.py -----
#!/usr/bin/env python

from socket import *
import sys
import select
import os
import math

host = ''

# Obtain port address to connect to
try:
    port = int(raw_input('Please Enter Port: '))
except ValueError:
    print 'Invalid Port'
    sys.exit(0)

if(port < 1 or port > 65535):
    print 'Invalid Port'
    sys.exit(0)


s = socket(AF_INET, SOCK_DGRAM)
s.bind((host, port))

addr = (host, port)
buf = 1024

data, addr = s.recvfrom(buf)
file_name = data.strip()
print "Received File:", file_name

f = open(file_name, "rb")
packet_size = 64
packet_id = 0
packet_list = []
file_size = os.path.getsize(file_name)
num_packets = math.ceil(float(file_size) / float(packet_size))
WINDOW_LENGTH = 5

print num_packets
with open(file_name, 'r') as newFile:

    if num_packets > WINDOW_LENGTH:
        # create header info
        for i in range(WINDOW_LENGTH):
            data = newFile.read(packet_size)
            data = str(packet_id) + '|' + data
            packet_list.append(data)
            packet_id += 1

        # send packet
        for packet in packet_list:
            print "Sending packet"
            s.sendto(str(packet), addr)

        while 1:
            # receive ack
            ack, addr = s.recvfrom(buf)
            print "Received acknowledgement"

            # in order
            if (ack != 0):
                packet_list.pop()

                data = newFile.read(packet_size)
                data = str(packet_id) + '|' + data
                packet_list.append(data)
                packet_id += 1

                # last packet
                if packet_id == num_packets:
                    print "Sending last packet"
                    data = data.split('|', 1)
                    last_data = '99999' + '|' + data[1]
                    s.sendto(str(last_data), addr)

                    break

                # send packet
                packet_sending = data.split('|', 1)
                print "Sending packet", packet_sending[0]
                s.sendto(str(data), addr)

            # error
            elif (ack == 0 and packet_id > 4):
                print "Received error"

    else:
        for i in range(int(num_packets)):
            data = newFile.read(packet_size)
            data = str(packet_id) + '|' + data
            packet_list.append(data)
            packet_id += 1

        # send packet
        for packet in packet_list:
            print "Sending packet"
            s.sendto(str(packet), addr)

        # TODO: Fix for small file sizes, ends up in infinite loop
        while 1:
            # receive ack
            ack, addr = s.recvfrom(buf)
            print "Received acknowledgement"

            # in order
            if (ack != 0):
                packet_list.pop()

                data = newFile.read(packet_size)
                data = str(packet_id) + '|' + data
                packet_list.append(data)
                packet_id += 1

                # last packet
                if packet_id == num_packets:
                    print "Sending last packet"
                    data = data.split('|', 1)
                    last_data = '99999' + '|' + data[1]
                    s.sendto(str(last_data), addr)
                    break
s.close()


# TODO: wait for acknowledgements


f.close()
