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

Main "Program" (bokeh remote client) on a SBC (Raspberry pi etc.)

The kitchen sink of devices is in this mix to assist with writing
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


"""

__author__  = 'Wayne Green'
__version__ = '0.1'


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
    width          = 600                              # width of the main things
    flexname       = "FlexSpec_Rodda"
    instrument     = Flex_Instrument(flexname,width=width)  # initialize the instrument with flexname
    #fstitle        = TextInput(value=f"title{flexname}", background='Black',
    #                           disabled=False, width=width)

    display        = FlexPublish("f{flexname}",width=width)

    slits          = BokehOVIOSlit   (flexname,display=display,width=width)
    grating        = BokehGrating    (instrument,display=display,width=width)  # instrument carries flexname.
    pangle         = FlexOrientation (flexname,display=display,width=width)
    guider         = Guider          (flexname,display=display,width=width)
    collimator     = Collimator      (flexname,display=display,width=width)
    camerafocus    = CameraFocus     (flexname,display=display,width=width)
    network        = FlexNetwork     (instrument,display=display,width=width)

    #fstitle.on_change('value_input', settitle) # call back for this

    #-------------------------------- Tab 1 -------------------------------------
    # The control tab (left most)
    l1             = column(instrument.layout()  ,  Spacer(width=width, height=5, background='black'),
                            #fstitle              ,  Spacer(width=width, height=5, background='black'),
                            grating.     layout(),  Spacer(width=width, height=5, background='black'),
                            collimator.  layout(),  Spacer(width=width, height=5, background='black'),
                            pangle.      layout())

    tab1           = Panel(child=l1,title='FlexSpec')

    #-------------------------------- Tab 2 -------------------------------------
    # The kzin control
    kzin1          = BokehKzinRing("Tony's Kzin Ring",display=display,width=width)
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

    tabn           = Panel(child = ln, title="Display")

    tabs           = Tabs(tabs=[tab1,tab2,tab3,tab4,tabn])

    try:
        curdoc().theme = 'dark_minimal'
        curdoc().title = "FlexSpec1 Spectrograph"
        curdoc().add_root(row(tabs,ln))
    except Exception as e:
        print("FlexSpec: Main. Terminating.")
        display.display(b'end')



