TOP=../..

include $(TOP)/configure/CONFIG
#=============================
# Build the IOC application

PROD_IOC = XBee
# XBee.dbd will be created and installed
DBD += XBee.dbd

# XBee.dbd will be made up from these files:
XBee_DBD += base.dbd
XBee_DBD += asyn.dbd
XBee_DBD += stream.dbd
XBee_DBD += drvAsynIPPort.dbd

# XBee_registerRecordDeviceDriver.cpp derives from XBee.dbd
XBee_SRCS += XBee_registerRecordDeviceDriver.cpp

# Build the main IOC entry point on workstation OSs.
XBee_SRCS_DEFAULT += XBeeMain.cpp

# Link in the code from the support library
XBee_LIBS += asyn stream

# Finally link to the EPICS Base libraries
XBee_LIBS += $(EPICS_BASE_IOC_LIBS)

#=============================

include $(TOP)/configure/RULES
#----------------------------------------
#  ADD RULES AFTER THIS LINE

