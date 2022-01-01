Arduino Code
============


There are two actionable (things that do something) member functions:
Thinkfast and Process.

Process starts something. Like a motor that is takine f_OR_  e_VER_
to make a simple 1-tick move; I can schedule myself for a re-visit
ever so often, like milliseconds -- and let the rest of the machine
do its trick. Seriously: This paradigm borrows from the old IBM channel
fast release trick.


So: Never use Thinkfast, embed those calls in Process.

#. Process is expected to take some time.
#. Thinkfast is used by Process.

Startup:

Hard conditions:
#. The SBM Instrument is programmed.
  - It will see input on the main USB interface.
  - It will offer a respone to query of a Patron called Initiate.
    . the patron responds with JSON with the layout for its widget:
      - the key is the widget type
      - the value is a dict:
         keys: name, version



#. A SBC is in charge of an interface.
#.


Open the box with the instrument, basic program in place
Create your own instrument and program the Serial Port
with the data.



The Dispatcher
--------------

We assume there is no reliable timer, and rely instead on the 
'loop' of the Arduino's main process.

We can toss in a delay of a few milliseconds. But! Some processes
need lots of time. With interrupts, we can start something and
let it mosey to a conclusion. Here we have to 'poll'. 

So, the "Thinkfast" member function comes into play. For
some things, the loop may see let a request 'play through'
the mix. For things like hitting a fast sensor; simply turning
something on/off or toggling; asking the IMU for a few register
values -- are things that take few micro-seconds. The slow
part is serializing the response. The Thinkfast also promotes
putting a response into a reply message queue ahead of other
slow processes.

So, with a loop, having a dispatcher that lets requests
or classes set a frequency to be polled is handy.

In general, each request registers with the dispatcher
for a on-time event. So a bit of this is moot. The architecture
is inexpensive.


Rambling Discussion
-------------------


In general, the vast number of Arduino programs are a "sketch"
designed to implement some simple logic, written with the IDE.

In reality the "sketch" code is C++11 with exception handling
(try/throw/catch) removed. This is reasonable, given the amount
of code-space on the Arduino families of CPUs.

We are using the Nano 33 BLE Sense, and the Seeeduino Xiao -- both ARM
core Single Board Microprocessors (SBM) machines with reasonable
memory. Goal is to use the SBMs as they come out of the box.

In order to promote good software practices, Makefiles (standard Unix make)
manages the tool-chains for the compiling and releasing the download images.

The IDE is fine for small builds, but with the amount of code the
Makefiles produce easy ways to manage any error corrections needed
during the compile stage and serve to document the compiler
instructions used for builds.

For FlexSpec1:

The goal is the architecture featuring extensibility to meet any type
of device under control of an instance of a SBM. 


Makefiles
---------

Makefile
makefile.nano

The main Makefile (note capital M) looks to environment variables
to control the builds.

HOME is the path to the basic user. We rely on the Arduino IDE build to
be in its standard place, relative to the user's home directory.

# TOOLCHAIN - where the main toolchain lives.
# USERROOT  - where the library manager will install packages.
# USERARDUINO $(HOME)/.arduino15/packages

export TOOLCHAIN=$(HOME)/Configuration/arduino-1.8.13
export USERROOT=$(HOME)/Arduino
export USERARDUINO=$(HOME)/.arduino15/packages

echo TOOLCHAIN="$TOOLCHAIN" 
echo USERROOT="$USERROOT" 
echo USERARDUINO="$USERARDUINO"

(progn
    (setenv "TOOLCHAIN"     "/home/wayne/Configuration/arduino-1.8.13"  )
    (setenv "USERROOT"      "/home/wayne/Arduino"  )
    (setenv "USERARDUINO"   "/home/wayne/.arduino15/packages"  )
)

Files
-----

These files were produced with custom emacs code to auto-generate coding
templates for .h and .cpp files. The template code has been retained.

ArduinoStub.h       -- Pile forward references here for regression testing.

FS_Blinky.cpp
FS_Blinky.h

FS_CAMLinearFocuser.h

FS_Dispatcher.cpp
FS_Dispatcher.h

FS_Event.h
FS_EventPool.h

FS_Focuser.h
FS_FullRotator.h
FS_HelicalFocuser.h

FS_Inventory.h

FS_LimitedRotator.h

FS_LinearFocuser.h

FS_Processor.h

FS_RGBlinky.h

FS_Rotator.h


FS_StepperMotor.h

FS_Switch.h
FS_TimedSwitch.h
FS_SimpleSwitch.h

FS_Timer.h

Unimplented Place Holders
-------------------------

FS_Sensor.h



Communication:

FS_SerialPort.h
FS_SerialServer.h
Message.h
MessagePool.h
Patron.h
PostMaster.h
FS_I2CPort.h
FS_IMU.h
FS_MQTT.h



Regression Handling
-------------------

At times, we use the native Linux system to do compile checks of code
that is never to run there. These files have a prefix of "Regression_".

Regression_Blinky.cpp
Regression_Patron.cpp

Pins
----

Certain things do not need a pin, such as the IMU, the build-in
LED, and RGBLED etc.


--



