#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# bokeh serve KzinBokeh.py --unused-session-lifetime 3600000
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
#  /home/git/external/SAS_NA1_3D_Spectrograph/Code/KzinBokeh.py
#
#emacs helpers
# (insert (format "\n# %s " (buffer-file-name)))
#
# (set-input-method 'TeX' t)
# (toggle-input-method)
# α
# β
# λ
# μ
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

/home/git/external/SAS_NA1_3D_Spectrograph/Code/KzinBokeh.py

[options] files...

Treat this as Kzin Ring Assy.

The buttons are:

   near     --  Calibration Lamp
   osram    --  OSRAM Lamp HV bulb
   hα       --  Reference Red LED
   oiii     --  Reference ND OIII region
   flat     --  Flat Assy
   augflat  --  Flat Assy with Blue Boost

Select the slider, fine-tune with keyboard arrows.

"""


__author__  = 'Wayne Green'
__version__ = '0.1'
__all__     = ['BokehKzinRing','KzinRingException']   # list of quoted items to export

# (wg-python-class "KzinRing")
##############################################################################
# KzinRingException
#
##############################################################################
class KzinRingException(Exception):
    """Special exception to allow differentiated capture of exceptions"""
    def __init__(self,message,errors=None):
        super(KzinRingException,self).__init__("KzinRing "+ message)
        self.errors = errors
    @staticmethod
    def __format__(e):
        return f" KzinRing: {e.__str__()}\n"
# KzinRingException

##############################################################################
# BokehKzinRing
#
##############################################################################
class BokehKzinRing(object):
    """ A small class to blink the led, with varying rate
    """

    # FAKE up some enums.
    ON          = 0  # BokehKzinRing.ON
    OFF         = 1  # BokehKzinRing.OFF
    RUN         = 2  # BokehKzinRing.RUN
    SateText    = ["Off","On","Illegal"]
    brre        = re.compile(r'\n')                         # used to convert newline to <br/>


    ##################################################################
    #  SliderValues an Internal instance placeholder to sidestep
    #  call by reference in python.
    ##################################################################
    class SliderValues(object):
        """Manage object values"""
        def __init__(self):
            self.values = dict((
            ("wheat_value"   ,"0"),
            ("osram_value"   ,"0"),
            ("hbeta_value"   ,"0"),
            ("oiii_value"    ,"0"),
            ("halpha_value"  ,"0"),
            ("flat_value"    ,"0"),
            ("augflat_value" ,"0"),
            ("near_value"    ,"0")
            ))
    # SliderValues

    #__slots__ = [''] # add legal instance variables
    # (setq properties `("" ""))
    def __init__(self, name : str = "Default",
                 display = fakedisplay,
                 width=250,pin=4): # BokehKzinRing::__init__()
        """Initialize this class."""
        #super().__init__()
        # (wg-python-property-variables)
        self.wwidth              = width
        self.display             = display
        self.name                = name
        self.display             = display
        self.wheatcheck_value    = 1                 # add a variable for each lamp
        self.osramcheck_value    = 0                 # installed.
        self.hαcheck_value       = 0
        self.oiiicheck_value     = 0
        self.flatcheck_value     = 0
        self.augflatcheck_value  = 0
        self.nearcheck_value     = 0

#        self.wheat_value         = 0
#        self.osram_value         = 0
#        self.hα_value            = 0
#        self.oiii_value          = 0
#        self.hβ_value            = 0
#        self.flat_value          = 0
#        self.augflat_value       = 0
#        self.near_value          = 0
#        self.onoff               = 0                # Off
        self.slider_values = BokehKzinRing.SliderValues()

        # Labels merge spaces into one space.
        self.wheatslider    = Slider(title=f"Incandescent Intensity", bar_color='firebrick',
                                     value = -1, start = -1,  end = 100, step = 1, width=self.wwidth)
        self.osramslider    = Slider(title=f"Osram Intensity", bar_color='firebrick',
                                     value = -1, start = -1,  end = 100, step = 1, width=self.wwidth)
        self.hβslider   = Slider(title=f"Hβ Finder Intensity", bar_color='firebrick',
                                     value = -1, start = -1,  end = 100, step = 1, width=self.wwidth)
        self.oiiislider     = Slider(title=f"O[III] Finder Intensity", bar_color='firebrick',
                                     value = -1, start = -1, end = 100, step = 1, width=self.wwidth)
        self.hαslider   = Slider(title=f"Hα Finder Intensity", bar_color='firebrick',
                                     value = -1, start = -1,  end = 100, step = 1, width=self.wwidth)
        self.flatslider     = Slider(title=f"Flat Intensity", bar_color='firebrick',
                                     value = -1, start = -1,  end = 100, step = 1, width=self.wwidth)
        self.augflatslider  = Slider(title=f"Augmented Flat Intensity", bar_color='firebrick',
                                     value = -1, start = -1,  end = 100, step = 1, width=self.wwidth)
        self.nearslider     = Slider(title=f"NeAr Intensity", bar_color='firebrick',
                                     value = -1, start = -1,  end = 100, step = 1, width=self.wwidth)

        self.wheatslider   .on_change('value', lambda attr, old, new: self.update_slider ("wheat_value"  , attr, old, new))
        self.osramslider   .on_change('value', lambda attr, old, new: self.update_slider ("osram_value"  , attr, old, new))
        self.hβslider      .on_change('value', lambda attr, old, new: self.update_slider ("hbeta_value"  , attr, old, new))
        self.oiiislider    .on_change('value', lambda attr, old, new: self.update_slider ("oiii_value"   , attr, old, new))
        self.hαslider      .on_change('value', lambda attr, old, new: self.update_slider ("halpha_value" , attr, old, new))
        self.flatslider    .on_change('value', lambda attr, old, new: self.update_slider ("flat_value"   , attr, old, new))
        self.augflatslider .on_change('value', lambda attr, old, new: self.update_slider ("augflat_value", attr, old, new))
        self.nearslider    .on_change('value', lambda attr, old, new: self.update_slider ("near_value"   , attr, old, new))

        # // coordinate with lampcheckboxes_handler
#        self.CBLabels=["Wheat", "Osram", "H-α", "O[iii]", "Flat", "Blue Flat", "NeAr" ]
#        self.LampCheckBoxes = CheckboxButtonGroup(labels=self.CBLabels,
#                                                  active=[0]*len(self.CBLabels)
#                                                 ) # create/init them

        self.process        = Button    (align='end', label=f"{self.name} On",  disabled=False,
                                                   button_type="success", width=self.wwidth//2)
        self.offbutton      = Button    (align='end', label=f"{self.name} Off",  disabled=False,
                                                   button_type="primary", width=self.wwidth//2)

#        self.LampCheckBoxes .on_change('active', lambda attr, old, new: self.lampcheckboxes_handler   (attr, old, new))
        self.process        .on_click (lambda : self.update_process())
        self.offbutton      .on_click (lambda : self.update_offbutton())


    ### BokehKzinRing.__init__()

    def update_slider(self,memberval,attr,old,new):                        # BokehGrating::cwave()
        """Get the new slider value and send it.
        This is a call by a lambda from many sliders, sending its
        corresponding value into the mix."""
        self. slider_values.values[memberval] = new

    ### BokehGrating.cwave()


    def update_offbutton(self):                                 # BokehKzinRing::update_offbutton()
        """Set internal variables to off."""
        self.onoff = 0
        msg = self.send_state()

    ### BokehKzinRing.update_offbutton()

    def update_process(self):                                   # BokehKzinRing::update_button_in()
        """update_process Button via an event lambda"""
        #os = io.StringIO()
        #self.debug(f"{self.name} Debug",skip=['varmap'], os=os)
        #os.seek(0)
        self.onoff = 1
        msg = self.send_state()

    ### BokehKzinRing.update_process()

#    def lampcheckboxes_handler(self,attr, old, new):            # BokehKzinRing::lampcheckboxes_handler()
#        """Handle the checkboxes, new is a list of indices into
#        self.CBLabels for their purpose"""
#        msg = f"attr {attr}, old {old}, new {new}"
#        self.wheatcheck_value   = 1 if 0 in new else 0
#        self.osramcheck_value   = 1 if 1 in new else 0
#        self.hαcheck_value      = 1 if 2 in new else 0
#        self.oiiicheck_value    = 1 if 3 in new else 0
#        self.flatcheck_value    = 1 if 4 in new else 0
#        self.augflatcheck_value = 1 if 5 in new else 0
#        self.nearcheck_value    = 1 if 6 in new else 0
#        #self.display(msg)

    ### BokehKzinRing.lampcheckboxes_handler()

    def update_debugbtn(self):                                  # BokehKzinRing::update_button_in()
        """update_debugbtn Button via an event lambda"""
        os = io.StringIO()
        self.debug(f"{self.name} Debug", os=os)
        os.seek(0)
        self.display.display(BokehKzinRing.brre.sub("<br/>",os.read()))

    ### BokehKzinRing.update_edebugbtn()

    def send_state(self):                                       # BokehKzinRing::send_state()
        """Several ways to send things"""
        cmddict = dict( [ ( "wheat"   , self.slider_values.values["wheat_value"   ]),
                          ( "osram"   , self.slider_values.values["osram_value"   ]),
                          ( "hbeta"   , self.slider_values.values["hbeta_value"   ]),
                          ( "oiii"    , self.slider_values.values["oiii_value"    ]),
                          ( "halpha"  , self.slider_values.values["halpha_value"  ]),
                          ( "flat"    , self.slider_values.values["flat_value"    ]),
                          ( "augflat" , self.slider_values.values["augflat_value" ]),
                          ( "near"    , self.slider_values.values["near_value"    ]),
                          ( "state"   , self.onoff)
                         ])
        d2    = dict([(f"{self.name}", dict([("Process", cmddict)]))])
        jdict = json.dumps(d2)
        self.display.display(f'{{ "{self.name}" : {jdict} , "returnreceipt" : 1 }}')

    ### BokehKzinRing.send_state()

