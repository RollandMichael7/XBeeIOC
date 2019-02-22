#!../../bin/linux-x86_64/XBee

## Location of stream protocol files
epicsEnvSet("ENGINEER",  "kgofron x5283")
epicsEnvSet("LOCATION", "740 BM6")

#epicsEnvSet("EPICS_CA_AUTO_ADDR_LIST", "NO")
#epicsEnvSet("EPICS_CA_ADDR_LIST", "10.6.0.255")

< envPaths

epicsEnvSet("STREAM_PROTOCOL_PATH", "$(TOP)/protocol")

## Register all support components
dbLoadDatabase "$(TOP)/dbd/XBee.dbd"
XBee_registerRecordDeviceDriver pdbbase

# Configure serial port for Rex-F9000 controller
drvAsynIPPortConfigure("XBEE","10.10.192.18:12000")

## Load record instances
dbLoadRecords "$(TOP)/db/asynRecord.db"
dbLoadRecords "$(TOP)/db/xbee.db"

iocInit
dbpf("XF:10IDB{XBEE:001}ID.SCAN","1 second")
dbpf("XF:10IDB{XBEE:001}L.SCAN", "1 second")
dbpf("XF:10IDB{XBEE:001}T.SCAN", "1 second")
dbpf("XF:10IDB{XBEE:001}H.SCAN", "1 second")

