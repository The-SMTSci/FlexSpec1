#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# bokeh serve ./SlitBokeh.py
# (wg-python-fix-pdbrc)

### HEREHEREHERE

import os
import optparse
import sys
import io
import re
import json
from Display import fakedisplay

from bokeh.events   import ButtonClick
from bokeh.io       import curdoc
from bokeh.layouts  import column, row, Spacer
from bokeh.models   import ColumnDataSource, Div, Slider, TextInput, Button
from bokeh.models   import RadioGroup
from bokeh.models   import Select

#from bokeh.models.widgets import Tabs, Panel

#############################################################################
#
#  /home/git/external/xxx.SAS_NA1_3D_Spectrograph/Code/NA1Focus/SlitBokeh.py
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

/home/git/external/xxx.SAS_NA1_3D_Spectrograph/Code/NA1Focus/SlitBokeh.py
[options] files...

This class displays a rate field, a state field (on/off) and
a small error text field.

A little documentation help.
(wg-browser "https://docs.bokeh.org/en/latest/docs/reference.html#refguide")

Slit is a tiny class, that should be part of every Arduino, giving the
user the ability to start a LED blinking.

The blink pattern is on for a duration, off for a duration, and
a pause between the on/off states. I can make a short pulse
every 10 seconds or every 1 second. (The off specification).

Slit Description:

The Flex Spec Ovio holder has one position Dark.
The home position is set to that


Kzin Ring Assy.

"""

__author__  = 'Wayne Green'
__version__ = '0.1'
__all__     = ['BokehOVIOSlit','BokehOVIOSlitException']   # list of quoted items to export

# (wg-python-class "BokehOVIOSlit")
##############################################################################
# BokehOVIOSlitException
#
##############################################################################
class BokehOVIOSlitException(Exception):
    """Special exception to allow differentiated capture of exceptions"""
    def __init__(self,message,errors=None):
        super(BokehOVIOSlitException,self).__init__("FlexSlit "+ message)
        self.errors = errors
    @staticmethod
    def __format__(e):
        return f" FlexSlit: {e.__str__()}\n"
# BokehOVIOSlitException

##############################################################################
# BokehOVIOSlit
#
##############################################################################
class BokehOVIOSlit(object):
    """ A small class to blink the led, with varying rate
    """

    # FAKE up some enums.
    brre     = re.compile(r'\n')                         # used to convert newline to <br/>

    ovioslittuples = [ ( "1"   ,   "10"  ),
                       ( "2"   ,   "20"  ),
                       ( "3"   ,   "30"  ),
                       ( "4"   ,   "40"  ),
                       ( "5"   ,   "50"  ),
                       ( "6"   ,   "70"  ),
                       ( "7"   ,   "100" ),
                       ( "8"   ,   "150" ),
                       ( "9"   ,   "200" ),
                       ( "10"  ,   "300" ),
                       ( "11"  ,   "500" ),   # masked out in FlexSpec "Dark"
                       ( "12"  ,   "700" )
                     ]

    oviodropdowns = [   "10" ,
                        "20" ,
                        "30" ,
                        "40" ,
                        "50" ,
                        "70" ,
                        "100",
                        "150",
                        "200",
                        "300",
                        "Shutter",
                        "700"
                     ]

    #__slots__ = [''] # add legal instance variables
    # (setq properties `("" ""))
    def __init__(self, name : str = "Default",
                 display = fakedisplay,
                 width=200): # BokehOVIOSlit::__init__()
        """Initialize this class."""
        #super().__init__()
        # (wg-python-property-variables)
        self.display     = display
        self.name        = name
        self.wwidth      = width
        self.slit        = "20"
        self.state       = 'undefined'
        self.lamp        = 0
        self.validp      = False                   # wake up in false position
        self.spacer      = Spacer(width=self.wwidth, height=5, background='black')
        self.slitlamp    = RadioGroup(labels=[f"Illuminator Off", f"Illuminator On" ],
                                      height=50, width=self.wwidth, active=0, orientation='horizontal')

        self.slitchoices = Select(title=f"OVIO Slits",value='20',options=self.oviodropdowns, width=self.wwidth)
        self.slitchoices .on_change('value',lambda attr, old, new: self.update_dropdown   (attr, old, new))
        self.slitlamp    .on_change('active', lambda attr, old, new: self.radio_handler   (attr, old, new))
        self.send_state()

    ### BokehOVIOSlit.__init__()

    def radio_handler(self,attr, old, new):                     # BokehFlexBlinky::radio_handler()
        """Do something about the blink via an event lambda"""
        self.lamp = new # self.blink_group.active
        if(self.lamp not in [0,1]):
            self.lamp = 3
        self.send_state()

    ### BokehOVIOSlit.radio_handler()

    def update_dropdown(self,attr,old,new):                     # BokehRoboFocuser::update_button_in()
        """update_debugbtn Button via an event lambda"""
        self.slit = new # self.slitchoices.value
        self.send_state() # display(f"{self.slit}")

    ### BokehOVIOSlit.display()

    def send_state(self):                                       # BokehOVIOSlit::send_state()
        """Several ways to send things"""
        cmddict = dict( [ ( "slit"  , self.slit),  # ascii text of the slit width.
                          ( "illuminator"  , self.lamp)
                         ])
        d2 = dict([(f"{self.name}", dict([("Process", cmddict)]))])
        jdict = json.dumps(d2)
        self.display.display(f'{{ {jdict} , "returnreciept" : 1 }}')

    ### BokehOVIOSlit.send_state()

    def layout(self):                                           # BokehOVIOSlit::layout()
        """Get the layout in gear"""
        return(row ( column ( self.slitchoices,
                              self.slitlamp
                            )  ))

    ### BokehOVIOSlit.layout()

    def debug(self,msg="",skip=[],os=sys.stderr):               # BokehOVIOSlit::debug()
        """Help with momentary debugging, file to fit.
           msg  -- special tag for this call
           skip -- the member variables to ignore
           os   -- output stream: may be IOStream etc.
        """
        import pprint
        print("BokehOVIOSlit - %s " % msg, file=os)
        for key,value in self.__dict__.items():
            if(key in skip):
               continue
            print(f'{key:20s} =',file=os,end='')
            pprint.pprint(value,stream=os,indent=4)
        return self

    ### BokehOVIOSlit.debug()

    __BokehOVIOSlit_debug = debug  # really preserve our debug name if we're inherited

   # (wg-python-properties properties)

# class BokehOVIOSlit

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
    curdoc().title = "Slit1 Test"
    slits = BokehOVIOSlit("FlexSpec_Rodda")
    curdoc().add_root(row(slits.layout()))
