#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# (compile (format "python -m py_compile %s" (buffer-file-name)))
#
# change the if stmt at bottom from if(0) to if(1) for regression.
# bokeh serve ./BlinkyBokeh.py
# (wg-python-fix-pdbrc)

### HEREHEREHERE

import os
import optparse
import sys
import io
import re
import json
from FlexPublish import fakedisplay        # Display upgrade

from bokeh.events   import ButtonClick
from bokeh.io       import curdoc
from bokeh.layouts  import column, row
from bokeh.models   import ColumnDataSource, Div, Slider, TextInput, Button
from bokeh.models   import Paragraph, Spacer, RadioGroup
from bokeh.plotting import figure


#############################################################################
#
#  /home/git/external/xxx.SAS_NA1_3D_Spectrograph/Code/NA1Focus/BlinkyBokeh.py
#
#
# (wg-python-toc)
#
#############################################################################
__doc__ = """

/home/git/external/xxx.SAS_NA1_3D_Spectrograph/Code/NA1Focus/BlinkyBokeh.py

The Arduino's have a built-in Color LED

This class displays a rate field, a state field (on/off) and a small
error text field.

A little documentation help.
(wg-browser "https://docs.bokeh.org/en/latest/docs/reference.html#refguide")

Blinky is a tiny class, that should be part of every Arduino, giving the
user the ability to start a LED blinking.

The blink pattern is on for a duration, off for a duration, and
a pause between the on/off states. I can make a short pulse
every 10 seconds or every 1 second. (The off specification).


   int colormask     0RBG                   ; // 3 lsb for colors, or ignored mono
   int         onduration                   ; // the duration
   int         offduration                  ; // the off duration
   int         state                        ; // toggle the on/off state



"""


__author__  = 'Wayne Green'
__version__ = '0.1'
__all__     = ['BokehFlexBlinky','FlexBlinkyException']   # list of quoted items to export

# (wg-python-class "FlexBlinky")
##############################################################################
# FlexBlinkyException
#
##############################################################################
class FlexBlinkyException(Exception):
    """Special exception to allow differentiated capture of exceptions"""
    def __init__(self,message,errors=None):
        super(FlexBlinkyException,self).__init__("FlexBlinky "+ message)
        self.errors = errors
    @staticmethod
    def __format__(e):
        return f" FlexBlinky: {e.__str__()}\n"
# FlexBlinkyException

