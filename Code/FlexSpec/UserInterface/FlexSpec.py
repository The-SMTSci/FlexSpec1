#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (compile "bokeh serve ./FlexSpec.py --unused-session-lifetime 3600000")
# (wg-python-fix-pdbrc)
# /home/git/external/FlexSpec1/Code/FlexSpec/UserInterface/FlexSpec.py
#
# (compile (format "python -m py_compile %s" (buffer-file-name)))
#
### HEREHEREHERE

import os
import optparse
import sys
import re
import logging

from bokeh                import events
from bokeh.events         import ButtonClick
from bokeh.io             import curdoc
from bokeh.layouts        import column, row, Spacer
from bokeh.models         import ColumnDataSource, Slider, TextInput, Button
from bokeh.models         import CustomJS, Div
from bokeh.plotting       import figure
from bokeh.models         import RadioGroup
from bokeh.models         import Select
from bokeh.models.widgets import Tabs, Panel

from Flex_Log             import *
from SlitBokeh            import BokehOVIOSlit
from KzinBokeh            import BokehKzinRing
from ParallacticAngle     import FlexOrientation
from GratingBokeh         import BokehGrating
from Guider               import Guider
from Collimator           import Collimator
from FlexPublish          import FlexPublish
from ParallacticAngle     import FlexOrientation
from Network              import FlexNetwork
from CameraFocusBokeh     import CameraFocus
from FlexTextInput        import FlexTextInput
from Flex_Instrument      import Flex_Instrument
from Flex_Dispatcher      import Flex_Dispatcher
from Flex_Shutter         import Flex_Shutter

#############################################################################
#
#  /home/git/external/SAS_NA1_3D_Spectrograph/Code/FlexSpec.py
#
#emacs helpers
# (insert (format "\n# %s " (buffer-file-name)))
#
# (set-input-method 'TeX' t)
# (toggle-input-method)
#
# (wg-astroconda3-pdb)      # CONDA Python3
#
# (wg-python-fix-pdbrc)  # PDB DASH DEBUG end-comments
#
# (ediff-current-file)
# (find-file-other-frame "./.pdbrc")

# (setq mypdbcmd (concat (buffer-file-name) "<args...>"))
# (progn (wg-python-fix-pdbrc) (pdb mypdbcmd))
#
# (wg-astroconda-pdb)       # IRAF27
#
# (set-background-color "light blue")
#
# (wg-python-toc)
#
#############################################################################
__doc__ = """

/home/git/external/SAS_NA1_3D_Spectrograph/Code/FlexSpec.py
[options] files...

The FlexSpec 'instrument' uses an Arduino or similar microprocessor.
The processor supports a number of 'gadgets' that control sub-insrumentation.
A 'gadget' is a widget without a window.

Here gadgets cover the Kzin ring, collimator, grating rotator, etc.
They are considered 'Patrons' of their device within the Postmaster
paragigm we use where a json string containing the state for
the gadget is passed to the Arduino, and a similar string
is returned reflecting the actual state the gadget was able to
achieve. This accounts for things like stepper-motor intervals
known only to the instrument.

This program constitutes a "main program" (bokeh remote client) on a
SBC (Raspberry pi etc.). It looks for an utilizes a dispatch server
on HOST at PORT. This is a 'Postmaster' responsible for the hosting
RPi to allow other avenues of messages to the Instrument.

A kitchen sink of devices is in this mix to assist with writing
proper FITS headers when the time comes.

This module relies on the RunFlexSpec script and a dispatch
server running as a seperate process.

The REST interface sets the internal state of this collection
of classes. When a "Process" "Home" or other "command" button
is pressed -- the internal state of these classes are sent
to a remote device. It is then up to the remote device to
"match" states. Thus, there are no real commands.

The remote device 'reacts' to the new knowledge of the
state of these classes by setting it's internal state
(by moving things or turing things on/off).

More complete layout discussion
https://medium.com/y-data-stories/python-and-bokeh-part-iii-tutorial-116aa2e873eb

https://docs.bokeh.org/en/latest/docs/user_guide/embed.html#bokeh-applications
"""

__author__  = 'Wayne Green'
__version__ = '0.1'

