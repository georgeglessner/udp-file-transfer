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
from time import sleep

s = socket(AF_INET, SOCK_DGRAM)


def start():
    '''
    Bind to socket
    '''
    global s
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

    s.bind((host, port))
    addr = (host, port)
    send()

def send():
    '''
    Send packets to client, receive acknowledgements
    '''
    global s
    buf = 1024

    data, addr = s.recvfrom(buf)
    file_name = data.strip()
    print 'Received File:', file_name

    f = open(file_name, 'rb')
    packet_size = 1000
    packet_id = 1
    packet_list = []
    acked_packs = 0
    file_size = os.path.getsize(file_name)
    num_packets = math.ceil(float(file_size) / float(packet_size))
    WINDOW_LENGTH = 5
    LAR = 0 # Last ack received
    LPS = 0 # Last packet sent

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
                LPS = int(packet.split('|',1)[0])
                print 'Sending packet'
                s.sendto(str(packet), addr)
                sleep(.1)


            s.settimeout(.2)
            while 1: 
                while 1:
                    try:
                        # receive ack
                        ack, addr = s.recvfrom(buf)
                        if (int(ack) == (LAR+1)):
                            print 'Received acknowledgement', ack
                            acked_packs += 1
                            LAR = int(ack)
                            break
                    except KeyboardInterrupt:
                        print 'Cancel'
                        sys.exit(-1)
                    except timeout:
                        print 'resending', LAR + 1
                        if packet_list[0][0] == 'R':
                            s.sendto(str(packet_list[0]), addr) 
                            sleep(.1)
                        else:
                            packet_list[0] = 'RESEND' + packet_list[0]
                            s.sendto(str(packet_list[0]), addr) 
                            sleep(.1)

                # in order
                if (LPS - LAR <= WINDOW_LENGTH): # (ack != 0)
                    packet_list.pop(0)
                    data = newFile.read(packet_size)
                    data = str(packet_id) + '|' + data
                    packet_list.append(data)
                    packet_id += 1

                    # last packet
                    if(acked_packs == num_packets):
                        print 'Sending last packet'
                        data = data.split('|', 1)
                        last_data = '99999' + '|' + data[1]
                        s.sendto(str(last_data), addr)
                        break

                    # send packet
                    packet_sending = data.split('|', 1)
                    print 'Sending packet'
                    s.sendto(str(data), addr)
                    sleep(.1)

                # error
                elif (ack == 0 and packet_id > 4):
                    print 'Received error'

        elif num_packets == 1:
            # only one packet
            data = newFile.read(packet_size)
            data = '99999' + '|' + data
            print 'Sending packet'
            s.sendto(str(data), addr)
            ack, addr = s.recvfrom(buf)
            print 'Received acknowledgement'
            sys.exit(0)

        else:
            # 2-4 packets
            for i in range(int(num_packets)):
                data = newFile.read(packet_size)
                data = str(packet_id) + '|' + data
                packet_list.append(data)
                packet_id += 1

            # send packet
            for packet in packet_list:
                LPS = int(packet.split('|',1)[0])
                print 'Sending packet'
                s.sendto(str(packet), addr)

            # loop to receive ack and send packets
            while 1:
                # receive ack
                ack, addr = s.recvfrom(buf)
                print 'Received acknowledgement'
                LAR = int(ack)

                # in order
                if (LPS - LAR <= WINDOW_LENGTH):
                    packet_list.pop()
                    data = newFile.read(packet_size)
                    data = str(packet_id) + '|' + data
                    packet_list.append(data)
                    packet_id += 1

                    # last packet
                    if packet_id == num_packets:
                        print 'Sending last packet'
                        data = data.split('|', 1)
                        last_data = '99999' + '|' + data[1]
                        s.sendto(str(last_data), addr)
                        break
    s.close()
    f.close()


if __name__ == '__main__':
    start()
