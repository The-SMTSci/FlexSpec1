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
    def __init__(self, name : str = "Default",
                 display = fakedisplay,
                 pangle : str = "0.0", width=200):  # FlexOrientation::__init__()
        """Initialize this class."""
        #super().__init__()
        # (wg-python-property-variables)
        self.name      = name
        self.display   = display
        self.wwidth    = width
        self.pangle    = float(pangle)
        self.spacer    = Spacer(width=self.wwidth, height=5, background='black')


        self.parallacticangle = Slider    (title=f"Parallactic Angle", bar_color='firebrick',
                                           value = self.pangle, start = 0,  end = 180,
                                           step = 0.1, width=self.wwidth)
        self.homebutton       = Button    ( label="Home",     disabled=False, button_type="danger", width=self.wwidth)

        self.parallacticangle .on_change('value', lambda attr, old, new: self.update_parallacticangle      (attr, old, new))

    ### FlexOrientation.__init__()

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
        pass # self.parallacticangle.value = float(new)

    ### FlexOrientation.update_parallacticangle()

    def ExtProcess(self, newvalue):                             # FlexOrientation::ExtProcess()
        """Process JSON string to update the display. Called from external process."""
        self.parallacticangle.value = float(new)
        self.display.display(newvalue)

    ### FlexOrientation.ExtProcess()

    def layout(self):                                           # FlexOrientation::layout()
        """Create the layout"""
        return(row ( column ( self.parallacticangle,
                              self.homebutton
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