##############################################################################
# BokehFlexBlinky
#
##############################################################################
class BokehFlexBlinky(object):
    """ A small class to blink the led, with varying rate
    """

    # FAKE up some enums.
    ON       = 0  # BokehFlexBlinky.ON
    OFF      = 1  # BokehFlexBlinky.OFF
    RUN      = 2  # BokehFlexBlinky.RUN
    SateText = ["Off","On","Illegal"]
    brre     = re.compile(r'\n')                         # used to convert newline to <br/>
    postmessage = { "name"    : "Unassigned",
                    "pin"     : None ,
                    "ontime"  : None ,
                    "offtime" : None ,
                    "rate"    : None ,
                    "state"   : None
                    }

    #__slots__ = [''] # add legal instance variables
    # (setq properties `("" ""))
    def __init__(self, name : str = "Default",
                 display = fakedisplay,
                 rate : int = 1,
                 wwidth=200,
                 pin=4): # BokehFlexBlinky::__init__()
        """Initialize this class."""
        #super().__init__()
        # (wg-python-property-variables)
        self.pin         = pin
        self.display     = display
        self.name        = name
        self.wwidth      = wwidth
        self.rate        = rate
        self.state       = BokehFlexBlinky.OFF
        self.ontime      = 0
        self.offtime     = 0

        #self.ratefield   = TextInput (title=f"{self.name} Count:", width=self.wwidth)
        self.blink_group = RadioGroup(labels=[f"{self.name} Off", f"{self.name} On" ], height=50, width=200,active=0, orientation='vertical')

        self.bkontime    = Slider    (title=f"{self.name} On-time [ms]", bar_color='firebrick',
                                      value = 1.0, start = self.ontime,  end = 1000, step = 1, width=self.wwidth)
        self.bkofftime   = Slider    (title=f"{self.name} Off-time [ms]",  bar_color='firebrick',
                                      value = 1.0, start = self.offtime,  end = 1000, step = 1, width=self.wwidth)
        self.debugbtn    = Button    (align='end', label="DEBUG",     disabled=False, button_type="success", width=self.wwidth)

        self.paragraph   = Div       (text="Hello", width=200,height=200,background='Bisque')

        #self.ratefield   .on_change('value',  lambda attr, old, new: self.rate_handler    (attr, old, new))
        self.blink_group .on_change('active', lambda attr, old, new: self.radio_handler   (attr, old, new))
        self.bkontime    .on_change('value', lambda attr, old, new: self.update_bkontime    (attr, old, new))
        self.bkofftime   .on_change('value', lambda attr, old, new: self.update_bkofftime   (attr, old, new))
        self.debugbtn    .on_click (lambda : self.update_debugbtn())


    ### BokehFlexBlinky.__init__()

    def update_debugbtn(self):                                  # BokehRoboFocuser::update_button_in()
        """update_debugbtn Button via an event lambda"""
        os = io.StringIO()
        self.debug(f"{self.name} Debug", os=os)
        os.seek(0)
        self.display(BokehFlexBlinky.brre.sub("<br/>",os.read()))

    ### BokehFlexBlinky.update_edebugbtn()

    def update_bkontime(self,attr, old, new):                   # BokehRoboFocuser.::pdate_microsteps()
        """update_microsteps Slider"""
        self.ontime=new

    ### BokehFlexBlinky.update_bkontime()

    def update_bkofftime(self,attr, old, new):           #       BokehRoboFocuser.::pdate_microsteps()
        """update_microsteps Slider via an event lambda"""
        self.offtime=new

    ### BokehFlexBlinky.update_bkofftime()

    def radio_handler(self,attr, old, new):                     # BokehFlexBlinky::radio_handler()
        """Do something about the blink via an event lambda"""
        self.state = new # self.blink_group.active
        if(self.state not in [0,1]):
            self.state = 3;
        self.send_state()
    ### BokehFlexBlinky.radio_handler()

    def rate_handler(self,attrname, old, new):                  # BokehRoboFocuser::pdate_commvals()
        """update_commvals TextInput via an event lambda"""
        try:
            val       = 0 # self.ratefield.value.strip()
            self.rate = int(val)
            self.display.display(f"New Rate {self.rate}.")
        except Exception as e:
            self.display.display(f"ERROR: BokehFlexBlinky {self,name}: Rate expecting integer [s].")

    ### BokehFlexBlinky.rate_handler()

    def send_state(self):
        """Several ways to send things"""
        devstate = dict( [
                           ( "name"    , '"%d"' % self.pin     ),  # name of this button
                           ( "pin"     , '"%d"' % self.pin     ),
                           ( "ontime"  , '"%d"' % self.ontime  ),
                           ( "offtime" , '"%d"' % self.offtime ),
                           ( "state"   , '"%d"' % self.state   ),
                         ])
        slitcmd            = dict([("process", json.dumps(devstate)), ("receipt" , json.dumps({"recepit" : "0"}))])

        slitcmd['receipt'] = 1                             # set the receipt as desired
        d2 = dict([(f"{self.name}", slitcmd)])
        d3 = dict([(f"{self.flexname}", d2)])
        jdict              = json.dumps(d3)
        self.display(f'{{ "{self.name}" : {jdict} , "returnreceipt" : 1 }}')

    ### BokehFlexBlinky.send_state()

    def layout(self):                                           # BokehFlexBlinky::layout()
        """Get the layout in gear"""
        return(row ( column ( #self.ratefield ,
                              self.blink_group,
                              self.bkontime,
                              self.bkofftime
                            )  ))

    ### BokehFlexBlinky.layout()

    def debug(self,msg="",skip=[],os=sys.stderr):               # BokehFlexBlinky::debug()
        """Help with momentary debugging, file to fit.
           msg  -- special tag for this call
           skip -- the member variables to ignore
           os   -- output stream: may be IOStream etc.
        """
        import pprint
        print("BokehFlexBlinky - %s " % msg, file=os)
        for key,value in self.__dict__.items():
            if(key in skip):
               continue
            print(f'{key:20s} =',file=os,end='')
            pprint.pprint(value,stream=os,indent=4)
        return self

    ### BokehFlexBlinky.debug()

    __BokehFlexBlinky_debug = debug  # really preserve our debug name if we're inherited

   # (wg-python-properties properties)

# class BokehFlexBlinky

##############################################################################
#                                    Main
#                               Regression Tests
##############################################################################
# HEREHEREHERE
if(0):   # set to 1 for bokeh regression test.
    opts = optparse.OptionParser(usage="%prog "+__doc__)

    opts.add_option("-v", "--verbose", action="store_true", dest="verboseflag",
                   default=False,
                   help="<bool>     be verbose about work.")

    (options, args) = opts.parse_args()

    blink1         = BokehFlexBlinky("PiggyBack")
    display        = FlexPublish("Blinky Test")
    curdoc().theme = 'dark_minimal'
    curdoc().title = "Blinky1 Test"
    curdoc().add_root(row(blink1.layout(), display.layout()))
