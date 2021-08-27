#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# bokeh serve ./GratingBokeh.py
# (wg-python-fix-pdbrc)

### HEREHEREHERE

import os
import optparse
import sys
import io
import re
from collections import OrderedDict
from Display import fakedisplay        # Display upgrade

import json

from bokeh.events   import ButtonClick
from bokeh.io       import curdoc
from bokeh.layouts  import column, row, Spacer
from bokeh.models   import ColumnDataSource, Div, Slider, TextInput, Button
from bokeh.models   import RadioGroup
from bokeh.models   import Select

#from bokeh.models.widgets import Tabs, Panel

#############################################################################
#
#  /home/git/external/xxx.SAS_NA1_3D_Spectrograph/Code/NA1Focus/GratingBokeh.py
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
# https://docs.bokeh.org/en/latest/docs/user_guide/interaction/widgets.html#paragraph
#
#
# (wg-python-toc)
#
#############################################################################
__doc__ = """

/home/git/external/xxx.SAS_NA1_3D_Spectrograph/Code/NA1Focus/GratingBokeh.py
[options] files...

This class displays a rate field, a state field (on/off) and
a small error text field.

A little documentation help.
(wg-browser "https://docs.bokeh.org/en/latest/docs/reference.html#refguide")

Grating is a tiny class, that should be part of every Arduino, giving the
user the ability to start a LED blinking.

The blink pattern is on for a duration, off for a duration, and
a pause between the on/off states. I can make a short pulse
every 10 seconds or every 1 second. (The off specification).

Grating Description:

The Flex Spec Ovio holder has one position Dark.
The home position is set to that


Kzin Ring Assy.

"""


__author__  = 'Wayne Green'
__version__ = '0.1'
__all__     = ['BokehGrating','BokehGratingException']   # list of quoted items to export

# (wg-python-class "BokehGrating")
##############################################################################
# BokehGratingException
#
##############################################################################
class BokehGratingException(Exception):
    """Special exception to allow differentiated capture of exceptions"""
    def __init__(self,message,errors=None):
        super(BokehGratingException,self).__init__("FlexGrating "+ message)
        self.errors = errors
    @staticmethod
    def __format__(e):
        return f" FlexGrating: {e.__str__()}\n"
# BokehGratingException

