#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# FlexSpec1/Code/FlexSpec/UserInterface/Shutter.py
# (wg-python-fix-pdbrc)

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
# __all__     = ['FlexShutterException','FlexShutter']   # list of quoted items to export
# class FlexShutterException(Exception):
#     def __init__(self,message,errors=None):
#     @staticmethod
#     def __format__(e):
# class FlexShutter(object):
#     #__slots__ = [''] # add legal instance variables
#     def __init__(self, flexname : str = "Default",
#     def update_closebutton(self):                               # FlexShutter::update_closebutton()
#     def update_openbutton(self):                                # FlexShutter::update_openbutton()
#     def debug(self,msg="",skip=[],os=sys.stderr):               # FlexShutter::debug()
#     def send_state(self):                                       # FlexSShutter::send_state()
#     def layout(self):                                           # FlexShutter::layout()
#
#
#
#############################################################################
__doc__ = """

/home/git/external/SAS_NA1_3D_Spectrograph/Code/FlexShutter.py
[options] files...

Manage a shutter control for the FlexSpec Bokeh GUI


"""

__author__  = 'Wayne Green'
__version__ = '0.1'
__all__     = ['FlexShutterException','FlexShutter']   # list of quoted items to export


##############################################################################
# FlexShutterException
#
##############################################################################
class FlexShutterException(Exception):
    """Special exception to allo
w differentiated capture of exceptions"""
    def __init__(self,message,errors=None):
        super(FlexShutterException,self).__init__("FlexShutter "+ message)
        self.errors = errors
    @staticmethod
    def __format__(e):
        return f" FlexShutter: {e.__str__()}\n"
# FlexShutterException

##############################################################################
# FlexShutter
#
##############################################################################
class FlexShutter(object):
    """ Manage the Orientation of a Nano
    """
    #__slots__ = [''] # add legal instance variables
    # (setq properties `("" ""))
    def __init__(self, flexname : str = "Default",
                 name  = "Shutter",
                 display = fakedisplay,
                 pangle : str = "0.0", width=200):  # FlexShutter::__init__()
        """Initialize this class."""
        #super().__init__()
        # (wg-python-property-variables)
        self.flexname     = flexname
        self.name         = name
        self.display      = display
        self.wwidth       = width
        self.openshutter  = 0
        self.closeshutter = 0
        self.spacer       = Spacer(width=self.wwidth, height=5, background='black')


        self.openbutton       = Button    ( label="Open",      disabled=False, button_type="danger",  width=self.wwidth//2)
        self.closebutton      = Button    ( label="Close",     disabled=False, button_type="success", width=self.wwidth//2)

        self.openbutton       .on_click(lambda : self.update_openbutton ())
        self.closebutton      .on_click(lambda : self.update_closebutton ())

    ### FlexShutter.__init__()

    def update_closebutton(self):                               # FlexShutter::update_closebutton()
        """Update the home command. """
        self.closeshutter = 1
        self.send_state()
        self.closeshutter = 0

    ### FlexShutter.update_closebutton()

    def update_openbutton(self):                                # FlexShutter::update_openbutton()
        """Update the read command. """
        self.openshutter = 1
        self.send_state()
        self.openshutter = 0

    ### FlexShutter.update_openbutton()

    def debug(self,msg="",skip=[],os=sys.stderr):               # FlexShutter::debug()
        """Help with momentary debugging, file to fit.
           msg  -- special tag for this call
           skip -- the member variables to ignore
           os   -- output stream: may be IOStream etc.
        """
        import pprint
        print("FlexShutter - %s " % msg, file=os)
        for key,value in self.__dict__.items():
            if(key in skip):
               continue
            print(f'{key:20s} =',file=os,end='')
            pprint.pprint(value,stream=os,indent=4)
        return self

    ### FlexShutter.debug()

    def send_state(self):                                       # FlexSShutter::send_state()
        """Several ways to send things
        """
        devstate = dict( [ ( "open"    , '"d"' % self.openshutter),  # quoted ascii numbers
                           ( "close"   , '"d"' % self.closeshutter)
                        ])
        slitcmd = dict([("Process", devstate), ("Receipt" , "1")])
        d2 = dict([(f"{self.name}",     slitcmd)])
        d3 = dict([(f"{self.flexname}", d2)])
        jdict = json.dumps(d3)
        self.display.display(f'{jdict}')

    ### FlexShutter.send_state()

    def layout(self):                                           # FlexShutter::layout()
        """Create the layout"""
        return(row ( column ( self.parallacticangle,
                              row(self.closebutton, self.openbutton)
                            )  ))

    ### FlexShutter.layout()

# class FlexShutter

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

    display        = FlexPublish("FlexShutter Test")
    pangle         = FlexShutter("FlexSpec_Rodda",display=display)
    curdoc().theme = 'dark_minimal'
    curdoc().title = "Pangle Test"
    curdoc().add_root(row(pangle.layout()))


