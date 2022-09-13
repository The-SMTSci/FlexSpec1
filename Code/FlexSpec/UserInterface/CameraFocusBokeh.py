#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# bokeh serve ./LampBokeh.py
# (wg-python-fix-pdbrc)

### HEREHEREHERE

import os
import optparse
import sys
import io
import re
import json
from FlexPublish          import fakedisplay


from bokeh                import events
from bokeh.events         import ButtonClick
from bokeh.io             import curdoc
from bokeh.layouts        import column, row, Spacer
from bokeh.models         import CheckboxButtonGroup,ColumnDataSource, Slider, TextInput, Button
from bokeh.models         import Spacer
from bokeh.models         import CustomJS, Div
from bokeh.plotting       import figure
from bokeh.models         import RadioGroup
from bokeh.models         import Select
from bokeh.models.widgets import Tabs, Panel


#############################################################################
#
#  /home/git/external/SAS_NA1_3D_Spectrograph/Code/LampBokeh.py
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

/home/git/external/SAS_NA1_3D_Spectrograph/Code/CameraFocusBokeh.py

[options] files...

A single Pin to illuminate a special lamp for focusing the science camera
lens.

The buttons are:

   near     --  Calibration Lamp
   osram    --  OSRAM Lamp HV bulb
   halpha   --  Reference Red LED
   oiii     --  Reference ND OIII region
   flat     --  Flat Assy
   augflat  --  Flat Assy with Blue Boost

_near
_osram
_halpha
_oiii
_flat
_augflat



