README
======

Testing can be done with Chrome in incognito mode (does't clutter
up cookies).

This approach uses a "matched class" and a "data driven" approach.
The 'def send_state(self) is the gateway to Flex dispatch server for
    each class.

FlexSpec.py - instantiate/layout the gadgets we're currently supporting:
   KzinBokeh.py
   Collimator.py
   GratingBokey.py GrratingDefinition.py
   ParallacticAngle.py
   Shutter.py  (Needs to be developed fully)

Other Gadgets:
      EEPROMBokeh.py
      BlinkyBokeh.h

Good to have:
     Site.py
     TargetsBokeh.py
     FITS/FITS.py       -- brew up header for the instrument


The objects to use/develop:

    BlinkyBokeh.py       - Test more than anything
    CameraFocusBokeh.py  - NOT the 'camera' lens
    Collimator.py        - drive the collimator motors
    EEPROMBokeh.py       - manage an eeprom filesystem     FlexEEPROM.py        -
    FITS.py              - FlexSpec FITS header details, fits format
    FlexSpec.py          - A class for the device itself
    GratingBokeh.py      - Motors and configuration of  a grating
    GratingDefinition.py - Definition of lots of gratings to choose
    Guider.py            - NOT focus/rotate the guider
    KzinBokeh.py         - Manage the cal lamps and the shutter
    LampBokeh.py         - ?
    Network.py           - GUI/Dispatch server management
    ParallacticAngle.py  - pangle - get/report the parallactic angle
    Shutter.py           - Deal with the shutter itself
    Site.py              - Site details
    SlitBokeh.py         - Select and manage slit details
    TargetsBokeh.py      - NOT state the curent target details

TBD: FITS.py, Site,Targets. Network

Not clearly defined.... FlexPublish.py       -




RunFlexSpec


Two classes -- A python class at the Bokeh level and a C++ class in the
Arduino have their data synchronized. The user's request is tested and all
error checking in performed at the Bokeh class then an image of the
variables' state is sent to the matched Arduino C++ partner class.
The C++ class strives to "match the request" and will achieve a final
state. For example a request for 5000 angstroms for a grating's central
wavelength may fall between 4995 and 5007 due to cogging of the control
motor. Assuming perfect backlash, the C++ class may choose 4995. It
then reports its state back to the Bokeh class -- the Bokeh updates
the user's interface to reflect the "current state-of-affairs" of the
remote device. The governing rule is the remote device takes precedence
over the display. The display strives to portray the remote state-of-affairs.

Release Note:
2022-08-09T08:20:31-0600

Several modules were sending actual non-quoted integer/float
values. This was corrected though there may be a few missed
cases. While the code was open, a few major internal changes
were implemented. This does not effect the general operation.

The main visible change is the 'Display' pane now outputs
text that may be cut then pasted into Python. This is more
for checking results by hand. This work is leading to
a log message.

The code was re-worked for formatting, nomenclature (Display was
changed to FlexPublish to reflect what it really does), the layout
variable names changed to reflect their actual order etc.  Comments
were added, formatting of the code, usual beautification things.

Work has began on the serial interface extension(s) to the
main backend dispatch server. Written in python, with the
target machine being the Raspberry Pi 4B+.


.. note::

    myapp
       |
       +---__init__.py
       +---app_hooks.py
       +---main.py
       +---request_handler.py
       +---static
       +---theme.yaml
       +---templates
            +---index.html

.. note::

    myapp
       |
       +---__init__.py
       |
       +---app_hooks.py
       +---data
       |    +---things.csv
       |
       +---helpers.py
       +---main.py
       |---models
       |    +---custom.js
       |
       +---request_handler.py
       +---static
       |    +---css
       |    |    +---special.css
       |    |
       |    +---images
       |    |    +---foo.png
       |    |    +---bar.png
       |    |
       |    +---js
       |        +---special.js
       |
       |---templates
       |    +---index.html
       |
       +---theme.yaml
    








