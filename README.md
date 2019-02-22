# XBeeIOC #
An EPICS StreamDevice input-output controller for wireless XBee L/T/H sensors, using a Python TCP server. 

## Known Issues ##
- The sCalcout record will cause an error when reading the generated dbd file. To avoid this, all references to 'scalcout' (about
3 lines) must be removed from the dbd file before running the IOC.
- Sometimes the IOC will interpret responses incorrectly when it starts up, causing readings to be sent to the wrong PVs. If this happens, just restart the IOC.

# Requirements #
- A Digi XBee Gateway that can run Python
- XBee wireless L/T/H sensors
- EPICS StreamDevice requirements:
  - EPICS base >R.13.8.2
  - asyn >R4-3
  
# Setup #
## Setting up your gateway ##
In order for the IOC to work, your gateway must be running a TCP server which responds to the specific commands sent to it
by the StreamDevice XBee protocol. Python files to run this server are included, however to obtain the data from the sensors your 
gateway must know the IDs of your sensors. These can be found on your gateway's web interface in the "XBee Network" section. 
Enter the IDs of your sensors in gateway_python/sensorTCP.py in the 'sensor_addresses' array, then transfer the xbeelib folder 
and sensorTCP.py file to your gateway. The server can be run either by SSHing to the gateway and using the command line or by 
setting the script to auto-run through the gateway's web interface. To run the server in the background from the gateway's 
command line, run ``` nohup python sensorTCP.py & ```. You may then disconnect from the gateway and it will continue to run the 
server while it is powered (unless the script crashes). Note that if you set the script to auto-run from the gateway's web 
interface, you can also set the script to restart if it ever crashes.

## Setting up the IOC ##
Edit XBeeApp/Db/xbee.substitutions to set the PV names, sensor numbers, and forward links. The PORT should always be 
XBEE. Each entry in this table will generate 4 PVs: 
  - ${Sys}${Dev}L
  - ${Sys}${Dev}T
  - ${Sys}${Dev}H
  - ${Sys}${Dev}ID

The XBEE port must be set to point to your gateway. Edit the following line in iocBoot/iocXBee/st.cmd:

```drvAsynIPPortConfigure("XBEE","{YOUR GATEWAY IP}:12000") ```

Additionally, change the scans at the bottom of st.cmd to scan the correct PV names.

After setting up the PVs, modify configure/RELEASE to point to your EPICS base and asyn installations then run 'make' 
to compile. Your IOC is now ready to run!
