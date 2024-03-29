#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# bokeh serve ./LampBokeh.py
#
# (compile (format "python -m py_compile %s" (buffer-file-name)))
#
# (wg-python-fix-pdbrc)

### HEREHEREHERE

import os
import sys
import io
import re
import json

from FlexPublish          import fakedisplay

from bokeh.models         import ColumnDataSource, Slider, TextInput, Button
from bokeh                import events
from bokeh.events         import ButtonClick
from bokeh.io             import curdoc
from bokeh.layouts        import column, row, Spacer
from bokeh.models         import Spacer
from bokeh.models         import CustomJS, Div
from bokeh.plotting       import figure
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
# CameraFocus - This is poorly defined and FlexSpec1 does not implement.
#
##############################################################################
class CameraFocus(object):
    """ A small class to blink the led, with varying rate
    """
    brre        = re.compile(r'\n')                         # used to convert newline to HTML <br/>

    sciencechoices = [ "QHY       268",  # sampled from BeSS database
                       "QHY       600 M",
                       "SX        694",
                       "SX        814",
                       "Atik      314 L",
                       "Atik      414 e",
                       "Atik      460 Ex"
                       "ASI       174 MM",
                       "ASI       183 MM",
                       "ASI      1600",
                       "ASI      2600",
                       "QSI       583",
                       "QSI       532",
                       "Audine    402 me",
                       "Audine  KF400",
                       "ST       8300"
                       ]

    #__slots__ = [''] # add legal instance variables
    # (setq properties `("" ""))
    def __init__(self, instrument : 'Flex_Instrument', /,       # CameraFocus::__init__()
                 display    = fakedisplay,
                 gadgetname = "scicamera",
                 width      = 250,
                 name       = 'collimator',
                 pin=4): 
        """Initialize this class."""
        #super().__init__()
        # (wg-python-property-variables)
        self.wwidth         = width         # the width of the dispaly
        self.display        = display       # the FlexPublish Div
        self.instrument     = instrument
        self.gadgetname     = gadgetname
        self.camera         = "camera"            # the type of camera
        self.stepin         = 0
        self.stepout        = 0
        self.camerafocus    = 0             # the device starts in off state.

        # // coordinate with lampcheckboxes_handler
        self.CBLabels=["CameraFocus"]
        self.camerachoices  = Select(title=f"Science Cameras",value='20',options=self.sciencechoices, width=self.wwidth)
        self.cameraname     = TextInput    (title='Science Camera',placeholder="Science Camera",disabled=False,
                                            width=self.wwidth)
        self.step_inbutton  = Button  (align='end', label=f"Step In",  disabled=False,
                                           button_type="warning", width=self.wwidth//2)
        self.step_outbutton = Button  (align='end', label=f"Step Off",  disabled=False,
                                           button_type="warning", width=self.wwidth//2)

        self.camerachoices . on_change('value',lambda attr, old, new: self.update_camerachoices (attr, old, new))
        self.cameraname     .on_change("value",lambda attr, old, new: self.update_cameraname(attr, old, new))
        self.step_inbutton  .on_click (lambda : self.update_step_inbutton())
        self.step_outbutton .on_click (lambda : self.update_step_outbutton())

    ### CameraFocus.__init__()

    def update_cameraname(self,attr,old,new):              # Network::update_connectbutton()
        self.camera = new

    def update_camerachoices(self,attr,old,new):                     # BokehRoboFocuser::update_button_in()
        """update_debugbtn Button via an event lambda"""
        self.camera = new # self.slitchoices.value
        self.cameraname.value = new
        self.send_state() # display(f"{self.slit}")

    def update_step_outbutton(self):                                 # CameraFocus::update_step_outbutton()
        """Set internal variables to off."""
        self.stepin  = 0;
        self.stepout = 1;
        self.send_state()                   # instant action

    ### CameraFocus.update_step_outbutton()

    def update_step_inbutton(self):                                   # CameraFocus::update_button_in()
        """update_step_inbutton Button via an event lambda"""
        self.stepin  = 1;
        self.stepout = 0;
        self.send_state()                   # instant action

    ### CameraFocus.update_step_inbutton()

    def update_debugbtn(self):                                  # CameraFocus::update_button_in()
        """update_debugbtn Button via an event lambda"""
        os = io.StringIO()
        self.debug(f"{self.gadgetname} Debug", os=os)
        os.seek(0)
        self.display.display(CameraFocus.brre.sub("<br/>",os.read()))

    ### CameraFocus.update_edebugbtn()

    def send_state(self):                                       # CameraFocus::send_state()
        """Several ways to send things
          {"sciencecamera" : {"in" : "", "out" : "", "reciept" : "1"}
        dict( [ ("in",  '"%d"' % self.stepin), ("out" , ), ("reciept", "1")] )
        """
        devstate  = dict( [ ("cammera", f"{self.camera}"      ),
                          ("in"     , f"{self.stepin:3d}" ),
                          ("out"    , f"{self.stepout:3d}"),
                          ("reciept", "1")
                        ])
        gadgetcmd = dict([("process", devstate)])
        package   = dict([(f"{self.gadgetname}", gadgetcmd)])
        envelope  = dict([(f"{self.instrument.flexname}", package)])
        
        jdict        = json.dumps(envelope)
        self.display.display(f'{jdict}')

    ### CameraFocus.send_state()

    def layout(self):                                           # CameraFocus::layout()
        """Get the layout in gear"""
        return(row ( column ( row(self.camerachoices),
                              row(self.cameraname),
                              row(self.step_inbutton,self.step_outbutton)
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

# class CameraFocus

##############################################################################
#                                    Main
#                               Regression Tests
##############################################################################
# HEREHEREHERE
if(0):

    camera = CameraFocus()

    if(0):
        with open('/tmp/debug1.txt','w') as os:
            blink1.debug(msg="Starting with...", os=os)

    tab1  = Panel(child=camera,title="Tony's Camera")
    tab2  = Panel(child=fakedisplay,title='Display')
    tabs  = Tabs(tabs=[tab1,tab2])
    curdoc().add_root(tabs)

#    curdoc().add_root(column(kzin1.layout(), kzin2.layout()))
#    curdoc().theme = 'dark_minimal'
#    curdoc().title = "Lamp1 Test"
