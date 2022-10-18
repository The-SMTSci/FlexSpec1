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
from collections    import OrderedDict
from FlexPublish    import fakedisplay        # Display upgrade

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
#
# (wg-python-toc)
#
# __doc__ = """
# __author__  = 'Wayne Green'
# __version__ = '0.1'
# __all__     = ['BokehGrating','BokehGratingException']   # list of quoted items to export
# class BokehGratingException(Exception):
#     def __init__(self,message,errors=None):
#     @staticmethod
#     def __format__(e):
# class BokehGrating(object):
#     #__slots__ = [''] # add legal instance variables
#     def __init__(self, flexname : str = "Default",              # BokehGrating::__init__()
#     def update_gratingchoice(self,attr,old,new):                # BokehGrating::update_gratingchoice()
#     def update_cwave(self,attr,old,new):                        # BokehGrating::cwave()
#     def update_homebutton(self):                                # BokehGrating::update_homebutton()
#     def update_processbutton(self):                             # BokehGrating::update_homebutton()
#     def send_state(self):                                       # BokehGrating::send_state()
#     def layout(self):                                           # BokehGrating::layout()
#     def debug(self,msg="",skip=[],os=sys.stderr):               # BokehGrating::debug()
#
#############################################################################
__doc__ = """

FlexSpec1/Code/NA1Focus/GratingBokeh.py

Designed to be included by a senior class to implement a control
panel for the FlexSpec1 spectrograph.

This class implements a Bokeh super-widget for the FlexSpec1 spectrograph
to allow choice of gratings. The gratings are contained, by name in
GratingDefinitions.py

A little documentation help.
   "https://docs.bokeh.org/en/latest/docs/reference.html#refguide"

Each grating carries a bit of information that should appear in headers
and to allow useful calculations about offsets etc.

The regression test for this module is guarded by if(0), but may
(probably not now!) contain some hints about the operation of this class.

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
    GratingInserts = ["150 l/mm","300 l/mm","600 l/mm","1200 l/mm","1800 l/mm","Unknown"]

    GratingsTable = OrderedDict( [ ("150 l/mm"  , [3000.0, 9500.0]),  # Synchronize with BokehGrating.GratingInserts
                                   ("300 l/mm"  , [3000.0, 7500.0]),
                                   ("600 l/mm"  , [3500.0, 7500.0]),
                                   ("1200 l/mm" , [3500.0, 7500.0]),
                                   ("1800 l/mm" , [3500.0, 7500.0])
                                 ])

    #__slots__ = [''] # add legal instance variables
    # (setq properties `("" ""))
    def __init__(self, flexname : str = "Default",              # BokehGrating::__init__()
                       name     : str = "Grating",
                       display        = fakedisplay,
                       grating : str  = "300 l/mm",
                       width   : int  = 200):
        """Initialize this class. If requested grating in choices, then use it
           otherwise add it.
        """

        # snipped of dead code to presume a grating...
        if(grating not in self.GratingInserts):        # guarantee the user's request in our vocab
            self.GratingInserts.append(grating)        # this is a programming error, so default...
            self.GratingsTable[grating] = [3500.0, 7500.0] # ...establish a default for values too

        self.grating       = self.GratingInserts.index(grating)
        self.display       = display                   # the name of the display for status trace
        self.flexname      = flexname                  # Name of associated instrument
        self.name          = name                      # Name of this instance
        self.wwidth        = width                     # govern the width of the Bokeh widgets
        self.grating       = grating                   # Start with a default 300 l/mm
        self.startwave     = 3200                      # start range current grating assume the whole spectrum
        self.endwave       = 10000                     # end   range current grating if grating in new to us.
        self.cwave         = 5000                      # current selected range.
        self.state         = "undefined"               # Just waking up
        self.home          = 0                         # we assume we're not homed
        self.validp        = False                     # wake up in false state
        self.receipt       = 1                         # always ask for a update on status

        # Handle startup the easy way. Proper will be to query before instantiation.
        entry              =  BokehGrating.GratingsTable.get(grating,None)
        if(entry is not None):
            grating          = entry
            self.startwave   = entry[0]
            self.endwave     = entry[1]

        self.gratingchoices   = Select  (title=f"Gratings",value=self.grating,options=self.GratingInserts, width=self.wwidth)
        self.cwavechoice      = Slider  (title=f"Central Wavelength (A)", bar_color='firebrick',
                                     value = self.cwave, start = self.startwave,  
                                     end = self.endwave+1, step = 1, width=self.wwidth)
        self.processbutton    = Button  ( label="Process",     disabled=False, button_type="warning", width=self.wwidth)

        self.homebutton       = Button  ( label="Home",     disabled=False, button_type="danger", width=self.wwidth)
        self.gratingchoices     .on_change('value', lambda attr, old, new: self.update_gratingchoice   (attr, old, new))
        self.cwavechoice     .on_change('value', lambda attr, old, new: self.update_cwave      (attr, old, new))
        self.processbutton   .on_click (lambda : self.update_processbutton())
        self.homebutton      .on_click (lambda : self.update_homebutton())
        self.send_state()

    ### BokehGrating.__init__()

    def update_gratingchoice(self,attr,old,new):                # BokehGrating::update_gratingchoice()
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

    ### BokehGrating.update_gratingchoice()

    def update_cwave(self,attr,old,new):                        # BokehGrating::cwave()
        """Get the new slider value and send it."""
        self.cwave = new

    ### BokehGrating.cwave()

    def update_homebutton(self):                                # BokehGrating::update_homebutton()
        """Send a home command"""
        self.home      = 1
        self.send_state()
        self.home      = 0   # clear the command


    def update_processbutton(self):                             # BokehGrating::update_homebutton()
        """Send a home command"""
        self.send_state()

    ### BokehGrating.update_homebutton()

    def send_state(self):                                       # BokehGrating::send_state()
        """Several ways to send things"""
        devstate = dict( [ ( "grating"   , self.grating),
                           ( "cwave"     , f"{self.cwave:d}"),
                           ( "home"      , f"{self.home:d}"),
                           ( "receipt"   , f"{self.receipt:d}")
                         ])
        gadgetcmd            = dict([("process", devstate)])
        d2                    = dict([(f"{self.name.lower()}", gadgetcmd)])
        d3                    = dict([(f"{self.flexname}", d2)])
        jdict                 = json.dumps(d3)
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
