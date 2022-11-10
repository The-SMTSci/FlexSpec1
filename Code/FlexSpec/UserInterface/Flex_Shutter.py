#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# FlexSpec1/Code/FlexSpec/UserInterface/Shutter.py
# (wg-python-fix-pdbrc)
# (compile (format "python -m py_compile %s" (buffer-file-name)))
# (compile (format "pydoc3 %s" (buffer-file-name)))

### HEREHEREHERE

import os
import optparse
import sys
import re
from FlexPublish          import fakedisplay
import json


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
#  /home/git/external/SAS_NA1_3D_Spectrograph/Code/FlexOrientation.py
#
#emacs helpers
# (wg-python-toc)
#
# __doc__ = """
# __author__  = 'Wayne Green'
# __version__ = '0.1'
# __all__     = ['Flex_ShutterException','Flex_Shutter']   # list of quoted items to export
# class Flex_ShutterException(Exception):
#     def __init__(self,message,errors=None):
#     @staticmethod
#     def __format__(e):
# class Flex_Shutter(object):
#     #__slots__ = [''] # add legal instance variables
#     def __init__(self, flexname :'Flex_Instrument',  # Flex_Shutter::__init__()
#     def update_closebutton(self):                               # Flex_Shutter::update_closebutton()
#     def update_openbutton(self):                                # Flex_Shutter::update_openbutton()
#     def debug(self,msg="",skip=[],os=sys.stderr):               # Flex_Shutter::debug()
#     def send_state(self):                                       # FlexSShutter::send_state()
#     def layout(self):                                           # Flex_Shutter::layout()
#
#
# 2022-11-10T08:24:34-0700 wlg
#############################################################################
__doc__ = """

/home/git/external/SAS_NA1_3D_Spectrograph/Code/Flex_Shutter.py
[options] files...

Manage a shutter control for the FlexSpec Bokeh GUI


"""

__author__  = 'Wayne Green'
__version__ = '0.1'
__all__     = ['Flex_ShutterException','Flex_Shutter']   # list of quoted items to export


##############################################################################
# Flex_ShutterException
#
##############################################################################
class Flex_ShutterException(Exception):
    """Special exception to allo
w differentiated capture of exceptions"""
    def __init__(self,message,errors=None):
        super(Flex_ShutterException,self).__init__("Flex_Shutter "+ message)
        self.errors = errors
    @staticmethod
    def __format__(e):
        return f" Flex_Shutter: {e.__str__()}\n"
# Flex_ShutterException

##############################################################################
# Flex_Shutter
#
##############################################################################
class Flex_Shutter(object):
    """ Manage the Orientation of a Nano
    """
    #__slots__ = [''] # add legal instance variables
    # (setq properties `("" ""))
    def __init__(self, flexname :'Flex_Instrument',  # Flex_Shutter::__init__()
                 gadgetname = "shutter",
                 display = fakedisplay,
                 width : int = 250
               ): 
        """Initialize this class."""
        #super().__init__()
        # (wg-python-property-variables)
        self.flexname     = flexname              # The instrument -- if user changes name we know it
        self.name         = gadgetname            # the target gadget in the Arduino
        self.display      = display               # the displayer we're using
        self.wwidth       = width                 # the width for this display widget
        self.openshutter  = 0                     # states of the buttons init to both off == unknown
        self.closeshutter = 0

        self.openbutton   = Button    ( label="Open",      disabled=False, button_type="success",  width=self.wwidth//2)
        self.closebutton  = Button    ( label="Close",     disabled=False, button_type="danger", width=self.wwidth//2)

        self.row           = row()
        self.background   = 'lime'

        self.openbutton   .on_click(lambda : self.update_openbutton ())
        self.closebutton  .on_click(lambda : self.update_closebutton ())

    ### Flex_Shutter.__init__()

    def update_closebutton(self):                               # Flex_Shutter::update_closebutton()
        """Update the home command. """
        self.closeshutter = 1
        self.send_state()
        self.closeshutter = 0

    ### Flex_Shutter.update_closebutton()

    def update_openbutton(self):                                # Flex_Shutter::update_openbutton()
        """Update the read command. """
        self.openshutter = 1
        self.send_state()
        self.openshutter = 0

    ### Flex_Shutter.update_openbutton()

    def debug(self,msg="",skip=[],os=sys.stderr):               # Flex_Shutter::debug()
        """Help with momentary debugging, file to fit.
           msg  -- special tag for this call
           skip -- the member variables to ignore
           os   -- output stream: may be IOStream etc.
        """
        import pprint
        print("Flex_Shutter - %s " % msg, file=os)
        for key,value in self.__dict__.items():
            if(key in skip):
               continue
            print(f'{key:20s} =',file=os,end='')
            pprint.pprint(value,stream=os,indent=4)
        return self

    ### Flex_Shutter.debug()

    def send_state(self):                                       # FlexSShutter::send_state()
        """Several ways to send things
        """
        devstate   = dict( [ ( "open"    , f'{self.openshutter}' ),  # quoted ascii numbers
                             ( "close"   , f'{self.closeshutter}'),
                             ( "receipt" , "1")
                           ])
        shuttercmd = dict([  ( "process"         , devstate)  ])   # Walk the parcel into existance.
        d2         = dict([  (f"{self.name}"     , shuttercmd)])
        d3         = dict([  (f"{self.flexname.flexname}" , d2)        ])

        jdict      = json.dumps(d3)

        self.display.display(f'{jdict}')

    ### Flex_Shutter.send_state()

    def layout(self):                                           # Flex_Shutter::layout()
        """Create the layout"""
        return(row ( column ( Spacer(width=self.wwidth, height=1),
                              row(self.closebutton, self.openbutton, background=self.background)
                            )
              ))

    ### Flex_Shutter.layout()

# class Flex_Shutter

##############################################################################
#                                    Main
#                               Regression Tests
##############################################################################
# HEREHEREHERE
if (0):  # set to 1 for hokeh regression test
    opts = optparse.OptionParser(usage="%prog "+__doc__)

    opts.add_option("-v", "--verbose", action="store_true", dest="verboseflag",
                   default=False,
                   help="<bool>     be verbose about work.")

    (options, args) = opts.parse_args()

    display        = FlexPublish("Flex_Shutter Test")
    shutter         = Flex_Shutter("FlexSpec_Rodda",display=display)
    curdoc().theme = 'dark_minimal'
    curdoc().title = "Shutter Test"
    curdoc().add_root(row(shutter.layout()))


