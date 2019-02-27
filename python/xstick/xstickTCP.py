import time
from digi.xbee.devices import XBeeDevice
from digi.xbee.io import IOLine, IOMode
from socket import *

lightADC = IOLine.DIO1_AD1
tempADC = IOLine.DIO2_AD2
humidityADC = IOLine.DIO3_AD3

# IMPORTANT: Set these to the port that
# your coordinator is connected to and
# its baud rate.
port = "/dev/ttyUSB0"
baud = 9600

# IMPORTANT: Set these to the Node Identifiers (NI)
# for your remote sensors. The NI can be set
# with Digi's XCTU application.
node_ids = ["SENSE1", "SENSE2", "SENSE3"]

local_device = XBeeDevice(port, baud)
local_device.open()

# Obtain the remote XBee device from the XBee network.
net = local_device.get_network()
sensors = [net.discover_device(node) for node in node_ids]

# Set up TCP socket
host = ''
port = 12000
TCPSock = socket(AF_INET, SOCK_STREAM)
TCPSock.bind((host, port))
connected = False
while True:
    if not connected:
        #print("Waiting for a connection...")
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
        #print("Error Occured.")
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
            sendData = node_ids[sensorNum]
        elif dataType == 'L':
            raw_light = sensors[sensorNum].get_adc_value(lightADC)
            sendData = (raw_light / 1023) * 1200
        elif dataType == 'T':
            raw_temp = sensors[sensorNum].get_adc_value(tempADC)
            mVanalog = (raw_temp / 1023) * 1200
            sendData = (mVanalog - 500) / 10
        elif dataType == 'H':
            raw_humidity = sensors[sensorNum].get_adc_value(humidityADC)
            mVanalog = (raw_humidity / 1023) * 1200
            sendData = (((mVanalog * 108.2 / 33.2) / 5000 - .16) / .0062)

        # send data if it was a valid request
        if sendData != '*':
            try:
                # add terminators so StreamDevice understands us
                sendData = str(sendData) + "\r\n"
                conn.sendall(sendData.encode())
            except error:
                # broken pipe; break connection
                #print("Broken pipe; disconnecting from " + str(addr))
                connected = False
                conn.close()
