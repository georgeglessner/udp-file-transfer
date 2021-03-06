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


def start():
    '''
    Connect to socket, ask for file
    '''
    global s

    # Obtain IP Address, should be local host
    host = raw_input('Please enter IP Address: ')
    # local loopback, mininet servers
    if not (host == '127.0.0.1' or host == '10.0.0.1' or host == '10.0.0.2'):
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

    addr = (host, port)

    # Obtain filename
    file_name = raw_input('Please enter a filename to transfer: ')
    if not os.path.exists('./' + str(file_name)):
        print 'Invalid file'
        sys.exit(0)

    # send file request to server
    s.sendto(file_name, addr)
    receive()


def receive():
    '''
    Receeive packets from server, send acknowledgements
    '''
    global s

    packetList = []
    WINDOW_LENGTH = 5
    LPR = 0  # Last packet Received
    LAP = 5  # Largest acceptable packet
    packet_id = 1
    ack_needed = 0
    acks_sent = []

    while 1:
        buf = 1024

        # receive data from server
        packetData, addr = s.recvfrom(buf)
        header = packetData.split('|', 1)
        # resend ack received
        if 'RESEND' in header[0]:
            header[0] = header[0][6:]
            packet_id = int(header[0])
            ack_needed = packet_id

        else:
            packet_id = int(header[0])

        # if packet_id is in window
        if LPR <= packet_id and packet_id <= LAP:
            # if packet is the ack needed
            if packet_id == ack_needed:
                # send ack to server
                LPR = int(packet_id)
                LAP = LPR + WINDOW_LENGTH
                # check to see if pack is in ack_sent list
                if packet_id not in acks_sent:
                    print 'Sending ACK for packet ', packet_id
                    s.sendto(str(packet_id), addr)
                    packetList.append(header[1])
                    acks_sent.append(packet_id)
                else:
                    s.sendto(str(packet_id), addr)

        # last packet
        if header[0] == '99999':
            packetList.append(header[1])
            print 'Sending last ACK'
            s.sendto(str(header[0]), addr)
            fileStr = ''
            for packet in packetList:
                fileStr += packet
            f = open('client_file', 'wb')
            f.write(fileStr)
            break

    # write to client_file
    fileStr = ''
    for packet in packetList:
        fileStr += packet
    f = open('client_file', 'wb')
    f.write(fileStr)
    print 'File complete'
    s.close()


if __name__ == '__main__':
    start()
