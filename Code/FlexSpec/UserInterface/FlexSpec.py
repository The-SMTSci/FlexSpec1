#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# bokeh serve ./FlexSpec.py --unused-session-lifetime 3600000
# (wg-python-fix-pdbrc)

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
from Display              import FlexDisplay

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


"""

__author__  = 'Wayne Green'
__version__ = '0.1'


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

    width          = 350
    flexname       = "FlexSpec_Rodda"
    fstitle        = TextInput(value=f"{flexname}", background='Black',disabled=True, width=width)
    display        = FlexDisplay("f{flexname}",width=600)

    curdoc().theme = 'dark_minimal'
    curdoc().title = "FlexSpec1 Spectrograph"
    kzin1          = BokehKzinRing("Tony's Kzin Ring",display=display,width=350)
    l1             = kzin1.layout()
    tab1           = Panel(child=l1,title='Kzin Calibration')

    slits          = BokehOVIOSlit   (flexname,display=display,width=width)
    grating        = BokehGrating    (flexname,display=display,width=width)
    pangle         = FlexOrientation (flexname,display=display,width=width)
    guider         = Guider          (flexname,display=display,width=width)
    collimator     = Collimator      (flexname,display=display,width=width)

    l2             = column(fstitle,                Spacer(width=width, height=5, background='black'),          
                            slits.layout(),         Spacer(width=width, height=5, background='black'),
                            grating.layout(),       Spacer(width=width, height=5, background='black'),
                            guider.layout(),        Spacer(width=width, height=5, background='black'),
                            collimator.layout(),    Spacer(width=width, height=5, background='black'),
                            pangle.layout())

    ln             = column(display.layout())
    tab2           = Panel(child=l2,title='FlexSpec')

    tabn           = Panel(child = ln, title="Display")

    tabs           = Tabs(tabs=[tab2,tab1,   tabn])

    try:
        curdoc().add_root(row(tabs))
    except Exception as e:
        print("FlexSpec: Main. Terminating.")
        display.display(b'end')



