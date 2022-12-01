MERLIN GCODE Tricks
===================


GCode "Gerber" code is widely used in Computer Numerical Code (CNC) machining.
Most 3D printers us Merlin's implementation. Full documentation is elsewhere.

Here are a few practical tips:

We use `Octoprint <https://octoprint.org/>`_ to interface the printer
to the recommended Raspberry Pi 3B, 3B+ or 4B computer. This is a
35USD simple solution, web based and easy to use. This is all open-source
code.

Make sure to enable autoscroll on the terminal.

The basics of GCode include a "letter" command and parameters.
Comments are enclosed in parenthesis (this is a comment).

OctoPrint and slicer programs allow users to create *scripts* to prepend
or append to the produced gcodes. Octoprint allows additinal scripts
(or the only ones) to be stored within the Octoprint computer. This
allows fine-tuning of gcode output to fit genaral or specific (one time)
needs.

Hand gcode scripts include one to make a small side print prior to
starting (test feed, bed adhesion); to raise/move the print head/bed
after the print -- etc.


M503 - dump the salient printer internal values. A screen dump from
OctoPrint via the Terminal tab::

    Send: M503
    Recv: echo:Steps per unit:
    Recv: echo:  M92 X81.00 Y81.00 Z400.50 E94.30
    Recv: echo:Maximum feedrates (mm/s):
    Recv: echo:  M203 X450.00 Y450.00 Z5.00 E25.00
    Recv: echo:Maximum Acceleration (mm/s2):
    Recv: echo:  M201 X3000 Y3000 Z100 E3000
    Recv: echo:Acceleration: S=acceleration, T=retract acceleration
    Recv: echo:  M204 S1000.00 T800.00
    Recv: echo:Advanced variables: S=Min feedrate (mm/s), T=Min travel feedrate (mm/s), B=minimum segment time (ms), X=maximum XY jerk (mm/s),  Z=maximum Z jerk (mm/s),  E=maximum E jerk (mm/s)
    Recv: echo:  M205 S0.00 T0.00 B20000 X10.00 Z0.40 E1.00
    Recv: echo:Home offset (mm):
    Recv: echo:  M206 X0.00 Y0.00 Z0.00
    Recv: echo:PID settings:
    Recv: echo:   M301 P33.41 I1.47 D189.27
    
Initial Tests
-------------

The initial testing should include printing a known good piece, and fine
tuning the M92 codes. To do this download a block like:

`CHEP <https://www.youtube.com/watch?v=UUelLZvDelU>`_ 
