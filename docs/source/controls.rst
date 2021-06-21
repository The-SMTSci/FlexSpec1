.. _fs1-ecosystem:

FlexSpec 1 Ecosystem
********************

Use Case: Develop a basic GUI to Arduino Test case that will be the 
basis for all Arduinos.

..   figure:: ./images/PiggyBackBllinky.png

     PiggyBack is the name of an Arduino, on an OTA, "piggybacked" onto
     the main spectrgraph OTA. The On/Off radio buttons originate
     a message down to the device. It advertises text in a SandStone
     coloured box, and allows a integer value to be entered for the
     Pause Rate and Cycle Count for the Blinky Object Chain.

Control Overview
----------------

The FlexSpec 1 is designed to live with other devices under the umbrella
of a main scheduler. This requires partitioning each subsystem, and its
components in a way that information can be shared at within the instrument,
between other instruments, shared resources at a site and between other
layers within a master scheduler. The architecture of FlexSpec 1 is open.

..  figure:: ./images/FlexSpec_Comm_Regional.png

    Seen from the point-of-view of the Main OTA: The Raspberry PI has three means of communication: Ethernet with the world; Serial (1.8V/Voltage management) with Arduino SBMs; I2C for short haul with SMBs and stand alone sensors. Each sub-system is managed by its own collection of C++/Python classes.

The best way to approach the control structure is to start at the distal
end of the control message chain -- the actual component being controlled.

The component is implemented using a C++ class within the arduino. There
may be a few implementations of these classes -- depending on the 
architectural type of the Arduino/other device used. C++ classes
are used, as several of the same component may appear in one FlexSpec 1
instrument. They are disambiguated using a name.

Classes consist of "data+methods". The data is always present when
included in a compiled program. However the data portion is only
created when a class is instantiated.

..  figure:: ./images/GUI_Hardware.png

    The Ethernet provides a potential connection to the world. The Browser in the world serves a HTML DIV for each of the instantiated devices, shown here with a darker green background. Here we have a power block "Blinky Power" -- with lots of switches; A LowRez configuration spectrograph with its slit positioner, its grating selector and a Calibration Lamp for NeAr.

In the figure, each "instantiated device". In the case of the Slit
Positioner "Slit LoRez" a motor, that is permitted to make full
rotations. It is controlled by an instance of a C++ class running
within its controlling Arduino. It is physically wired and resides on
a multi-drop line. The "shim" that connects this physical device to
the outside world is an instance of a Bokeh class that translates the
HTML/JSNode events from the Browser into JSON strings to be shipped to
its associated widget within one of the arduinos attached to this
system. This is a common widely used protocol -- borrowed mostly from
the Data Visualization Community. It is extremely platform independent.

You can control your system with any enabled browser, on any device,
anywhere you are allowed to go: including NASA's Deep Space Network.





a C++ class instance running on an arduino connected by a "RS-232" type interface to its controlling Arduino residing on a multi-drop 


Scenario: Consider temperature sensors.

..  code-block:: none

    The generic temperature sensor: FlexTemperature
    Data: string Name
    Methods:
      FlexTemperature() // constructor
      FlexTemperature(const string &ref)
      void status(Message<x,y> &response)
      static FlexTemperature *factory(const string &ref)
    
In general a non-initialized constructor is only supported for
development. It costs nothing in terms of the code.

The construction with initialization capability of the form
FlexTemperature(const string &ref). The string is a narrow
subset of a JSON structure. The syntax is described 
    

This spectrograph uses several small single board computers with a serial
protocol to control:

- Slit selection

- Grating selection

- Focus of the colliminating lens

- Enabling one or more calibration lamps

  - High voltage lamps require a duty cycle

 -  High intensity (boosting blue) requires short cycle times

  - Colour LEDs to support gross grating position

- A slit back-illumination lamp

- Sensors for temperature and other aspects

- Orientation for parallactic angle measurement


The control elements essentially boil down to:
 
- Motor

- Sensor

- Switch


.. _fs1-control:

Control System
--------------

The critical part of the control system is the device to be control.
The devices essentially fall into three main categories:

#. Sensor
#. Switch
#. Motor

.. _flexjson:

FlexJSON -- Narrow JSON Description
-----------------------------------

This section was created to address the use of JSON on Arduino/
C++ environments that have very limited CPUs and small memory.
The choice of the Nano BLE Sense 33 and the Xiao do not have
these restrictions.

The character set for the JSON permitted include only
Latin-7 characters; useful for encoding while preserving
some "in-band" testing.

`JSON <https://en.wikipedia.org/wiki/JSON>`_ (Javascript Object
Notation) provides a stateless, real-time peer-peer communications
protocol. It defines the "payload" of any communications wrapper.


JSON is well modeled by a Python Dictionary. A "dictionary" consists
of a Key:Value pair.  In the JSON world, a general restriction is to
have all characters within the string to be plain text (no 'binary'
characters.) Integers are represented by their textual representation,
floats etc.  A JSON value may be a string, integer, float, list or
another dictionary.  It is the nested nature of the dictionary that
supports FlexSpec interoperability.



The Arduino Nano 33 BLE Sense and IoT have sufficient capability
to support the ArduinoJson library. This is well crafted to be
memory efficient.



Motors
------

ELEGOO 5 Sets 28BYJ-48 ULN2003 5V Stepper Motor + ULN2003 Driver Board Compatible with Arduino

ULN2803 Darlington driver
