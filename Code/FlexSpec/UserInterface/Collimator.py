#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# (wg-python-fix-pdbrc)

### HEREHEREHERE

import os
import optparse
import sys
import re
import json
from FlexPublish          import fakedisplay        # Display upgrade

from bokeh                import events
from bokeh.events         import ButtonClick
from bokeh.io             import curdoc
from bokeh.layouts        import column, row, Spacer
from bokeh.models         import ColumnDataSource, Slider, TextInput, Button
from bokeh.models         import Spacer
from bokeh.models         import CustomJS, Div
from bokeh.plotting       import figure
from bokeh.models         import RadioGroup
from bokeh.models         import Select
from bokeh.models.widgets import Tabs, Panel


#############################################################################
#
#  FlexSpec1/Code/Collimator.py
#
#emacs helpers
#
# (wg-python-toc)
#
# __doc__ = """
# __author__  = 'Wayne Green'
# __version__ = '0.1'
# __all__     = ['CollimatorException','Collimator']   # list of quoted items to export
# class CollimatorException(Exception):
#     def __init__(self,message,errors=None):
#     @staticmethod
#     def __format__(e):
# class Collimator(object):
#     #__slots__ = [''] # add legal instance variables
#     def __init__(self,                                          # Collimator::__init__()
#     def debug(self,msg="",skip=[],os=sys.stderr):               # Collimator::debug()
#     def update_collimator(self, attr,old,new):                  # Collimator::update_collimator()
#     def update_speed(self, attr,old,new):                       # Collimator::update_speed()
#     def update_stepin(self):                                    # Collimator::update_stepin()
#     def update_stepout(self):                                   # Collimator::update_stepout()
#     def update_homebutton(self):                                # Collimator::update_homebutton()
#     def send_home(self):                                        # Collimator::send_home()
#     def send_state(self):                                       # Collimator::send_state()
#     def layout(self):                                           # Collimator::layout()
#
#
#
#############################################################################
__doc__ = """

/home/git/external/SAS_NA1_3D_Spectrograph/Code/Collimator.py
[options] files...

Handle the details of focusing the Collimating Lens.

Note: There are details in here planned for future updates,
  like a home sensor.


"""

__author__  = 'Wayne Green'
__version__ = '0.1'
__all__     = ['CollimatorException','Collimator']   # list of quoted items to export


##############################################################################
# CollimatorException
#
##############################################################################
class CollimatorException(Exception):
    """Special exception to allow differentiated capture of exceptions"""
    def __init__(self,message,errors=None):
        super(CollimatorException,self).__init__("Collimator "+ message)
        self.errors = errors
    @staticmethod
    def __format__(e):
        return f" Collimator: {e.__str__()}\n"
# CollimatorException


