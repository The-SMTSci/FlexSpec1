EEPROM
======


The FS1 uses an 24FC256 I2C EEPROM module to store information. The module
is at I2C J11 and uses processor Pins 24 for SCL and 25 for SDA on Pin 25.

The Flex_EEPROM module implements a simple load-leveling key/value system.
The key is the device name (user/system defined) and the value is a simple
ASCII only JSON string as sent to the device using the Patron Process
command, with RRR = No. The values are obtained by the Patron's Report
process.

https://ww1.microchip.com/downloads/aemDocuments/documents/MPD/ProductDocuments/DataSheets/24AA256-24LC256-24FC256-256-Kbit-I2C-Serial-EEPROM-20001203X.pdf
