#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# FlexSpec1/Code/FlexSpec/UserInterface/Shutter.py 
# (wg-python-fix-pdbrc)

### HEREHEREHERE

import os
import optparse
import sys
import re
from Display import fakedisplay
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

/home/git/external/SAS_NA1_3D_Spectrograph/Code/FlexShutter.py
[options] files...



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
        self.pangle       = float(pangle)
        self.openshutter  = 0
        self.closeshutter = 0
        self.spacer       = Spacer(width=self.wwidth, height=5, background='black')


        self.parallacticangle = Slider    (title=f"Shutter", bar_color='firebrick',
                                           value = self.pangle, start = 0,  end = 180,
                                           step = 0.1, width=self.wwidth)
        self.openbutton       = Button    ( label="Open",      disabled=False, button_type="danger",  width=self.wwidth//2)
        self.closebutton      = Button    ( label="Close",     disabled=False, button_type="success", width=self.wwidth//2)

        self.parallacticangle .on_change('value', lambda attr, old, new: self.update_parallacticangle      (attr, old, new))

        self.openbutton       .on_click(lambda : self.update_openbutton ())
        self.closebutton      .on_click(lambda : self.update_closebutton ())

    ### FlexShutter.__init__()

    def update_closebutton(self):                                # FlexShutter::update_closebutton()
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

    def update_parallacticangle(self, attr,old,new):            # FlexShutter::update_parallacticangle()
        """Update the parallactic angle. Disabled in interface"""
        self.pangle = new

    ### FlexShutter.update_parallacticangle()

    def ExtProcess(self, newvalue):                             # FlexShutter::ExtProcess()
        """Process JSON string to update the display. Called from external process."""
        self.parallacticangle.value = float(new)
        self.display.display(newvalue)

    ### FlexShutter.ExtProcess()

    def send_state(self):                                       # FlexSShutter::send_state()
        """Several ways to send things
        
        """
        devstate = dict( [ ( "open"    , self.openshutter),
                           ( "close"   , self.closeshutter),
                           ( "pangle"  , self.pangle)
                        ])
        slitcmd = dict([("Process", devstate), ("Receipt" , 0)])
        slitcmd['Receipt'] = 1                             # set the receipt as desired
        d2 = dict([(f"{self.name}", slitcmd)])
        d3 = dict([(f"{self.flexname}", d2)])
        jdict = json.dumps(d3)
        self.display.display(f'{jdict}')

    ### FlexSShutter.send_state()

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

    display        = FlexDisplay("FlexShutter Test")
    pangle         = FlexShutter("FlexSpec_Rodda",display=display)
    curdoc().theme = 'dark_minimal'
    curdoc().title = "Pangle Test"
    curdoc().add_root(row(pangle.layout()))


