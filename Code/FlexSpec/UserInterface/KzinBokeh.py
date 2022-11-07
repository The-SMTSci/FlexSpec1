#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Test with:
# bokeh serve KzinBokeh.py --unused-session-lifetime 3600000
# (wg-python-fix-pdbrc)

### HEREHEREHERE

import os
import optparse
import sys
import io
import re
import json
import datetime
from FlexPublish          import fakedisplay


from bokeh                import events
from bokeh.events         import ButtonClick
from bokeh.io             import curdoc
from bokeh.layouts        import column, row, Spacer
from bokeh.models         import CheckboxButtonGroup,ColumnDataSource, Slider, TextInput, Button
from bokeh.models         import CustomJS, Div
from bokeh.plotting       import figure
from bokeh.models         import RadioGroup
from bokeh.models         import Select
from bokeh.models.widgets import Tabs, Panel

#from Shutter              import FlexShutter


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
# (wg-python-toc)
#
# __doc__ = """
# __author__  = 'Wayne Green'
# __version__ = '0.1'
# __all__     = ['BokehKzinRing','KzinRingException']   # list of quoted items to export
# class KzinRingException(Exception):
#     def __init__(self,message,errors=None):
#     @staticmethod
#     def __format__(e):
# class BokehKzinRing(object):
#     class SliderValues(object):
#         def __init__(self):
#     #__slots__ = [''] # add legal instance variables
#     def __init__(self, name : str = "Default",
#     def update_slider(self,memberval,attr,old,new):             # BokehGrating::cwave()
#     def update_offbutton(self):                                 # BokehKzinRing::update_offbutton()
#     def update_process(self):                                   # BokehKzinRing::update_button_in()
#     def update_debugbtn(self):                                  # BokehKzinRing::update_button_in()
#     def send_state(self):                                       # BokehKzinRing::send_state()
#     def layout(self):                                           # BokehKzinRing::layout()
#     def debug(self,msg="",skip=[],os=sys.stderr):               # BokehKzinRing::debug()
#
#
#
#############################################################################
__doc__ = """

/home/git/external/SAS_NA1_3D_Spectrograph/Code/KzinBokeh.py

[options] files...

Treat this as Kzin Ring Assy.

The buttons are:

   near     --  Calibration Lamp
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
            ("wheat"   ,"0"),
            ("hbeta"   ,"0"),
            ("oiii"    ,"0"),
            ("halpha"  ,"0"),
            ("flat"    ,"0"),
            ("augflat" ,"0"),
            ("near"    ,"0")
            ))
        def insertquery(self,name : str = "kzin") -> str:
            """Make an insert query for the ring.
            name is the name of the kzin"""
            vallist = ['name','tstamp']
            values  = [f"'{name}'", f"'{datetime.datetime.now()}'"]
            for k,v in self.values.items():
                vallist.append(f"""{k}""")
                values.append(f"{v}")
            inslist = '(' + ','.join(vallist)+ ')'
            insvals = '(' + ','.join(values) + ')'
            stmt = f"""insert into kzinvalues {inslist} values {insvals};"""
            return stmt
    # SliderValues

    #__slots__ = [''] # add legal instance variables
    # (setq properties `("" ""))
    def __init__(self, flexname : str = "Default",
                 name : str = "Default",
                 display = fakedisplay,
                 width=250,pin=4): # BokehKzinRing::__init__()
        """Initialize this class."""
        #super().__init__()
        # (wg-python-property-variables)
        self.wwidth              = width
        self.display             = display
        self.flexname            = flexname
        self.name                = name
        self.display             = display
        self.wheatcheck_value    = 1                 # add a variable for each lamp
        self.hαcheck_value       = 0
        self.oiiicheck_value     = 0
        self.flatcheck_value     = 0
        self.augflatcheck_value  = 0
        self.nearcheck_value     = 0
        self.receipt             = 1                 # always ask for an update
        #self.shutter             = FlexShutter (flexname,display=display,width=width)

        self.slider_values = BokehKzinRing.SliderValues()

        self.gowcolor       = 'antiquewhite'      # set the colors in one place
        self.nearcolor      = 'fuchsia'           # https://docs.bokeh.org/en/latest/docs/reference/colors.html
        self.boostcolor     = 'dodgerblue'
        self.flatcolor      = 'gainsboro'
        self.oiii           = 'mediumslateblue'
        self.hb             = 'lime'
        self.ha             = 'firebrick'
        self.wheatslider    = Slider(title=f"GoW", bar_color='firebrick', orientation='vertical',
                                     background=self.gowcolor, direction='rtl',
                                     value = -1, start = -1,  end = 100, step = 1, width=self.wwidth//8)
        self.nearslider     = Slider(title=f"NeAr", bar_color='firebrick', orientation='vertical',
                                     background=self.nearcolor, direction='rtl',
                                     value = -1, start = -1,  end = 100, step = 1, width=self.wwidth//8)
        self.augflatslider  = Slider(title=f"Boost", bar_color='firebrick', orientation='vertical',
                                     background=self.boostcolor, direction='rtl',
                                     value = -1, start = -1,  end = 100, step = 1, width=self.wwidth//8)
        self.flatslider     = Slider(title=f"Flat", bar_color='firebrick', orientation='vertical',
                                     background=self.flatcolor, direction='rtl',
                                     value = -1, start = -1,  end = 100, step = 1, width=self.wwidth//8)
        self.hβslider       = Slider(title=f"Hβ", bar_color='firebrick',orientation='vertical',
                                     background=self.oiii, direction='rtl',
                                     value = -1, start = -1,  end = 100, step = 1, width=self.wwidth//8)
        self.oiiislider     = Slider(title=f"O[III]", bar_color='firebrick',orientation='vertical',
                                     background=self.hb, direction='rtl',
                                     value = -1, start = -1, end = 100, step = 1, width=self.wwidth//8)
        self.hαslider       = Slider(title=f"Hα", bar_color='firebrick',orientation='vertical',
                                     background=self.ha, direction='rtl',
                                     value = -1, start = -1,  end = 100, step = 1, width=self.wwidth//8)

        self.nearslider    .on_change('value', lambda attr, old, new: self.update_slider ("near_value"   , attr, old, new))
        self.wheatslider   .on_change('value', lambda attr, old, new: self.update_slider ("wheat_value"  , attr, old, new))
        self.augflatslider .on_change('value', lambda attr, old, new: self.update_slider ("augflat_value", attr, old, new))
        self.flatslider    .on_change('value', lambda attr, old, new: self.update_slider ("flat_value"   , attr, old, new))
        self.hβslider      .on_change('value', lambda attr, old, new: self.update_slider ("hbeta_value"  , attr, old, new))
        self.oiiislider    .on_change('value', lambda attr, old, new: self.update_slider ("oiii_value"   , attr, old, new))
        self.hαslider      .on_change('value', lambda attr, old, new: self.update_slider ("halpha_value" , attr, old, new))

        # // coordinate with lampcheckboxes_handler
        pwidth = self.wwidth//12
        self.onbutton       = Button    (align='end', label=f"On",  disabled=False,
                                                   button_type="warning", width=5*pwidth)
        self.offbutton      = Button    (align='end', label=f"Off",  disabled=False,
                                                   button_type="success", width=5*pwidth)
        self.recordbutton   = Button    (align='end', label=f"Record",  disabled=False,
                                                   button_type="success", width=2*pwidth)

        self.onbutton        .on_click (lambda : self.update_onbutton())
        self.offbutton       .on_click (lambda : self.update_offbutton())
        self.recordbutton    .on_click (lambda : self.update_recordbutton())


    ### BokehKzinRing.__init__()

    def update_recordbutton(self):                          # BokehGrating::cupdate_slider()
        """Send the state to a database somewhere"""
        query = self.slider_values.insertquery()
        self.display.display(f"""Record Not Implemented\n{query}""")

    ### BokehGrating.update_recordbutton()


    def update_slider(self,memberval,attr,old,new):         # BokehGrating::cupdate_slider()
        """Get the new slider value and send it.
        This is a call by a lambda from many sliders, sending its
        corresponding value into the mix."""
        self. slider_values.values[memberval] = new

    ### BokehGrating.update_slider()


    def update_slider(self,memberval,attr,old,new):         # BokehGrating::cwave()
        """Get the new slider value and send it.
        This is a call by a lambda from many sliders, sending its
        corresponding value into the mix."""
        self. slider_values.values[memberval] = new

    ### BokehGrating.cwave()

    def update_offbutton(self):                             # BokehKzinRing::update_offbutton()
        """Set internal variables to off."""
        self.onoff = 0
        msg = self.send_state()

    ### BokehKzinRing.update_offbutton()

    def update_onbutton(self):                              # BokehKzinRing::update_button_in()
        """update_onbutton Button via an event lambda"""
        #os = io.StringIO()
        #self.debug(f"{self.name} Debug",skip=['varmap'], os=os)
        #os.seek(0)
        self.display.display(BokehKzinRing.brre.sub("<br/>",f"Things in onbutton{dir(self.onbutton._property_values)}"))
        self.onoff = 1
        msg = self.send_state()

    ### BokehKzinRing.update_onbutton()

    def update_debugbtn(self):                              # BokehKzinRing::update_button_in()
        """update_debugbtn Button via an event lambda"""
        os = io.StringIO()
        self.debug(f"{self.name} Debug", os=os)
        os.seek(0)
        self.display.display(BokehKzinRing.brre.sub("<br/>",os.read()))

    ### BokehKzinRing.update_edebugbtn()

    def send_state(self):                                   # BokehKzinRing::send_state()
        """Several ways to send things
           schematic  2021-08-27T11:32:01-0600
        """
        # dropped
                        #   ( "flat"    , self.slider_values.values["flat_value"    ]),
                        #   ( "near"    , self.slider_values.values["near_value"    ]), # Relco
        #                    JSON TXT      Bokeh                    PY Variable
        devstate = dict( [ ( "wheat"   , f'"{self.slider_values.values["wheat_value"   ]}"'), # Tungstun
                           ( "callamp" , f'"{self.slider_values.values["near_value"    ]}"'), # CAL Relco
                           ( "hbeta"   , f'"{self.slider_values.values["hbeta_value"   ]}"'), # M3 BLUE LED
                           ( "oiii"    , f'"{self.slider_values.values["oiii_value"    ]}"'), # M2 GREEN LED
                           ( "halpha"  , f'"{self.slider_values.values["halpha_value"  ]}"'), # M1 RED LED
                           ( "uvboost" , f'"{self.slider_values.values["augflat_value" ]}"'), # Blue boost
                           ( "flat"    , f'"{self.slider_values.values["flat_value"    ]}"'), # MID WHITE LED
                           ( "state"   , f'"{self.onoff}"'),                                  # State  ON/OFF
                           ( "receipt" , f'"{self.receipt}"')                                 # get update
                         ])

        gadgetcmd  = dict([("process", devstate)])
        d2        = dict([(f"{self.name}", gadgetcmd)])     # Add in my decice (instance with in one instrument) name
        d3        = dict([(f"{self.flexname}", d2)])        # Add in my 'Instrument' name (vis-a-vis other instruments)
        jdict     = json.dumps(d3)                          # make string image
        self.display.display(f'{jdict}')                    # send it to browser DIV, and off to communications port.

    ### BokehKzinRing.send_state()

    def layout(self):                                       # BokehKzinRing::layout()
        """Get the layout in gear"""
        return(row ( column ( #self.LampCheckBoxes,             # Physical layout the user.
                            row(
                              column(self.hβslider),                    # Marker for BLUE  LED  - broad band led
                              column(self.oiiislider),                  # Marker for GREEN LED
                              column(self.hαslider),                    # Marker for REF   LED
                              Spacer(width=10, height=self.wwidth//2, background='black'),
                              column(self.nearslider),                  # Relco -
                              Spacer(width=10, height=self.wwidth//2, background='black'),
                              column(self.augflatslider),               # ... add in some BLUE LED boost
                              column(self.wheatslider),                 # Tungstun flat
                              column(self.flatslider)),                 # ... and/or toss in WHITE LIGHT LED
                              Spacer(width=self.wwidth, height=5, background='black'),
                              row(self.onbutton,self.offbutton,self.recordbutton),
                              #row(self.shutter.layout())
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

    kzin1  = BokehKzinRing("Tony")
    kzin2  = BokehKzinRing("John")
    if(0):
        with open('/tmp/debug1.txt','w') as os:
            blink1.debug(msg="Starting with...", os=os)
    l1     = kzin1.layout()
    l2     = kzin2.layout()
    tab1   = Panel(child=l1,title='Tony')
    tab2   = Panel(child=l2,title='John')
    tabs   = Tabs(tabs=[tab1,tab2])
    curdoc().add_root(tabs)

#    curdoc().add_root(column(kzin1.layout(), kzin2.layout()))
#    curdoc().theme = 'dark_minimal'
#    curdoc().title = "Lamp1 Test"
