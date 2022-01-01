/******************************************************************************
* FS_Initiator
*   {"" : "FS_Initiator"}
{"channel":"/dev/AMT0"}   # return reciept
{"host":"hostname"}       # return reciept
{"":""}

FS_LinearFocuser.h
FS_Processor.h
FS_Timer.h

The main program:

FS_Dispatcher.h           -- Widget can schedule a revisit.

FS_Event.h                -- Implemententation details in Arduino
FS_EventPool.h
Message.h
MessagePool.h

Patron.h                  -- define a 'Patron'
PostMaster.h              -- Manage messages between 'Patrons' via channels

FS_SerialServer.h         -- ?

FS_SerialPort.h
FS_I2CPort.h              -- Manage a 'channel'
FS_BLEPort                -- Manage a 'BLE' channel
FS_Socket                 -- Manage a socket
FS_MQTT.h                 -- A way to send a message somewhere


--- Patron subclass management:

Patron.h                  -- define virtual interface/ common data

    FS_StepperMotor.h         -- stuff to control a stepper motor
    
    FS_CAMLinearFocuser.h     -- The colliminator focuser, steps:degrees
    
    FS_Focuser.h              -- Main Scope      microns
       FS_HelicalFocuser.h       -- Guider  home, rotations, fraction of rotation
    
    FS_Rotator.h              -- Slit
       FS_FullRotator.h          -- Rotates 360     steps:degrees
       FS_LimitedRotator.h       -- Rotates in range Grating 
    
    FS_IMU.h                  -- Parallactic Angle
    FS_Inventory.h            -- User stff
    
    FS_Blinky.h               -- Visual at instrument
    FS_RGBlinky.h             -- Visual at instrument
    
    FS_SimpleSwitch.h         -- LED, SlitIlluminator
    FS_Switch.h               -- Slit Illuminator with a timeout.
    FS_TimedSwitch.h          -- Slit Illuminator with a timeout.
    
    FS_Sensor.h               -- Define things from a sensor



******************************************************************************/
//(class-insert)
/* *INDENT-OFF* */
#if 0

(Classdef "FS_Initiator"
  "Put a string together to allow a blank-bokeh server to create an interface."


   (variable (access private) (attributes dialog encapsulate persistent stream)
    ("" (
       (""   "" )
    )))


   (variable (access private) (attributes dialog encapsulate persistent stream)
    ("" (
       (""   "" )
    )))


   (variable (access private) (attributes dialog encapsulate persistent stream)
    ("" (
       (""   "" )
    )))


   (header      t)     ; nil for second/subsequent class insertions.
   ;(equality    t)     ; operator != ==
   ;(comparison  t)     ; operator > >= < <= 
   ;(arithmetic  t)     ; operators + - * /
   ;(destructor  t)     ; ~X 
   ;(freepool    t)     ; Manage used objects from a pool.
   ;(iterator    t)     ; Add X<TTT> conainer operations.
   (debug       t)     ; Stuff to assist with debuging.
   ;(dialog      t)     ; Will this class use a dialog to manage members?
   ;(assignment  t)     ; operator =
   (memberwise  t)     ; X::X() : v(), v() ...
   (encapsulate t)     ; Get/Set routines for variables
   (friendio    t)     ; friend [io]stream &operator [<<,>>]
   (persistence t)     ; (Un)Marshall routines.
   (cpp         FS_Initiator)   ; nil or name xxx of xxx.cpp. (cpp xxx).
   ;(html        nil)   ; Generate a documentation .html file if possible.

   ;(man         nil)   ; Generate a documentation .html file if possible.



   (interface (access public) ; (attributes virtual pure)
      (
         (""  ""   "()"   "")
      )
   )



)
#endif
/*  *INDENT-ON*  */
