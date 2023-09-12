Stellarmate on RPi
==================

The Flexspec leverages a Raspberry Pi 4B 4GB memory for its operation.
We do not recommend VNC connections as they are un-necessary and take
a lot of bandwidth to support -- particularly in shared remote observatory
settings. The RPi's Raspbian/Debian operating system fully supports X11.
Win1x boxes may run the Xming program as a XServer (client and server
terms are reversed in X11). 



Service           Port           WAN/Internet Control
SSH               5624           Required for Flexspec
INDI Web Manager  8624           Not required
INDI Server       7624           Not required
EkosLive Server   3000           Not required

Web VNC           6080           Not required
VNC               5900           Not required

Serial            /dev/ttyn      Arduino Serial1 pins on RPi
Serial            /dev/ttyADM0   Arduino Serial USB


The FlexSpec uses a 5 wire bundle to supply power, ground, 
RX, TX and a hard reset signal to the Arduino. The software
looks for commands on Serial1 and may supplies optional 
status information on the USB Serial interface. This requirements
off-loads traffic from and frees for use one USB port.

Of the USB Ports:

   # Science camera
   # Guide Camera
   # Optional wide field "finder camera", otherwise not required.
   # Optional Serial1 interface, otherwise not required.

Feathering the Nest
-------------------

The following packages may be loaded:
sudo apt-get install x11-utils            # xeyes for testing X
sudo apt install iraf                     # focus, analysis
sudo apt install pyraf3
sudo apt install locate                   # fast find of files.