"""


__author__  = 'Wayne Green'
__version__ = '0.1'
__all__     = ['BokehFlexLamp','FlexLampException']   # list of quoted items to export

# (wg-python-class "CameraFocus")
##############################################################################
# CameraFocusException
#
##############################################################################
class CameraFocusException(Exception):
    """Special exception to allow differentiated capture of exceptions"""
    def __init__(self,message,errors=None):
        super(CameraFocusException,self).__init__("CameraFocus "+ message)
        self.errors = errors
    @staticmethod
    def __format__(e):
        return f" CameraFocus: {e.__str__()}\n"
# CameraFocusException

##############################################################################
# CameraFocus
#
##############################################################################
class CameraFocus(object):
    """ A small class to blink the led, with varying rate
    """

    # FAKE up some enums.
    ON          = 0  # CameraFocus.ON
    OFF         = 1  # CameraFocus.OFF
    RUN         = 2  # CameraFocus.RUN
    StateText   = ["Off","On","Illegal"]
    brre        = re.compile(r'\n')                         # used to convert newline to HTML <br/>
    postmessage = { "name"        : "Unassigned",
                    "camerafocus" : None
                    }


    #__slots__ = [''] # add legal instance variables
    # (setq properties `("" ""))
    def __init__(self, name : str = "CameraFocus",
                 display   = fakedisplay,
                 width     = 250,
                 pin=4): # CameraFocus::__init__()
        """Initialize this class."""
        #super().__init__()
        # (wg-python-property-variables)
        self.wwidth         = width
        self.display        = display
        self.name           = name
        self.camerafocus    = 0             # the lamp starts in off position.

        # // coordinate with lampcheckboxes_handler
        self.CBLabels=["CameraFocus"]

        self.LampCheckBoxes = CheckboxButtonGroup(labels=self.CBLabels,
                                                  active=[0]*len(self.CBLabels)
                                                 ) # create/init them
        self.process        = Button    (align='end', label=f"{self.name} On",  disabled=False,
                                                   button_type="success", width=self.wwidth//2)
        self.offbutton      = Button    (align='end', label=f"{self.name} Off",  disabled=False,
                                                   button_type="primary", width=self.wwidth//2)

        self.LampCheckBoxes .on_change('active', lambda attr, old, new: self.lampcheckboxes_handler   (attr, old, new))
        self.process        .on_click (lambda : self.update_process())
        self.offbutton      .on_click (lambda : self.update_offbutton())


    ### CameraFocus.__init__()

    def update_offbutton(self):                                 # CameraFocus::update_offbutton()
        """Set internal variables to off."""
        msg = self.send_off()

    ### CameraFocus.update_offbutton()

    def update_process(self):                                   # CameraFocus::update_button_in()
        """update_process Button via an event lambda"""
        #os = io.StringIO()
        #self.debug(f"{self.name} Debug",skip=['varmap'], os=os)
        #os.seek(0)
        msg = self.send_state()

    ### CameraFocus.update_process()

    def lampcheckboxes_handler(self,attr, old, new):            # CameraFocus::lampcheckboxes_handler()
        """Handle the checkboxes, new is a list of indices into
        self.CBLabels for their purpose"""
        msg = f"attr {attr}, old {old}, new {new}"
        self.camerafocus   = 1 if 0 in new else 0

        #self.display(msg)

    ### CameraFocus.lampcheckboxes_handler()

    def update_debugbtn(self):                                  # CameraFocus::update_button_in()
        """update_debugbtn Button via an event lambda"""
        os = io.StringIO()
        self.debug(f"{self.name} Debug", os=os)
        os.seek(0)
        self.display.display(CameraFocus.brre.sub("<br/>",os.read()))

    ### CameraFocus.update_edebugbtn()

    def send_state(self):                                       # CameraFocus::send_state()
        """Several ways to send things"""
        cmddict = dict( [ ( "camerafocus"   , self.camerafocus)    # nest into message
                        ] )
        d2 = dict([(f"{self.name}", dict([("Process", cmddict)]))])
        jdict = json.dumps(d2)
        self.display.display(f'{{ "{self.name}" : {jdict} , "returnreceipt" : 1 }}')

    ### CameraFocus.send_state()

    def send_off(self):                                         # CameraFocus::send_off()
        """Don't change the internal variables, fake a message to make
        the lamps off."""
        cmddict = dict( [ ("camerafocus"   , 0)
                         ])
        d2      = dict([("camerafocus", dict([("Process", cmddict)]))])
        jdict   = json.dumps(d2)
        self.display.display(f'{{ "{self.name}" : {jdict} , "returnreceipt" : 1 }}')
        return jdict

    ### CameraFocus.send_off(()

    def layout(self):                                           # CameraFocus::layout()
        """Get the layout in gear"""
        return(row ( column ( #self.LampCheckBoxes,
                              row(self.process,self.offbutton)
                            )  ))
        return self

    ### CameraFocus.layout()

    def debug(self,msg="",skip=[],os=sys.stderr):           # CameraFocus::debug()
        """Help with momentary debugging, file to fit.
           msg  -- special tag for this call
           skip -- the member variables to ignore
           os   -- output stream: may be IOStream etc.
        """
        import pprint
        print("CameraFocus - %s " % msg, file=os)
        for key,value in self.__dict__.items():
            if(key in skip):
               continue
            print(f'{key:20s} =',file=os,end='')
            pprint.pprint(value,stream=os,indent=4)
        return self

    ### CameraFocus.debug()

    __CameraFocus_debug = debug  # really preserve our debug name if we're inherited

   # (wg-python-properties properties)

# class CameraFocus

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

    kzin1  = CameraFocus("Tony")
    kzin2  = CameraFocus("Jerry")
    if(0):
        with open('/tmp/debug1.txt','w') as os:
            blink1.debug(msg="Starting with...", os=os)
    l1    = kzin1.layout()
    l2    = kzin2.layout()
    tab1  = Panel(child=l1,title='Tony')
    tab2  = Panel(child=l2,title='Jerry')
    tabs  = Tabs(tabs=[tab1,tab2])
    curdoc().add_root(tabs)

#    curdoc().add_root(column(kzin1.layout(), kzin2.layout()))
#    curdoc().theme = 'dark_minimal'
#    curdoc().title = "Lamp1 Test"
