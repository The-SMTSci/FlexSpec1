#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# (wg-python-fix-pdbrc)

### HEREHEREHERE

import os
import optparse
import sys
import re
import numpy as np
import pandas as pd
import json
from FlexPublish          import fakedisplay


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

from typing import NewType, TypeVar
npRadianArray = NewType('bpRadianArray',np.array)  # define some better module types
millimeter    = TypeVar('millimeter',int, float)
centimeter    = TypeVar('centimeter',int, float)
angstrom      = NewType('angstrom', float)
percent       = TypeVar('percent',int,float)

#############################################################################
#
#  /home/git/external/SAS_NA1_3D_Spectrograph/Code/Guider.py
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

/home/git/external/SAS_NA1_3D_Spectrograph/Code/Guider.py
[options] files...



"""


__author__  = 'Wayne Green'
__version__ = '0.1'
__all__     = ['GuiderException','Guider']   # list of quoted items to export


##############################################################################
# GuiderException
#
##############################################################################
class GuiderException(Exception):
    """Special exception to allo
w differentiated capture of exceptions"""
    def __init__(self,message,errors=None):
        super(GuiderException,self).__init__("Guider "+ message)
        self.errors = errors
    @staticmethod
    def __format__(e):
        return f" Guider: {e.__str__()}\n"
# GuiderException


##############################################################################
# Guider
#
##############################################################################
class Guider(object):
    """ Manage the Orientation of a Nano
    """
    #__slots__ = [''] # add legal instance variables
    # (setq properties `("" ""))

    brre     = re.compile(r'\n')                         # used to convert newline to <br/>

    def __init__(self, instrument : 'Flex_Instrumentstr',# Guider::__init__()
                 name : str = "Guider",
                 display = fakedisplay,
                 position : str = "0.0",
                 maxrange : float = 1.5, width : int = 200):  
        """Initialize this class."""
        #super().__init__()
        # (wg-python-property-variables)
        self.instrument  = instrument          # name of this instrument
        self.name        = name              # name this instance recognizes
        self.display     = display           # where to put debug info

        self.position    = float(position)   # state variables
        self.direction   = 1                 # tied to step/in step/out buttons
        self.speed       = 0.10              # fraction of the speed to move
        self.homestate   = 0                 # a tristate by convention

        self.wwidth      = width             # interval variables
        self.maxrange    = float(maxrange)

        self.spacer      = Spacer(width=self.wwidth, height=5, background='black') # None #

        self.guider      = Slider    (title=f"Guider Position", bar_color='firebrick',
                                           value = self.position, start = 0,  end = self.maxrange,
                                           step = 0.01, format="0.000f",width=self.wwidth)
        self.guiderspeed = Slider    (title=f"Guider Speed", bar_color='firebrick',
                                           value = self.speed, start = 0,  end = 1,
                                           step = .01, width=self.wwidth)
        self.stepin      = Button    ( label="Step In",  disabled=False, button_type="warning", width=self.wwidth//2)
        self.stepout     = Button    ( label="Step Out", disabled=False, button_type="warning", width=self.wwidth//2)
        self.homebutton  = Button    ( label="Home",     disabled=False, button_type="danger", width=self.wwidth)

        self.guider       .on_change ('value', lambda attr, old, new: self.update_guider      (attr, old, new))
        self.guiderspeed  .on_change ('value', lambda attr, old, new: self.update_speed       (attr, old, new))
        self.stepin       .on_click  (lambda : self.update_stepin()     )
        self.stepout      .on_click  (lambda : self.update_stepout()    )
        self.homebutton   .on_click  (lambda : self.update_homebutton() )

    ### Guider.__init__()

    def debug(self,msg="",skip=[],os=sys.stderr):               # Guider::debug()
        """Help with momentary debugging, file to fit.
           msg  -- special tag for this call
           skip -- the member variables to ignore
           os   -- output stream: may be IOStream etc.
        """
        import pprint
        print("Guider - %s " % msg, file=os)
        for key,value in self.__dict__.items():
            if(key in skip):
               continue
            print(f'{key:20s} =',file=os,end='')
            pprint.pprint(value,stream=os,indent=4)
        return self

    ### Guider.debug()

    def update_guider(self, attr,old,new):                      # Guider::update_guider()
        """Update the parallactic angle. Disabled in interface"""
        self.position = float(new)

    ### Guider.update_guider()

    def update_speed(self, attr,old,new):                       # Guider::update_speed()
        """Update the parallactic angle. Disabled in interface"""
        self.speed = float(new)

    ### Guider.update_speed()

    def update_stepin(self):                                    # Guider::update_stepin()
        """Update the parallactic angle. Disabled in interface"""
        self.direction = 0
        newposition = self.position - (self.speed * self.guider.step)
        if(newposition >= 0):
            self.position = newposition
            self.guider.value = newposition
            self.send_state()

    ### Guider.update_stepin()

    def update_stepout(self):                                   # Guider::update_stepout()
        """Update the parallactic angle. Disabled in interface"""
        self.direction = 1
        newposition = self.position + (self.speed * self.guider.step)
        if(newposition < self.maxrange):
            self.position = newposition
            self.guider.value = newposition
            self.send_state()

    ### Guider.update_stepout()

    def update_homebutton(self):                                # Guider.update_homebutton()
        """Send a home command"""
        self.homestate = 1
        self.send_state()
        self.homestate = 0         # clear home, it should have been sent.

    ### Guider.update_homebutton()

#    def send_home(self):                                        # Guider.send_home()
#        """Send a Home Command"""
#        cmddict = dict( [ ( "guiderhome"  , 1)      # just a home command
#                         ])
#        d2 = dict([(f"{self.name}", dict([("Process", cmddict)]))])
#        jdict = json.dumps(d2)
#        self.display.display(f'{{ {jdict} , "returnreceipt" : 1 }}')

    ### Guider.send_home()

    def send_state(self):                                       # Guider.send_state()
        """Several ways to send things"""
        devstate = dict( [( "position" , f"{self.position:7.4f}"),
                          ( "direction", int(self.direction)),
                          ( "speed"    , self.speed),
                          ( "home"     , self.homestate)
                        ])
        slitcmd = dict([("process", devstate), ("receipt" , 0)])
        slitcmd['receipt'] = 1                             # set the receipt as desired
        d2 = dict([(f"{self.name}", slitcmd)])
        d3 = dict([(f"{self.instrument.flexname}", d2)])
        jdict = json.dumps(d3)
        self.display.display(f'{jdict}')

    ### Guider.send_state()

    def layout(self):                                           # Guider::layout()
        """Create the layout"""
        return(row ( column ( self.guider,
                              self.guiderspeed,
                              row(self.stepin,self.stepout),
                              self.homebutton
                            )  ))

    ### Guider.layout()

# class Guider

##############################################################################
#                                    Main
#                               Regression Tests
##############################################################################
# HEREHEREHERE
if (0):  #  __name__ == "__main__":
    opts = optparse.OptionParser(usage="%prog "+__doc__)

    opts.add_option("-v", "--verbose", action="store_true", dest="verboseflag",
                   default=False,
                   help="<bool>     be verbose about work.")

    (options, args) = opts.parse_args()

    curdoc().theme = 'dark_minimal'
    curdoc().title = "Pangle Test"
    guider = Guider("FlexSpec_Rodda")
    curdoc().add_root(row(guider.layout()))