# Related to css and Bokeh
#class MyResources(Resources):
#    """ https://stackoverflow.com/questions/44607084/background-color-of-bokeh-layout """
#    @property
#    def css_raw(self):
#        return super().css_raw + [
#            """.bk-root {
#                    background-color: #000000;
#                    border-color: #000000;
#                    }
#            """
#        ]
## class MyResources

def settitle(attr,old,new):
    print(f"FlexSpec settitle old={attr}, old={old}, new={new}")

##############################################################################
#                                    Main
#                               Regression Tests
##############################################################################
# HEREHEREHERE
if (1):  # This is main! leave set to 1
    opts = optparse.OptionParser(usage="%prog "+__doc__)

    opts.add_option("--host", action="store", dest="host",
                   default='localhost',
                   help="<IP address>  The address to use.")

    opts.add_option("--port", action="store", dest="port",
                   default=5006,
                   help="<IP Port>    The IP Port to use ")

    opts.add_option("-v", "--verbose", action="store_true", dest="verboseflag",
                   default=False,
                   help="<bool>     be verbose about work.")

    (options, args) = opts.parse_args()

    # set a few main constants
    width          = 600                              # width of the main div
    flexname       = "FlexSpec_Rodda"
    logger         = Flex_Log() # logging.getLogger(__name__) # 
    logger.info(f"FlexSpec {flexname} starting...")
    display        = FlexPublish("f{flexname}",width=width)
    instrument     = Flex_Instrument(logger,flexname,display,width=width)  # initialize the instrument with flexname


    shutter        = Flex_Shutter    (instrument,display=display,width=width)
    kzin1          = BokehKzinRing   (instrument,display=display,width=width,shutter=shutter)
    slits          = BokehOVIOSlit   (instrument,display=display,width=width)
    grating        = BokehGrating    (instrument,display=display,width=width)
    pangle         = FlexOrientation (instrument,display=display,width=width)
    guider         = Guider          (instrument,display=display,width=width)
    collimator     = Collimator      (instrument,display=display,width=width)
    camerafocus    = CameraFocus     (instrument,display=display,width=width)
    network        = FlexNetwork     (instrument,display=display,width=width)

    gadgets        = dict([('kzin'       , kzin1       ), # tie the flexspec gadgets to their methods.
                           ('display'    , display     ),
                           ('slits'      , slits       ),
                           ('grating'    , grating     ),
                           ('pangle'     , pangle      ),
                           ('collimator' , collimator  ),
                           ('camerafocus', camerafocus )
                         ])

    dispatcher     = Flex_Dispatcher(instrument,gadgets)
    dispatcher.debug()

    #-------------------------------- Tab 1 -------------------------------------
    # The control tab (left most)
    l1             = column(instrument.layout()  ,  Spacer(width=width, height=5, background='black'),
                            grating.     layout(),  Spacer(width=width, height=5, background='black'),
                            collimator.  layout(),  Spacer(width=width, height=5, background='black'),
                            pangle.      layout())

    tab1           = Panel(child=l1,title='FlexSpec')

    #-------------------------------- Tab 2 -------------------------------------
    # The kzin control
    l2             = kzin1.layout()
    tab2           = Panel(child=l2,title='Kzin Calibration')

    #-------------------------------- Tab 3 -------------------------------------
    # Provision for additional network information (On for now)
    l3             = column(network.layout())
    tab3           = Panel(child=l3,title='Network')

    #-------------------------------- Tab 4 -------------------------------------
    # Provision for coming attractions unimplemented
    l4             = column( slits.       layout(),  Spacer(width=width, height=5, background='black'),
                             guider.      layout(),  Spacer(width=width, height=5, background='black'),
                             camerafocus. layout(),  Spacer(width=width, height=5, background='black'),
                           )
    tab4           = Panel(child=l4,title='Static Gadgets')

    ########################### Start the main layout ###########################
    ln             = column(display.layout())


    ############################ Create the main tab ############################
    # Tab n is the last tab (here devoted to a report column)

    tabn           = Panel(child = ln, title="Display")   # TODO Tuck the display back as a main panel tabs

    tabs           = Tabs(tabs=[tab1,tab2,tab3,tab4,tabn])

    try:
        curdoc().theme = 'dark_minimal'
        curdoc().title = "FlexSpec1 Spectrograph"
        curdoc().add_root(row(tabs,ln))
    except Exception as e:
        print("FlexSpec: Main. Terminating.")
        display.display(b'end')



