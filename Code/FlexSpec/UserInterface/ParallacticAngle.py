#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# (wg-python-fix-pdbrc)
#
# (compile (format "python -m py_compile %s" (buffer-file-name)))
# (compile (format "pydoc3 " (buffer-file-name) ))
#
### HEREHEREHERE

import os
import optparse
import sys
import re
import json
from FlexPublish          import fakedisplay
from Flex_Instrument      import Flex_Instrument

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
#
# (wg-python-toc)
#
# __doc__ = """
# __author__  = 'Wayne Green'
# __version__ = '0.1'
# __all__     = ['FlexOrientationException','FlexOrientation']   # list of quoted items to export
# class FlexOrientationException(Exception):
#     def __init__(self,message,errors=None):
#     @staticmethod
#     def __format__(e):
# class FlexOrientation(object):
#     #__slots__ = [''] # add legal instance variables
#     def __init__(self,                                          # FlexOrientation::__init__()
#     def update_homebutton(self):                                # FlexOrientation::update_homebutton()
#     def update_readbutton(self):                                # FlexOrientation::update_readbutton()
#     def debug(self,msg="",skip=[],os=sys.stderr):               # FlexOrientation::debug()
#     def update_parallacticangle(self, attr,old,new):            # FlexOrientation::update_parallacticangle()
#     def ExtProcess(self, newvalue):                             # FlexOrientation::ExtProcess()
#     def send_state(self):                                       # ParallacticAngle::send_state()
#     def layout(self):                                           # FlexOrientation::layout()
#
#
#
#############################################################################
__doc__ = """

/home/git/external/SAS_NA1_3D_Spectrograph/Code/FlexOrientation.py
[options] files...

Manage Parallactic Angle for the FlexSpec1 bokeh GUI.

"""

__author__  = 'Wayne Green'
__version__ = '0.1'
__all__     = ['FlexOrientationException','FlexOrientation']   # list of quoted items to export


##############################################################################
# FlexOrientationException
#
##############################################################################
class FlexOrientationException(Exception):
    """Special exception to allo
w differentiated capture of exceptions"""
    def __init__(self,message,errors=None):
        super(FlexOrientationException,self).__init__("FlexOrientation "+ message)
        self.errors = errors
    @staticmethod
    def __format__(e):
        return f" FlexOrientation: {e.__str__()}\n"
# FlexOrientationException

##############################################################################
# FlexOrientation
#
##############################################################################
class FlexOrientation(object):
    """ Manage the Orientation of a Nano
    """
    #__slots__ = [''] # add legal instance variables
    # (setq properties `("" ""))
    def __init__(self,instrument : 'Flex_Instrument',      # FlexOrientation::__init__()
                 name     : str               = "pangle",      # The internal device name
                 display  : 'Flex_Publish'    = fakedisplay,   # display for results
                 pangle   : str               = "0.0",         # The parallactic angle in fraction degrees
                 width    : int               = 200):          # the width for bokeh display
        """Initialize this class."""
        #super().__init__()
        # (wg-python-property-variables)
        self.instrument       = instrument
        self.name             = name
        self.display          = display
        self.wwidth           = width
        self.pangle           = float(pangle)
        self.home             = 0
        self.receipt          = 1                              # always ask for an update
        self.read             = 0
        self.spacer           = Spacer(width=self.wwidth, height=5, background='black')

        self.parallacticangle = Slider    (title=f"Parallactic Angle", bar_color='firebrick',
                                           value = self.pangle, start = 0,  end = 180,
                                           step = 0.1, width=self.wwidth)
        self.readbutton       = Button    ( label="Read",     disabled=False, button_type="success", width=self.wwidth)
        self.homebutton       = Button    ( label="Home",     disabled=False, button_type="danger",  width=self.wwidth//2)

        self.parallacticangle .on_change('value', lambda attr, old, new: self.update_parallacticangle      (attr, old, new))

        self.readbutton       .on_click(lambda : self.update_readbutton ())
        self.homebutton       .on_click(lambda : self.update_homebutton ())

    ### FlexOrientation.__init__()

    def update_homebutton(self):                                # FlexOrientation::update_homebutton()
        """Update the home command. """
        self.home = 1                                  # home for sure
        self.send_state()
        self.home = 0                                  # but reset no matter what

    ### FlexOrientation.update_homebutton()

    def update_readbutton(self):                                # FlexOrientation::update_readbutton()
        """Update the read command. """
        self.read = 1                                  # read
        self.send_state()
        self.read = 0                                  # but reset no matter what

    ### FlexOrientation.update_readbutton()

    def debug(self,msg="",skip=[],os=sys.stderr):               # FlexOrientation::debug()
        """Help with momentary debugging, file to fit.
           msg  -- special tag for this call
           skip -- the member variables to ignore
           os   -- output stream: may be IOStream etc.
        """
        import pprint
        print("FlexOrientation - %s " % msg, file=os)
        for key,value in self.__dict__.items():
            if(key in skip):
               continue
            print(f'{key:20s} =',file=os,end='')
            pprint.pprint(value,stream=os,indent=4)
        return self

    ### FlexOrientation.debug()

    def update_parallacticangle(self, attr,old,new):            # FlexOrientation::update_parallacticangle()
        """Update the parallactic angle. Disabled in interface"""
        self.pangle = new                              # grab new value from the widget

    ### FlexOrientation.update_parallacticangle()

    def ExtProcess(self, newvalue):                             # FlexOrientation::ExtProcess()
        """Process JSON string to update the display. Called from external process."""
        self.parallacticangle.value = float(new)
        self.display.display(newvalue)

    ### FlexOrientation.ExtProcess()

    def send_state(self):                                       # ParallacticAngle::send_state()
        """Several ways to send things

        """
        devstate           = dict( [ ( "read"    , f"{self.read:d}"),   # '"%d"'    % self.read),
                                     ( "home"    , f"{self.home:d}"),   # '"%d"'    % self.home),
                                     ( "pangle"  , f"{self.pangle}"),   # '"%f7.3"' % self.pangle),
                                     ( "receipt" , f"{self.receipt:d}") # '"%d"'    % self.receipt)
                                   ])
        gadgetcmd          = dict([("process", devstate)])
        d2                 = dict([(f"{self.name}", gadgetcmd)])
        d3                 = dict([(f"{self.instrument.flexname}", d2)])
        jdict              = json.dumps(d3)
        self.display.display(f'{jdict}')

    ### ParallacticAngle.send_state()

    def layout(self):                                           # FlexOrientation::layout()
        """Create the layout"""
        return(row ( column ( self.parallacticangle,
                              self.readbutton
                            )  ))

    ### FlexOrientation.layout()

# class FlexOrientation

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

    display        = FlexPublish("FlexOrientation Test")
    pangle         = FlexOrientation("FlexSpec_Rodda",display=display)
    curdoc().theme = 'dark_minimal'
    curdoc().title = "Pangle Test"
    curdoc().add_root(row(pangle.layout()))


