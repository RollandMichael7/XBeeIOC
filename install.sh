#!/bin/bash

# compile and remove sCalcout records that IOC doesnt like
make
chmod +w dbd/XBee.dbd
sed -i '/recordtype(scalcout)/,+1d' dbd/XBee.dbd
sed -i '/scalcout/d' dbd/XBee.dbd
chmod -w dbd/XBee.dbd
