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
from Display          import fakedisplay


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

/home/git/external/SAS_NA1_3D_Spectrograph/Code/LampBokeh.py

[options] files...

Treat this as Kzin Ring Assy.

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

# (wg-python-class "FlexLamp")
##############################################################################
# FlexLampException
#
##############################################################################
class FlexLampException(Exception):
    """Special exception to allow differentiated capture of exceptions"""
    def __init__(self,message,errors=None):
        super(FlexLampException,self).__init__("FlexLamp "+ message)
        self.errors = errors
    @staticmethod
    def __format__(e):
        return f" FlexLamp: {e.__str__()}\n"
# FlexLampException

##############################################################################
# BokehFlexLamp
#
##############################################################################
class BokehFlexLamp(object):
    """ A small class to blink the led, with varying rate
    """

    # FAKE up some enums.
    ON          = 0  # BokehFlexLamp.ON
    OFF         = 1  # BokehFlexLamp.OFF
    RUN         = 2  # BokehFlexLamp.RUN
    SateText    = ["Off","On","Illegal"]
    brre        = re.compile(r'\n')                         # used to convert newline to <br/>
    postmessage = { "name"    : "Unassigned",
                    "near"    : None ,
                    "osram"   : None ,
                    "halpha"  : None ,
                    "oiii"    : None ,
                    "flat"    : None ,
                    "augflat" : None
                    }


    #__slots__ = [''] # add legal instance variables
    # (setq properties `("" ""))
    def __init__(self, name : str = "Default",
                 display = fakedisplay,
                 width=250,pin=4): # BokehFlexLamp::__init__()
        """Initialize this class."""
        #super().__init__()
        # (wg-python-property-variables)
        self.wwidth         = width
        self.display        = display
        self.name           = name
        self.display        = display
        self.wheat_value    = 1                 # add a variable for each lamp
        self.osram_value    = 0                 # installed.
        self.halpha_value   = 0
        self.oiii_value     = 0
        self.flat_value     = 0
        self.augflat_value  = 0
        self.near_value     = 0

        # // coordinate with lampcheckboxes_handler
        self.CBLabels=["Wheat", "Osram", "H-alpha", "O[iii]", "Flat", "Blue Flat", "NeAr" ]

        self.LampCheckBoxes = CheckboxButtonGroup(labels=self.CBLabels,
                                                  active=[0]*len(self.CBLabels)
                                                 ) # create/init them
        self.process        = Button    (align='end', label=f"{self.name} On",  disabled=False,
                                                   button_type="success", width=self.wwidth)
        self.offbutton      = Button    (align='end', label=f"{self.name} Off",  disabled=False,
                                                   button_type="primary", width=self.wwidth)

        self.LampCheckBoxes .on_change('active', lambda attr, old, new: self.lampcheckboxes_handler   (attr, old, new))
        self.process        .on_click (lambda : self.update_process())
        self.offbutton      .on_click (lambda : self.update_offbutton())


    ### BokehFlexLamp.__init__()

    def update_offbutton(self):                                 # BokehFlexLamp::update_offbutton()
        """Set internal variables to off."""
        msg = self.send_off()

    ### BokehFlexLamp.update_offbutton()

    def update_process(self):                                   # BokehFlexLamp::update_button_in()
        """update_process Button via an event lambda"""
        #os = io.StringIO()
        #self.debug(f"{self.name} Debug",skip=['varmap'], os=os)
        #os.seek(0)
        msg = self.send_state()

    ### BokehFlexLamp.update_process()

    def lampcheckboxes_handler(self,attr, old, new):            # BokehFlexLamp::lampcheckboxes_handler()
        """Handle the checkboxes, new is a list of indices into
        self.CBLabels for their purpose"""
        msg = f"attr {attr}, old {old}, new {new}"
        self.wheat_value   = 1 if 0 in new else 0
        self.osram_value   = 1 if 1 in new else 0
        self.halpha_value  = 1 if 2 in new else 0
        self.oiii_value    = 1 if 3 in new else 0
        self.flat_value    = 1 if 4 in new else 0
        self.augflat_value = 1 if 5 in new else 0
        self.near_value    = 1 if 6 in new else 0
        #self.display(msg)

    ### BokehFlexLamp.lampcheckboxes_handler()

    def update_debugbtn(self):                                  # BokehFlexLamp::update_button_in()
        """update_debugbtn Button via an event lambda"""
        os = io.StringIO()
        self.debug(f"{self.name} Debug", os=os)
        os.seek(0)
        self.display.display(BokehFlexLamp.brre.sub("<br/>",os.read()))

    ### BokehFlexLamp.update_edebugbtn()

    def send_state(self):                                       # BokehFlexLamp::send_state()
        """Several ways to send things"""
        cmddict = dict( [ ( "wheat"   , self.wheat_value),
                          ( "osram"   , self.osram_value),
                          ( "halpha"  , self.halpha_value),
                          ( "oiii"    , self.oiii_value),
                          ( "flat"    , self.flat_value),
                          ( "augflat" , self.augflat_value),
                          ( "near"    , self.near_value)
                         ])
        d2 = dict([(f"{self.name}", dict([("Process", cmddict)]))])
        jdict = json.dumps(d2)
        self.display.display(f'{{ "{self.name}" : {jdict} , "returnreciept" : 1 }}')

    ### BokehFlexLamp.send_state()

    def send_off(self):                                         # BokehFlexLamp::send_off()
        """Don't change the internal variables, fake a message to make
        the lamps off."""
        cmddict = dict( [ ( "wheat"   , 0),
                          ( "osram"   , 0),
                          ( "halpha"  , 0),
                          ( "oiii"    , 0),
                          ( "flat"    , 0),
                          ( "augflat" , 0),
                          ( "near"    , 0)
                         ])
        d2      = dict([("Kzin", dict([("Process", cmddict)]))])
        jdict   = json.dumps(d2)
        self.display.display(f'{{ "{self.name}" : {jdict} , "returnreciept" : 1 }}')
        return jdict

    ### BokehFlexLamp.send_off(()

    def layout(self):                                           # BokehFlexLamp::layout()
        """Get the layout in gear"""
        return(row ( column ( self.LampCheckBoxes,
                              row(self.process,self.offbutton)
                            )  ))
        return self

    ### BokehFlexLamp.layout()

    def debug(self,msg="",skip=[],os=sys.stderr):           # BokehFlexLamp::debug()
        """Help with momentary debugging, file to fit.
           msg  -- special tag for this call
           skip -- the member variables to ignore
           os   -- output stream: may be IOStream etc.
        """
        import pprint
        print("BokehFlexLamp - %s " % msg, file=os)
        for key,value in self.__dict__.items():
            if(key in skip):
               continue
            print(f'{key:20s} =',file=os,end='')
            pprint.pprint(value,stream=os,indent=4)
        return self

    ### BokehFlexLamp.debug()

    __BokehFlexLamp_debug = debug  # really preserve our debug name if we're inherited

   # (wg-python-properties properties)

# class BokehFlexLamp

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

    kzin1 = BokehFlexLamp("Tony")
    kzin2  = BokehFlexLamp("Woody")
    if(0):
        with open('/tmp/debug1.txt','w') as os:
            blink1.debug(msg="Starting with...", os=os)
    l1 = kzin1.layout()
    l2 = kzin2.layout()
    tab1 = Panel(child=l1,title='Tony')
    tab2 = Panel(child=l2,title='Woody')
    tabs = Tabs(tabs=[tab1,tab2])
    curdoc().add_root(tabs)

#    curdoc().add_root(column(kzin1.layout(), kzin2.layout()))
#    curdoc().theme = 'dark_minimal'
#    curdoc().title = "Lamp1 Test"
