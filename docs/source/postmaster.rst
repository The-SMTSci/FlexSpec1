Postmaster
==========

There are a few paradigms of FlexSpec1.

#. A "Postmaster"/"Patron"/"Parcel" paradigm. The Bokeh server sends
   its information to the RPi PostmasterServer that acts as a
   'dispatch-server'. It adds keys to 'wrapper' a few things in a
   "Parcel" that is sent to the 'Serial' device requested by
   Bokeh. This parcel is unwrapped and routines are dispatched to C++
   classes within the Arduino.

#. The "matched class" paradigm -- a python class maintains variables related to a
   widget, that are encapsulated within a json string and sent to the Arduino (other)
   for processing. It contains the name of the device, the name of the widget in the
   device and a set of key/value pairs to be mirrored and acted upon by the "matched"
   C++ class in the Arduino.

#. JSON is used in a pure ASCII form. Numbers are strings, that are converted by
   the C++ mechanism within the Arduino. This avoids any Big/Little Endian issues
   and allows a simple terminal for monitoring the exchanges.

#. Error handling means a) someone cares, b) something meaningful may be done, and
   c) the error may be communicated. To get around this, add error checking is
   done by Bokeh at that end -- and we ASSUME, you know what that means, all
   input is legal.

The form is::

    { "DeviceName" : 
       { "Target C++  Widget" : 
          { "Process" : {"key" : "value", ... , "key" : "value" }}
          { "Report" : "1" }
       }
    }

Here The receiving serial port checks that it is within a device "DeviceName".
The "Target C++  Widget" is mapped to a Patron pointer. If the name is invalid,
the map returns a null and the packed is silently dropped. The dispatcher
validates the "command" (Process in this example) is a valid virtual member
of the Patron class - and that "value" which is a simple JSON string of
key/values for the member variables for that class are accepted and acted
upon.

For example for an IMU, the request might read "IMU" : {"x" : "1", "y" : "1", "z" : "1"}.
The dispatcher verifies that IMU exists, the Process() function reads the port,
sets internal variables. A second "Report" ... is requested, and the process
unwinds to send a message back to the Bokeh class making the request. 

Returning values update the Bokeh widget. In the case of the "Grating", the
wavelength may not be precise, as the motor has finite steps that may not
fall exactly where requested. The "Grating" class computes the CWAVE it
can achieve, reports back; the Bohek class updates the browser with the achieved
value.


