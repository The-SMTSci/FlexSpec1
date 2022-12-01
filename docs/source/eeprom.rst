EEPROM
======


The FS1 uses an 24FC256 I2C EEPROM module to store information. The module
is at I2C J11 and uses processor Pins 24 for SCL and 25 for SDA on Pin 25.
Its official address is 0x50. 

The EEPROM only supports 

We are using the AMC256 prom with ..math`256\times 1024 = 262144` bits
for 32768 bytes or ..math`32 \times 1024` pages.

We have less than 32 thingys to manage, so we allocate room for a JSON
string that is 1024 bytes long that mimics the process command for each main class.

The Flex_EEPROM module implements a simple load-leveling key/value system.
The key is the device name (user/system defined) and the value is a simple
ASCII only JSON string as sent to the device using the Patron Process
command, with RRR = No. The values are obtained by the Patron's Report
process.

https://ww1.microchip.com/downloads/aemDocuments/documents/MPD/ProductDocuments/DataSheets/24AA256-24LC256-24FC256-256-Kbit-I2C-Serial-EEPROM-20001203X.pdf

.. code-block:: python

    # Example of a pythonic image for the EEPROM. The placement depends
    # on the "flexspec" "toc" entry.
    eepromdefs = {"eeprom" : {"process" :
    {"flexspec" : {
        "owner"           : "indef",
        "contact"         : "indef",
        "serialno"        : "indef",
        "coderevision"    : "indef",
        "installdate"     : "indef",
        "updatedate"      : "indef",
        "toc"             : {
            "flexspec"        : "(0    ,1024)"
            "guidecamera"     : "(1024 ,1024)"
            "slit"            : "(2048 ,1024)"
            "fraunhofer"      : "(3072 ,1024)"
            "grating"         : "(4096 ,1024)"
            "camera"          : "(5120 ,1024)"
        }
    },
    "guidecamera" : {
        "vendor"          : "indef",
        "serialumber"     : "indef",
        "pixelsize"       : "indef",
        "lens1"           : "indef",
        "lens2"           : "indef",
        "ccdsum"          : "(1,1)",
        "slotoffset"      : "indef",
    },
    "slit" : {
        "vendor"          : "ovio",
        "serialno"        : "indef",
        "widthmicrons"    : "indef",
    },
    "fraunhofer" : {
        "baffleheight"    : "indef",
        "bafflewidth"     : "indef",
        "baffleoffset"    : "indef"
    },
    "grating" : {
        "name"            : "Thorlabs_500_600_25_0",
        "vendor"          : "Thorlabs",
        "catalogid"       : "GR25-0605",
        "length"          : "25.0",
        "height"          : "25.0",
        "thickness"       : "6.0",
        "lmm"             : "600",
        "cwave"           : "500",
        "blaze"           : "8.617",
        "dispersion"      : "1.65",
        "tcoeff"          : "8.0",
        "home"            : "indef",
        "offset"          : "indef",
        "other"           : "indef",
    },
    "camera" : {
        "vendor"          : "indef",
        "serialno"        : "indef",
        "pixelsize"       : "indef",
        "backfocus"       : "indef",
        "ccdsum"          : "(1,1)"
        "lensdesc"        : "indef",
        "lensaperture"    : "indef",
        "lensfl"          : "indef",
        "lensaperture"    : "indef",
        "tempsetting"     : "indef"
    }
    }
    }
    }
    

The FS1 has classes for various independent components. Some classes
are placeholders -- like the slit. Some refer to relativly inert elements
like the fraunhofer baffle. In roughly optical-axis order:

    #. flexspec - the details about the spectrograph itself. The "toc" (table of contents) lists starting offset and length for the 'page' by name. Accessing the structure by name allows the Postmaster to dispatch the initialization to each device's instance.

    #. guidecamera - important details known to the spectrograph to help inform the guide software (E.g.: Phd2)

    #. slit - Currently not selectable, establish on the bench. This will be an active class in future.
    #. fraunhofer - the geometry of the slit.

    #. grating - the details of the grating currently being used.

    #. camera - while controlled by other software (E.g.: libindi), the 'camera' (objective) lens, its backfocus, aperture, focal length do inform focus. At some point we hope to motorize this aspect.

The rest of the entries are self-explanatory. 

EEPROM Layout
-------------

The number of write cycles are important. We see the EEProm being used on a very 
infrequent basis. It will be consulted on each powerup/reboot of the Arduino.
The values are placed at locations within the EEPROM.



If page write is available use the beginTransmission(), ... write() ...
and endTransmission() calls. In our case, from 1 to 64 bytes may be written.



https://www.arduino.cc/reference/en/language/functions/communication/wire/begintransmission/


..