#    def send_off(self):                                         # BokehKzinRing::send_off()
#        """Don't change the internal variables, fake a message to make
#        the lamps off."""
#        cmddict = dict( [ ( "wheat"   , 0),
#                          ( "osram"   , 0),
#                          ( "hβ"      , 0),
#                          ( "oiii"    , 0),
#                          ( "hα"      , 0),
#                          ( "flat"    , 0),
#                          ( "augflat" , 0),
#                          ( "near"    , 0),
#                          ( "state"   , self.onoff))
#                         ])
#        d2      = dict([("Kzin", dict([("Process", cmddict)]))])
#        jdict   = json.dumps(d2)
#        self.display.display(f'{{ "{self.name}" : {jdict} , "returnreceipt" : 1 }}')
#        return jdict
#
#    ### BokehKzinRing.send_off(()

    def layout(self):                                           # BokehKzinRing::layout()
        """Get the layout in gear"""
        return(row ( column ( #self.LampCheckBoxes,
                              self.wheatslider,
                              self.osramslider,
                              self.hβslider,
                              self.oiiislider,
                              self.hαslider,
                              self.flatslider,
                              self.augflatslider,
                              self.nearslider,
                              row(self.process,self.offbutton)
                            )  ))
        return self

    ### BokehKzinRing.layout()

    def debug(self,msg="",skip=[],os=sys.stderr):           # BokehKzinRing::debug()
        """Help with momentary debugging, file to fit.
           msg  -- special tag for this call
           skip -- the member variables to ignore
           os   -- output stream: may be IOStream etc.
        """
        import pprint
        print("BokehKzinRing - %s " % msg, file=os)
        for key,value in self.__dict__.items():
            if(key in skip):
               continue
            print(f'{key:20s} =',file=os,end='')
            pprint.pprint(value,stream=os,indent=4)
        return self

    ### BokehKzinRing.debug()

    __BokehKzinRing_debug = debug  # really preserve our debug name if we're inherited

   # (wg-python-properties properties)

# class BokehKzinRing

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

    kzin1 = BokehKzinRing("Tony")
    kzin2  = BokehKzinRing("Woody")
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