##############################################################################
# BokehGrating
#
##############################################################################
class BokehGrating(object):
    """ A small class to blink the led, with varying rate
    """

    # FAKE up some enums.
    brre     = re.compile(r'\n')                         # used to convert newline to <br/>
    GratingInserts = ["150 l/mm","300 l/mm","600 l/mm","1200 l/mm","1800 l/mm"]

    GratingsTable = OrderedDict( [ ("150 l/mm"  , [3000.0, 9500.0]),  # Synchronize with BokehGrating.GratingInserts
                                   ("300 l/mm"  , [3000.0, 7500.0]),
                                   ("600 l/mm"  , [3500.0, 7500.0]),
                                   ("1200 l/mm" , [3500.0, 7500.0]),
                                   ("1800 l/mm" , [3500.0, 7500.0])
                                 ])

    #__slots__ = [''] # add legal instance variables
    # (setq properties `("" ""))
    def __init__(self, flexname : str = "Default",
                 name : str = "Grating",
                 display = fakedisplay,
                 grating : str = "300 l/mm",
                 width=200): # BokehGrating::__init__()
        """Initialize this class."""
        #super().__init__()
        # (wg-python-property-variables)
        self.display       = display
        self.flexname      = flexname    # Name of associated instrument
        self.name          = name        # Name of this instance
        self.wwidth        = width
        self.grating       = grating     # Start with a default 300 l/mm
        self.startwave     = 100         # start range current grating
        self.endwave       = 200         # end   range current grating
        self.cwave         = 50          # current selected range.
        self.slit          = "20"
        self.state         = "undefined"
        self.homestate     = 0
        self.homed         = False       # don't know.
        self.validp        = False       # wake up in false position


        # Handle startup the easy way. Proper will be to query before instantiation.
        entry              =  BokehGrating.GratingsTable.get(grating,None)
        if(entry is not None):
            grating = entry
            self.cwave    = self.startwave   = entry[0]
            self.endwave  = entry[1]

        self.gratingchoices   = Select  (title=f"Gratings",value='20',options=self.GratingInserts, width=self.wwidth)
        self.cwavechoice   = Slider  (title=f"Central Wavelength (A)", bar_color='firebrick',
                                     value = self.cwave, start = self.startwave,  
                                     end = self.endwave+1, step = 10, width=self.wwidth)
        self.processbutton = Button  ( label="Process",     disabled=False, button_type="warning", width=self.wwidth)

        self.homebutton    = Button  ( label="Home",     disabled=False, button_type="danger", width=self.wwidth)
        self.gratingchoices     .on_change('value', lambda attr, old, new: self.update_slitchoice   (attr, old, new))
        self.cwavechoice     .on_change('value', lambda attr, old, new: self.update_cwave      (attr, old, new))
        self.processbutton   .on_click (lambda : self.update_processbutton())
        self.homebutton      .on_click (lambda : self.update_homebutton())
        self.send_state()

    ### BokehGrating.__init__()

    def update_slitchoice(self,attr,old,new):                    # BokehGrating::update_slitchoice()
        """update_debugbtn Button via an event lambda"""
        grating = new # self.gratingchoices.value
        entry   = BokehGrating.GratingsTable.get(grating)
        if(entry):
            self.grating           = grating
            self.startwave         = entry[0]             # set our values first
            self.endwave           = entry[0]
            if(self.cwave == 50):
                self.cwave             = entry[1]
            self.gratingchoices.value = f"{self.startwave}"  # update with current values.
            #self.gratingchoices.start = f"{self.endwave}"
            #self.gratingchoices.end   = f"{self.cwave}"
        #self.send_state()

    ### BokehGrating.slitchoice()

    def update_cwave(self,attr,old,new):                        # BokehGrating::cwave()
        """Get the new slider value and send it."""
        self.cwave = new

    ### BokehGrating.cwave()

    def update_homebutton(self):                                # BokehGrating::update_homebutton()
        """Send a home command"""
        self.homestate = 1
        self.send_state()
        self.homestate = 0

    def update_processbutton(self):                                # BokehGrating::update_homebutton()
        """Send a home command"""
        self.send_state()

    ### BokehGrating.update_homebutton()

    def send_state(self):                                       # BokehGrating::send_state()
        """Several ways to send things"""
        devstate = dict( [ ( "grating"   , self.grating),
                          ( "cwave"     , self.cwave),
                          ( "homestate" , self.homestate)
                        ])
        slitcmd = dict([("Process", devstate), ("Receipt" , 0)])
        slitcmd['Receipt'] = 1                             # set the receipt as desired
        d2 = dict([(f"{self.name}", slitcmd)])
        d3 = dict([(f"{self.flexname}", d2)])
        jdict = json.dumps(d3)
        self.display.display(f'{jdict}')

    ### BokehGrating.send_state()

    def layout(self):                                           # BokehGrating::layout()
        """Get the layout in gear"""
        return(row ( column ( self.gratingchoices,
                              self.cwavechoice,
                              self.processbutton,
                              self.homebutton
                            )  ))

    ### BokehGrating.layout()

    def debug(self,msg="",skip=[],os=sys.stderr):               # BokehGrating::debug()
        """Help with momentary debugging, file to fit.
           msg  -- special tag for this call
           skip -- the member variables to ignore
           os   -- output stream: may be IOStream etc.
        """
        import pprint
        print("BokehGrating - %s " % msg, file=os)
        for key,value in self.__dict__.items():
            if(key in skip):
               continue
            print(f'{key:20s} =',file=os,end='')
            pprint.pprint(value,stream=os,indent=4)
        return self

    ### BokehGrating.debug()

    __BokehGrating_debug = debug  # really preserve our debug name if we're inherited

   # (wg-python-properties properties)

# class BokehGrating


##############################################################################
#                                    Main
#                               Regression Tests
##############################################################################
# HEREHEREHERE
if(0):
    opts = optparse.OptionParser(usage="%prog "+__doc__)

    opts.add_option("-v", "--verbose", action="store_true", dest="verboseflag",
                   default=False,
                   help="<bool>     be verbose about work.")

    (options, args) = opts.parse_args()

    curdoc().theme = 'dark_minimal'
    curdoc().title = "Grating1 Test"
    grating = BokehGrating("FlexSpec_Rodda")
    curdoc().add_root(row(grating.layout()))
