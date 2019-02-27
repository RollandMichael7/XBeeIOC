############################################################################
#                                                                          #
# Copyright (c)2009, Digi International (Digi). All Rights Reserved.       #
#                                                                          #
# Permission to use, copy, modify, and distribute this software and its    #
# documentation, without fee and without a signed licensing agreement, is  #
# hereby granted, provided that the software is used on Digi products only #
# and that the software contain this copyright notice,  and the following  #
# two paragraphs appear in all copies, modifications, and distributions as #
# well. Contact Product Management, Digi International, Inc., 11001 Bren   #
# Road East, Minnetonka, MN, +1 952-912-3444, for commercial licensing     #
# opportunities for non-Digi products.                                     #
#                                                                          #
# DIGI SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT LIMITED   #
# TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A          #
# PARTICULAR PURPOSE. THE SOFTWARE AND ACCOMPANYING DOCUMENTATION, IF ANY, #
# PROVIDED HEREUNDER IS PROVIDED "AS IS" AND WITHOUT WARRANTY OF ANY KIND. #
# DIGI HAS NO OBLIGATION TO PROVIDE MAINTENANCE, SUPPORT, UPDATES,         #
# ENHANCEMENTS, OR MODIFICATIONS.                                          #
#                                                                          #
# IN NO EVENT SHALL DIGI BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT,      #
# SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING LOST PROFITS,   #
# ARISING OUT OF THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF   #
# DIGI HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.                #
#                                                                          #
############################################################################

"""\
    
    XBee server for sending L/T/H sensor data over TCP connection when requested
    
"""

import sys, os 
import time
from socket import *

import xbeelib.xbeelt

# Create sensor objects
sensor_addresses = ["[00:13:a2:00:41:63:87:88]!",
                    "[00:13:a2:00:41:4f:ad:92]!",
                    "[00:13:a2:00:41:4f:ad:97]!"]
sensors = [xbeelib.xbeelt.XBeeLTN(addr) for addr in sensor_addresses]

# Setup socket
host = ''
port = 12000
TCPSock = socket(AF_INET, SOCK_STREAM)
TCPSock.bind((host, port))

connected = False
while True:
    if not connected:
        TCPSock.listen(1)
        conn, addr = TCPSock.accept()
        #print('Connected to ' + str(addr))
        connected = True
    try:
        # wait for someone to request data
        data = conn.recv(1024)
        data = data.decode('utf-8')
        #print('Received ' + data)
    except error:
        #print "Error Occured."
        break

    # if we receive nothing, terminate the connection
    if data == "":
            #print('Disconnecting from ' + str(addr))
            connected = False
            conn.close()
    elif len(data) > 1:
        getID = False
        if data[:2] == "ID":
            getID = True

        # check for bad requests
        try:
            if getID:
                sensorNum = int(data[2:])
            else:
                sensorNum = int(data[1:])
        except (ValueError, IndexError):
            continue 
        if sensorNum >= len(sensors):
            continue   

        # Get only the requested data     
        dataType = data[0]
        sendData = '*'
        if getID:
            sendData = sensor_addresses[sensorNum]
        elif dataType == 'L':
            sendData = sensors[sensorNum].sample()['light']
        elif dataType == 'T':
            sendData = sensors[sensorNum].sample()['temperature']
        elif dataType == 'H':
            sendData = sensors[sensorNum].sample()['humidity']

        # send data if it was a valid request
        if sendData != '*':
            try:
                # add terminators so StreamDevice understands us
                conn.sendall(str(sendData) + "\r\n")
            except error:
                # broken pipe; break connection
                #print("Broken pipe; disconnecting from " + str(addr))
                connected = False
                conn.close()