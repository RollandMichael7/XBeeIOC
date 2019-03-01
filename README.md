# XBeeIOC #
An EPICS StreamDevice input-output controller for wireless XBee L/T/H sensors, using a Python TCP server. 

## Known Issues ##
- The sCalcout record will cause an error when reading the generated dbd file. To avoid this, all references to 'scalcout' (about
3 lines) must be removed from the dbd file before running the IOC. This is done by the provided install script.
- Sometimes the IOC will interpret responses incorrectly when it starts up, causing readings to be sent to the wrong PVs. If this happens, just restart the IOC.

# Requirements #
- An XBee coordinator node, either an [XStick](https://www.digi.com/products/networking/rf-adapters-modems/xstick) or [Gateway](https://www.digi.com/products/networking/gateways/xbee-gateway)
- If using an XStick:
  - Python 3
  - XBee python module: ``` pip install digi-xbee ```
- [XBee wireless sensors](https://www.digi.com/products/networking/rf-adapters-modems/xbee-sensors#overview)
- EPICS StreamDevice requirements:
  - EPICS base >R3.14.6
  - asyn >R4-3
  - stream
  
# Setup #
Follow the setup for the coordinator that you're using, either a gateway or an XStick USB adapter.

## Setting up your gateway ##

This setup assumes that you have already connected your gateway to your network and know its IP. If not, see [Digi's 
documentation](https://www.digi.com/resources/documentation/digidocs/90001399-13/Default.htm).

In order for the IOC to work, your gateway must be running a TCP server which responds to the specific commands sent to it
by the StreamDevice XBee protocol. Python files to run this server are included, however to obtain the data from the sensors your 
gateway must know the IDs of your sensors. These can be found on your gateway's web interface in the "XBee Network" section. If 
your gateway isnt connected to the sensors, click "Discover XBee Devices" and the sensors should show up with their IDs. 
Additionally, the sensors and the gateway must have matching PAN IDs which can also be configured from the XBee Network section.
Once you've connected and set up the sensors, enter their IDs in ```python/gateway/gatewayTCP.py``` in the ```sensor_addresses``` 
array, then transfer the contents of the ```python/gateway``` folder to your gateway. The server can be run either by SSHing to 
the gateway and using the command line or by setting the script to auto-run through the gateway's web interface. To run the 
server in the background from the gateway's command line, run ``` nohup python gatewayTCP.py & ```. You may then disconnect from 
the gateway and it will continue to run the server while it is powered (unless the script crashes). Note that if you set the 
script to auto-run from the gateway's web interface, you can also set the script to restart if it ever crashes.

## Setting up your XStick ##
To configure your XStick, download the [XCTU](https://www.digi.com/products/iot-platform/xctu) software from Digi. Open XCTU and 
use the discover modules tool to discover your XStick, and use the XStick panel to discover the sensors. Use the panels for each 
node to set their PAN IDs to the same value of your choosing. Also give each sensor a unique Node Identifier (NI). Enter your 
node identifiers into ```python/xstick/xstickTCP.py``` in the ```node_ids``` array, and set the port and baud rate for your 
XStick. Note that if the port file is not accessible to your account, you may need to use ```sudo``` to run the server. After 
setting these variables, the script is ready to run; the IOC will work only as long as this script is running, so keep it 
running in the background: ``` (sudo) nohup python3 xstickTCP.py & ```.

## Setting up the IOC ##
Edit XBeeApp/Db/xbee.substitutions to set the PV names, sensor numbers, and forward links. The PORT should always be 
XBEE. Each entry in this table will generate 4 PVs: 
  - ${Sys}${Dev}L
  - ${Sys}${Dev}T
  - ${Sys}${Dev}H
  - ${Sys}${Dev}ID

The XBEE port must be set to point to your gateway or the computer your XStick is connected to. Edit the following line in 
iocBoot/iocXBee/st.cmd:

```drvAsynIPPortConfigure("XBEE","{YOUR COORDINATOR IP}:12000") ```

If your XStick is connected to the same computer running the IOC, use 'localhost'. 

After setting up the port, change the scans at the bottom of st.cmd to scan the correct PV names. Modify configure/RELEASE to 
point to your EPICS base, asyn and stream installations then run ```install.sh``` to compile. Your IOC is now ready to run!
