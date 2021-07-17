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
from Display import fakedisplay        # Display upgrade


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
#  /home/git/external/SAS_NA1_3D_Spectrograph/Code/Collimator.py
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

/home/git/external/SAS_NA1_3D_Spectrograph/Code/Collimator.py
[options] files...



"""


__author__  = 'Wayne Green'
__version__ = '0.1'
__all__     = ['CollimatorException','Collimator']   # list of quoted items to export


##############################################################################
# CollimatorException
#
##############################################################################
class CollimatorException(Exception):
    """Special exception to allo
w differentiated capture of exceptions"""
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

    def __init__(self, name : str = "Default",
                 display = fakedisplay,
                 instrumentname="Collimator",
                 position : str = "0.0",
                 maxrange : float = 1.5, width : int = 200):  # Collimator::__init__()
        """Initialize this class."""
        #super().__init__()
        # (wg-python-property-variables)
        self.name            = name
        self.display         = display
        self.instrumentname  = instrumentname
        self.wwidth          = width
        self.position        = float(position)
        self.speed           = 0.10
        self.maxrange        = float(maxrange)
        self.direction       = 1
        self.spacer          = Spacer(width=self.wwidth, height=5, background='black') #None #

        self.collimator      = Slider    (title=f"Collimator Position", bar_color='firebrick',
                                           value = self.position, start = 0,  end = self.maxrange,
                                           step = 0.01, format="0.000f",width=self.wwidth)
        self.collimatorspeed = Slider    (title=f"Collimator Speed", bar_color='firebrick',
                                           value = self.speed, start = 0,  end = 1,
                                           step = .01, width=self.wwidth)
        self.stepin          = Button    ( label="Step In",  disabled=False, button_type="warning", width=self.wwidth//2)
        self.stepout         = Button    ( label="Step Out", disabled=False, button_type="warning", width=self.wwidth//2)
        self.homebutton      = Button    ( label="Home",     disabled=False, button_type="danger", width=self.wwidth)

        self.collimator       .on_change('value', lambda attr, old, new: self.update_collimator      (attr, old, new))
        self.collimatorspeed  .on_change('value', lambda attr, old, new: self.update_speed       (attr, old, new))
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
        """Update the parallactic angle. Disabled in interface"""
        self.position = float(new)

    ### Collimator.update_collimator()

    def update_speed(self, attr,old,new):                       # Collimator::update_speed()
        """Update the parallactic angle. Disabled in interface"""
        self.speed = float(new)

    ### Collimator.update_speed()

    def update_stepin(self):                                    # Collimator::update_stepin()
        """Update the parallactic angle. Disabled in interface"""
        self.direction = 0
        newposition = self.position - (self.speed * self.collimator.step)
        if(newposition >= 0):
            self.position = newposition
            self.collimator.value = newposition
            self.send_state()

    ### Collimator.update_stepin()

    def update_stepout(self):                                   # Collimator::update_stepout()
        """Update the parallactic angle. Disabled in interface"""
        self.direction = 1
        newposition = self.position + (self.speed * self.collimator.step)
        if(newposition < self.maxrange):
            self.position = newposition
            self.collimator.value = newposition
            self.send_state()

    ### Collimator.update_stepout()

    def update_homebutton(self):                                # Collimator::update_homebutton()
        """Send a home command"""
        self.send_home()

    ### Collimator.update_homebutton()

    def send_home(self):                                        # Collimator::send_home()
        """Send a Home Command"""
        cmddict = dict( [ ( "home"  , 1)      # just a home command
                         ])
        d2 = dict([(f"{self.name}", dict([("Process", cmddict)]))])
        jdict = json.dumps(d2)
        self.display.display(f'{{ {jdict} , "returnreceipt" : 1 }}')

    ### Collimator.send_home()

    def send_state(self):                                       # Collimator::send_state()
        """Several ways to send things"""
        cmddict = dict( [ ( "position" , f"{self.position:7.4f}"),
                          ( "direction", int(self.direction)),
                          ( "speed"    , self.speed)
                        ])
        d2      = dict([(f"{self.name}", dict([("Process", cmddict)]))])
        jdict   = json.dumps(d2)
        self.display.display(f'{{ {jdict} , "returnreceipt" : 1 }}')

    ### Collimator.send_state()

    def layout(self):                                           # Collimator::layout()
        """Create the layout"""
        return(row ( column ( self.collimator,
                              self.collimatorspeed,
                              row(self.stepin,self.stepout),
                              self.homebutton
                            )  ))

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

    display        = FlexDisplay("Collimator Test")
    collimator     = Collimator("FlexSpec_Rodda",display=display)
    curdoc().theme = 'dark_minimal'
    curdoc().title = "Pangle Test"
    curdoc().add_root(row(collimator.layout(), display.layout()))