##############################################################################
# Collimator
#
##############################################################################
class Collimator(object):
    """ Manage the Orientation of a Nano
    """
    #__slots__ = [''] # add legal instance variables
    # (setq properties `("" ""))

    brre     = re.compile(r'\n')                         # used to convert newline to <br/>

    def __init__(self, instrument : str   = "Flex_Instrument",  # Collimator::__init__()
                 name     : str   = "Collimator",
                 display          = fakedisplay,
                 position : str   = "0.0",
                 maxrange : float = 1.5,
                 width    : int   = 200):
        """Initialize this class."""
        #super().__init__()
        # (wg-python-property-variables)
        self.instrument      = instrument     # name of the FlexSpec tied to this python instance
        self.name            = name             # name of the C++ instance in FlexSpec box
        self.display         = display          # the FlexDisplay to report
        self.wwidth          = width            # c++ instance width to guide bokeh widgits herein
        self.position        = float(position)  # c++ instance position of the collimator's motor
        self.speed           = 0.10             # c++ instance speed to jog along at
        self.maxrange        = float(maxrange)  # c++ instance Max range
        self.direction       = 1                # c++ instance current direction of rotation
        self.homestate       = 0                # c++ instance is it homed (no home sensor now)
        self.receipt         = 1                # always ask for an update on positions

        # Bokeh bits
        self.spacer          = Spacer(width=self.wwidth, height=5, background='black') #None #

        self.collimator      = Slider    (title=f"Collimator Position", bar_color='firebrick',
                                           value = self.position, start = 0,  end = self.maxrange,
                                           step = 0.01, format="0.000f",width=self.wwidth)

        self.collimatorspeed = Slider    (title=f"Collimator Speed", bar_color='firebrick',
                                           value = self.speed, start = 0,  end = 1,
                                           step = .01, width=self.wwidth)

        self.stepin          = Button    ( label="Step In",  disabled=False, button_type="warning", width=self.wwidth//2)
        self.stepout         = Button    ( label="Step Out", disabled=False, button_type="warning", width=self.wwidth//2)
        self.homebutton      = Button    ( label="Home",     disabled=False, button_type="danger" , width=self.wwidth)

        self.collimator       .on_change('value', lambda attr, old, new: self.update_collimator   (attr, old, new))
        self.collimatorspeed  .on_change('value', lambda attr, old, new: self.update_speed        (attr, old, new))
        self.stepin           .on_click (lambda : self.update_stepin())
        self.stepout          .on_click (lambda : self.update_stepout())
        self.homebutton       .on_click (lambda : self.update_homebutton())

    ### Collimator.__init__()

    def debug(self,msg="",skip=[],os=sys.stderr):               # Collimator::debug()
        """Help with momentary debugging, file to fit.
           msg  -- special tag for this call
           skip -- the member variables to ignore
           os   -- output stream: may be IOStream etc.
        """
        import pprint
        print("Collimator - %s " % msg, file=os)
        for key,value in self.__dict__.items():
            if(key in skip):
               continue
            print(f'{key:20s} =',file=os,end='')
            pprint.pprint(value,stream=os,indent=4)
        return self

    ### Collimator.debug()

    def update_collimator(self, attr,old,new):                  # Collimator::update_collimator()
        """Update the position"""
        self.position = float(new)

    ### Collimator.update_collimator()

    def update_speed(self, attr,old,new):                       # Collimator::update_speed()
        """Update the speed"""
        self.speed = float(new)

    ### Collimator.update_speed()

    def update_stepin(self):                                    # Collimator::update_stepin()
        """Update direction to move"""
        self.direction = 0
        newposition = self.position - (self.speed * self.collimator.step)
        if(newposition >= 0):
            self.position         = newposition
            self.collimator.value = newposition
            self.send_state()

    ### Collimator.update_stepin()

    def update_stepout(self):                                   # Collimator::update_stepout()
        """Calculate and update the position"""
        self.direction = 1
        newposition = self.position + (self.speed * self.collimator.step)
        if(newposition < self.maxrange):
            self.position         = newposition
            self.collimator.value = newposition
            self.send_state()

    ### Collimator.update_stepout()

    def update_homebutton(self):                                # Collimator::update_homebutton()
        """Send a home command"""
        self.send_home()

    ### Collimator.update_homebutton()

    def send_home(self):                                        # Collimator::send_home()
        """Send a Home Command"""
        self.home      = 1
        self.send_state()
        self.homestate = 0
    ### Collimator.send_home()

    def send_state(self):                                       # Collimator::send_state()
        """Several ways to send things"""
        devstate = dict( [ ( "position" , f"{self.position:7.4f}"   ),
                           ( "direction", f"{int(self.direction):d}"),
                           ( "speed"    , f"{self.speed:3f}"        ),
                           ( "home"     , f"{self.homestate:d}"     ),
                           ( "receipt"  , f"{self.receipt:d}"       )
                        ])
        gadgetcmd          = dict([("process"         , devstate)])
        d2                 = dict([(f"{self.instrument.flexname}"    , gadgetcmd)])
        jdict              = json.dumps(d2)
        self.display.display(f'{jdict}')

    ### Collimator.send_state()

    def layout(self):                                           # Collimator::layout()
        """Create the layout"""
        return(row ( column ( self.collimator,
                              self.collimatorspeed,
                              row(self.stepin,self.stepout),
                              self.homebutton
                            )
               ))

    ### Collimator.layout()

# class Collimator

##############################################################################
#                                    Main
#                               Regression Tests
##############################################################################
# HEREHEREHERE
if (0):  # set to 1 for bokeh server regression test
    opts = optparse.OptionParser(usage="%prog "+__doc__)

    opts.add_option("-v", "--verbose", action="store_true", dest="verboseflag",
                   default=False,
                   help="<bool>     be verbose about work.")

    (options, args) = opts.parse_args()

    display        = FlexPublish("Collimator Test")
    collimator     = Collimator("FlexSpec_Rodda",display=display)
    curdoc().theme = 'dark_minimal'
    curdoc().title = "Collimator Test"
    curdoc().add_root(row(collimator.layout(), display.layout()))


