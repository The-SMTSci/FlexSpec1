Remote Protocol
===============

The control structure is being developed in a platform agnostic network
neutral fashion leveraging web applications (web apps) via bokeh and
other tools.

The bokeh server is a Raspberry Pi and is be considered to be the
'main' computer, a peer in an asynchronous distributed network of
peers. Any SBC/Desktop computer with a decent operating system may be
used for the server. The ODroid, BeagleBone, Intel NUC etc. Some SBC
:index:`SBC;Configuration` configuration will be required.

Arduino class devices are designated as an SBM is a "Single Board
Microcontroller".

This approach sticks with the Arduino control system (boots out of the
box) and does not use an after-marker RTOS or PyCharm.

The essential parts:

- The actual hardware at the interface of the SBM and the real world,
  where the if/then/else/switch/maths part is next to the
  hardware. Timing may exist here.

- The logical element within the Arduino for a part: A 'StepperMotor' may
  have several ways to do things, there may be several different steppers
  in a device. Handles the commands and is a communications terminus
  or originator of status etc back to its manager.

- The Raspberry Pi/Odroid/Linux box that owns the serial wires. Actual
  wires.

- The user interface:
     - People via interaction a browser with buttons etc...
     - A controller program like a scheduler
     - (both at the same time)

One hard part is the timing required. We don't have any real sense
of a "timer". We have hacked up something to help, but that control
loop gets complicated with more than one set of things to do.



The other main division is in how messages flow.

- A message shall only be a JSON structure. The structure will be
  created by a program and therefore checked before being sent. This
  requirement removes all the checking requirements in the
  Arduino. The JSON message will be a single string of ASCII
  characters consisting divided into two classes of characters: Case
  1) special - the braces, colon, comma and double quote mark {}:,"
  Case 2) The characters A-Za-z0-9._ and noting else.

**Case 1** are filtered when messages are parsed. This makes matching the close
     brace to the open brace very small in the Arduino.
**Case 2** Means any illegal character -- that have a remote possibility
     of occurring due to a bit-flip in coms, can act as a trigger to reset.


A JSON structure is a "dictionary" (special collection or set) of a
  "key" and a "value". A key is restricted to being only a quoted
  string and a value may be one of three things: a quoted string,
  ASCII integer representation, float in the form of
  whole-dot-fraction expressed.

The Serial communications assumes more than on SBM on a wire pair. 
All listen to the wire and parse a single JSON dictionary that matches
their name. The SBM parses this dictionary and dispatches any enclosed
value JSON dictionaries to each "widget". The widget is responsible
for understanding and acting on the content of that dictionary.
A Key is considered a class of command and its values are considered
the parameters for that action.


This next part is a trick.

There will be two "mirrored" classes: Python for the Raspberry Pi
and C++ for the SBM.

The class (Python) in the Raspberry Pi has to mirror the class in the
Arduino exactly. This allows them to communicate in their own agreed
upon way to assure proper operation. This requirement alleviates
the need for a universal grammar or command set. 

The 'format' of the message will be 1) JSON BUT 2) the content is left
up to both sides of that class.  The Python will have Bokeh/GUI
stuff. The Arduino implements all the tedious logic to make things act
and/or move. The paradigm is one of a Navy Captain and the Chief of
the Boat: The Captain knows he wants to make a certain speed to
a target and no idea how that happens. He 'orders' the Chief
to make 15 knots NNE. The Cheif tells the engine room to make
a certain number of 'revolutions'.

The GUI user does not want to think in terms of stepper-motor
steps, directions. They want to move to a logical position.
The Arduino receives a JSON key/value pair that might say --
in this scenario -- { ... "speed" : "23[knots]" ... } and
parses the value as it sees fit. The units may be implicit, as
the two classes understand how that message's value needs to
be handled.

The Raspberry Pi Python class communicates with the 'user'
(person/algorithm). In this case a Python web-app built on Bokeh, or
will simply accept and pass-thru messages from an algorithm user. It
lives on a Raspberry Pi, and has lots of program space to do all the
logic and format checks to guarantee the messages sent to the SBM is
correct.  (Remember remove checks from the Arduino to the degree
possible).

The Raspberry Pi owns the serial lines: RS-232 two-wire, I2C, BLE
device.  This means Serial will be a server. It is provides one access
point to all classes/programs the electrical system. It will accept
and queue messages and route them by electrical protocol.

In the code repository the Slit may look like:

FS_Slit.h
FS_SLit.cpp
FS_SLit.py

They will have dependencies in other classes within the architecture,
to handle the Bokeh (Python) and the messaging (Python and Arduino).

Summary:
--------

The controls/sensors may be part of the Raspberry Pi itself, using a
separate RS-232/I2C/Wireless/Ethernet channel to the physical bits;
They may go through RS-232/I2C/BLE to a Arduino SBM. Tying these
together will be in Python/C++ on the Raspberry Pi. Doing the work is a
problem left somewhere else -- but required to use this communications
scheme.

Differences with ASCOM:

We do the GUI parts inside the chain, and do not rely on templates
as shims between components. This makes fast/direct coding possible.

Kzin Ring Example
-----------------

The Kzin ring example:

.. figure:: images/KzinArduinoCommand.png
   :align: left

   The Kzin ring has the ability to turn on one or more of the lamps within its purview as needed. Here NeAr, Osram (Argon only), H-Alpha (LED), O[III] (LED), Flat (Compo of lamps) and Blue (additional LEDs) may be chosen. The yellow area is a debug mode window showing the text to be sent by serial port to the registered LED.

.. code-block: none
   :linenos:

    {"Kzin": 
       {"Process": 
          {"near": 1, "osram": 0, "halpha": 1, "oiii": 0, 
           "flat": 0, "augflat": 0}
       }
    }
    
The nested-dictionary is nested inside a distribution to the "Postmaster"
that owns the spectrograph with the Kzin ring. The "Postmaster" on the
particular Arduino dispatches to an instance of a Kzin class with
the name (Kzin) the class sends the settings to to the class using
the "Process" method. The fine details of "Process" are implemented
to set the internal state and do what is necessary to conform that internal
state to the operation of that ring. In other words, if 'osram' had been on
at the time "Process" was called; it will be turned off. I 'near' was
off it is turned on -- all within the context of this one 'command' to
the Kzin ring.

The details of routing are not shown, as the Bokeh class only contributes
this message and that is the text we see.


