#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# bokeh serve ./GratingBokeh.py
# (wg-python-fix-pdbrc)
#
# (compile (format "python -m py_compile %s" (buffer-file-name)))
# (compile (format "pydoc3 %s" (buffer-file-name)))

### HEREHEREHERE

import os
import optparse
import sys
import io
import re
from Flex_Patron     import Flex_Patron
from collections     import OrderedDict
from FlexPublish     import fakedisplay        # Display upgrade 
from Flex_Instrument import Flex_Instrument    # Flex_Instrument,Flex_InstrumentException

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
class BokehGrating(Flex_Patron):
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
    # (setq properties '("" ""))
    def __init__(self, instrument : 'Flex_Instrument', /,     # BokehGrating::__init__()
                       name       : str           = "grating",   # internal Ardnino name
                       grating    : str           = "300 l/mm",  # Our opinion Ardnino's l/mm
                       display    : 'FlexPublish' = fakedisplay, # Browser thingy to publish things
                       width      : int           = 200,         # Bokeh: width of our  <DIV>
                       notify     : bool          = False):      # Bokeh/Dispatch send out initial notification
        """
        If requested grating in choices, then use it otherwise add it.
        The grating is a mechanized component of the 'Instrument', with the
        Ardino name of 'grating'
        """

        # snipped of dead code to presume a grating...
        if(grating not in self.GratingInserts):        # guarantee the user's request in our vocab
            self.GratingInserts.append(grating)        # this is a programming error, so default...
            self.GratingsTable[grating] = [3500.0, 7500.0] # ...establish a default for values too

        self.grating       = self.GratingInserts.index(grating)
        self.display       = display                   # the name of the display for status trace
        self.instrument    = instrument                # Name of associated instrument
        self.name          = name                      # Name of this instance
        self.wwidth        = width                     # govern the width of the Bokeh widgets
        self.notify        = notify                    # send(or not) out notification on startuy.

        # fields matched (shared) with Ardhino C++ class.
        self.grating       = grating                   # Start with a default 300 l/mm
        self.startwave     = 3200                      # start range current grating assume the whole spectrum
        self.endwave       = 10000                     # end   range current grating if grating in new to us.
        self.cwave         = 5000                      # current selected range.
        self.state         = "undefined"               # Just waking up
        self.home          = 0                         # we assume we're not homed
        self.validp        = False                     # wake up in false state
        self.receipt       = 1                         # always ask for a update on status
        self.rotdir        = 1                         # motor direction 1 = CW 2 = CCW

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

        self.rot_group = RadioGroup(labels=["CW", "CCW" ], height=50, width=200,active=0, inline=True)

        self.processbutton    = Button  ( label="Process",     disabled=False, button_type="warning", width=self.wwidth)

        self.homebutton       = Button  ( label="Home",     disabled=False, button_type="danger", width=self.wwidth)

        self.gratingchoices  .on_change('value', lambda attr, old, new: self.update_gratingchoice   (attr, old, new))
        self.cwavechoice     .on_change('value', lambda attr, old, new: self.update_cwave      (attr, old, new))
        self.rot_group       .on_change('active', lambda attr, old, new: self.radio_handler   (attr, old, new))
        self.processbutton   .on_click (lambda : self.update_processbutton())
        self.homebutton      .on_click (lambda : self.update_homebutton())
        if(self.notify):
            self.send_state()    # when initialized send out info.

    ### BokehGrating.__init__()

    def update_gratingchoice(self,attr,old,new):           # BokehGrating::update_gratingchoice()
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

    def update_cwave(self,attr,old,new):                    # BokehGrating::cwave()
        """Get the new slider value and send it."""
        self.cwave = new

    ### BokehGrating.cwave()

    def update_homebutton(self):                            # BokehGrating::update_homebutton()
        """Send a home command"""
        self.home      = 1
        self.send_state()
        self.home      = 0   # clear the command

    ### BokehGrating.update_homebutton()

    def radio_handler(self,attr, old, new):                 # BokehFlexBlinky::radio_handler()
        """Do something about the blink via an event lambda"""
        self.state = new # self.blink_group.active
        if(self.rotdir not in [0,1]):
            self.rotdir = 3;
        self.send_state()

    ### BokehGrating..radio_handler()

    def update_processbutton(self):                         # BokehGrating::update_homebutton()
        """Send a home command"""
        self.send_state()


    ### BokehGrating.update_homebutton()

    def send_state(self):                                   # BokehGrating::send_state()
        """Several ways to send things"""
        flexname = self.instrument.flexname                         # get the actual latest name.
        devstate = dict( [ ( "grating"   , self.grating),
                           ( "cwave"     , f"{self.cwave:d}"),
                           ( "home"      , f"{self.home:d}"),
                           ( "rotdir"    , f"{self.rotdir}"),
                           ( "receipt"   , f"{self.receipt:d}")
                         ])
        gadgetcmd             = dict([("process", devstate)])
        d2                    = dict([(f"{self.name.lower()}", gadgetcmd)])
        d3                    = dict([(f"{flexname}", d2)])
        jdict                 = json.dumps(d3)
        self.display.display(f'{jdict}')

    ### BokehGrating.send_state()

    def layout(self):                                       # BokehGrating::layout()
        """Get the layout in gear"""
        return(row ( column ( self.gratingchoices,
                              self.cwavechoice,
                              self.rot_group,
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

    ##################################################################
    #  Abstract methods needed
    #  
    ##################################################################
    def get_state(self) ->bool:
        raise(FlexPatronException(f"{self.__class__name} get_state implemented"))
        pass

    def Process(self, jsonstr : (dict,'FlexStdString') = None, reply : str = "") -> int:
        raise(FlexPatronException(f"{self.__class__name} Process implemented"))
        pass
    def ThinkFast(self, report : (str,'FlexStdString') = None)-> int:
        raise(FlexPatronException(f"{self.__class__name} ThinkFast implemented"))
        pass
    def Report(self,report : (str,'FlexStdString') = None)-> str:
        raise(FlexPatronException(f"{self.__class__name} Report implemented"))
        pass
    def Inventory(self,report : (str,'FlexStdString') = None)-> int:
        raise(FlexPatronException(f"{self.__class__name} Inventory implemented"))
        pass
    def Reset(self) ->'self':
        raise(FlexPatronException(f"{self.__class__name} Reset implemented"))
        pass
    def Validp(self) ->bool:
        raise(FlexPatronException(f"{self.__class__name} Validp implemented"))
        pass


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
