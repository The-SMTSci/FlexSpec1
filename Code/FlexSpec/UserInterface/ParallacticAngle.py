#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
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
#     def __init__(self, name : str = "Default",
#     def update_homebutton(self):                                # Collimator::update_homebutton()
#     def update_readbutton(self):                                # Collimator::update_readbutton()
#     def debug(self,msg="",skip=[],os=sys.stderr):               # FlexOrientation::debug()
#     def update_parallacticangle(self, attr,old,new):            # FlexOrientation::update_parallacticangle()
#     def ExtProcess(self, newvalue):                             # FlexOrientation::ExtProcess()
#     def layout(self):                                           # FlexOrientation::layout()
#
#
#
#############################################################################
__doc__ = """

/home/git/external/SAS_NA1_3D_Spectrograph/Code/FlexOrientation.py
[options] files...



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
    def __init__(self, flexname : str = "Default",
                 name  = "IMU",
                 display = fakedisplay,
                 pangle : str = "0.0", width=200):  # FlexOrientation::__init__()
        """Initialize this class."""
        #super().__init__()
        # (wg-python-property-variables)
        self.flexname      = flexname
        self.name      = name
        self.display   = display
        self.wwidth    = width
        self.pangle    = float(pangle)
        self.home      = 0
        self.read      = 0
        self.spacer    = Spacer(width=self.wwidth, height=5, background='black')


        self.parallacticangle = Slider    (title=f"Parallactic Angle", bar_color='firebrick',
                                           value = self.pangle, start = 0,  end = 180,
                                           step = 0.1, width=self.wwidth)
        self.readbutton       = Button    ( label="Read",     disabled=False, button_type="warning", width=self.wwidth//2)
        self.homebutton       = Button    ( label="Home",     disabled=False, button_type="danger",  width=self.wwidth//2)

        self.parallacticangle .on_change('value', lambda attr, old, new: self.update_parallacticangle      (attr, old, new))

        self.readbutton       .on_click(lambda : self.update_readbutton ())
        self.homebutton       .on_click(lambda : self.update_homebutton ())

    ### FlexOrientation.__init__()

    def update_homebutton(self):                                # FlexOrientation::update_homebutton()
        """Update the home command. """
        self.home = 1 
        self.send_state()
        self.home = 0

    ### FlexOrientation.update_homebutton()

    def update_readbutton(self):                                # FlexOrientation::update_readbutton()
        """Update the read command. """
        self.read = 1 
        self.send_state()
        self.read = 0

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
        self.pangle = new

    ### FlexOrientation.update_parallacticangle()

    def ExtProcess(self, newvalue):                             # FlexOrientation::ExtProcess()
        """Process JSON string to update the display. Called from external process."""
        self.parallacticangle.value = float(new)
        self.display.display(newvalue)

    ### FlexOrientation.ExtProcess()

    def send_state(self):                                       # ParallacticAngle::send_state()
        """Several ways to send things
        
        """
        devstate           = dict( [ ( "read"    , self.read),
                                     ( "home"    , self.home),
                                     ( "pangle"  , self.pangle)
                                   ])
        slitcmd            = dict([("Process", devstate), ("Receipt" , 0)])
        slitcmd['Receipt'] = 1                             # set the receipt as desired
        d2                 = dict([(f"{self.name}", slitcmd)])
        d3                 = dict([(f"{self.flexname}", d2)])
        jdict              = json.dumps(d3)
        self.display.display(f'{jdict}')

    ### ParallacticAngle.send_state()

    def layout(self):                                           # FlexOrientation::layout()
        """Create the layout"""
        return(row ( column ( self.parallacticangle,
                              row(self.homebutton, self.readbutton)
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

    display        = FlexDisplay("FlexOrientation Test")
    pangle         = FlexOrientation("FlexSpec_Rodda",display=display)
    curdoc().theme = 'dark_minimal'
    curdoc().title = "Pangle Test"
    curdoc().add_root(row(pangle.layout()))


