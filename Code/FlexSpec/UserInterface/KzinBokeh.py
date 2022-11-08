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
#         def insertquery(self,name : str = "kzin") -> str:
#     #__slots__ = [''] # add legal instance variables
#     def __init__(self, flexname : str = "Default",
#     def update_wheatvalue(self,valname,attr,old,new):       # BokehKzinRing.update_wheatvalue()
#     def update_nearvalue(self,valname,attr,old,new):        # BokehKzinRing.update_nearvalue()
#     def update_augvalue(self,valname,attr,old,new):         # BokehKzinRing.update_augvalue()
#     def update_flatsvalue(self,valname,attr,old,new):       # BokehKzinRing.update_flatsvalue()
#     def update_hβvalue(self,valname,attr,old,new):          # BokehKzinRing.update_hβvalue()
#     def update_oiiivalue(self,valname,attr,old,new):        # BokehKzinRing.update_oiiivalue()
#     def update_hαvalue(self,valname,attr,old,new):          # BokehKzinRing.update_hαvalue()
#     def update_recordbutton(self):                          # BokehGrating::cupdate_slider()
#     def update_slider(self,memberval,attr,old,new):         # BokehGrating::cupdate_slider()
#     def update_offbutton(self):                             # BokehKzinRing::update_offbutton()
#     def update_onbutton(self):                              # BokehKzinRing::update_button_in()
#     def update_debugbtn(self):                              # BokehKzinRing::update_button_in()
#     def send_state(self):                                   # BokehKzinRing::send_state()
#     def layout(self):                                       # BokehKzinRing::layout()
#     def debug(self,msg="",skip=[],os=sys.stderr):           # BokehKzinRing::debug()
#
#############################################################################
__doc__ = """

/home/git/external/SAS_NA1_3D_Spectrograph/Code/KzinBokeh.py

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
    """ Manage the kzin ring with a slider to set the intensity.
    The pins are supposed to be mapped to PWM pins on an Arduino, with
    electonics to manage the official values to each device on the Kzin
    board.
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
            name is the name of the kzin:
                drop table kzin;
                create table if not exists kzin (name text, tstamp , jsonmessage text);
                insert into kzin (name,tstamp,jsonmessage)
                values
                    ('tonyflex','2022-11-11 11:00:00',
                       '{"tonyflex" : {"kzin" : {"halpha" : "1", "hbeta" :"0"}}}'
                    );
                select name,datetime(tstamp),jsonmessage from kzin;
                select name,julianday(tstamp),jsonmessage from kzin;
                commit;  # dont forget this commit!
            """
            ret         = ""
            vallist     = ','.join(['name','tstamp','jsonmessage'])
            #jsonmessage = f"""'{{"{name}" : {{"kzin" : {{"halpha" : "1", "hbeta" :"0"}}}}}}'"""
            jsonmessage = f"""'{{"{name}" : {{"kzin" : {json.dumps(self.values)}}}}}"""
            values      = ','.join([f"'{name}'", f"'{datetime.datetime.now()}'", f"""'{jsonmessage}'"""
                                    ])
            ret         = f"""insert ( {vallist} + ) into kzin values ( {values} );"""

            return ret

    # SliderValues

    def __init__(self, flexname : str = "Default",          # BokehKzinRing::__init__()
                 name           : str = "Default",
                 display        : 'FlexPublish' = fakedisplay,
                 width          : int = 250,
                 pin            : int= 4):
        """Setup the UI, manage the callbacks, layout, messaging etc for the
        Kzin widget."""

        self.wwidth              = width
        self.display             = display
        self.flexname            = flexname
        self.name                = name
        self.display             = display
        self.receipt             = 1                   # always ask for an update

        self.slider_values       = BokehKzinRing.SliderValues()

        self.gowcolor            = 'antiquewhite'      # manage the slider color values in one place
        self.nearcolor           = 'fuchsia'           # https://docs.bokeh.org/en/latest/docs/reference/colors.html
        self.boostcolor          = 'dodgerblue'
        self.flatcolor           = 'gainsboro'
        self.oiii                = 'mediumslateblue'
        self.hβ                  = 'lime'
        self.hα                  = 'firebrick'

        self.configurations      = ["Recent", "Default"]
        self.profiles            = Select(title="Recent Configurations", options = self.configurations, width = self.wwidth)

        pwidth = self.wwidth//12                       # uniform width/spacing
        twidth = self.wwidth//8

######################################### Bokeh Sliders ############################################

        self.wheatslider    = Slider(title=f"GoW", bar_color='firebrick', orientation='vertical',
                                     background=self.gowcolor, direction='rtl',
                                     value = -1, start = -1,  end = 100, step = 0.1, width=self.wwidth//8)
        self.nearslider     = Slider(title=f"NeAr", bar_color='firebrick', orientation='vertical',
                                     background=self.nearcolor, direction='rtl',
                                     value = -1, start = -1,  end = 100, step = 0.1, width=self.wwidth//8)
        self.augflatslider  = Slider(title=f"Boost", bar_color='firebrick', orientation='vertical',
                                     background=self.boostcolor, direction='rtl',
                                     value = -1, start = -1,  end = 100, step = 0.1, width=self.wwidth//8)
        self.flatslider     = Slider(title=f"Flat", bar_color='firebrick', orientation='vertical',
                                     background=self.flatcolor, direction='rtl',
                                     value = -1, start = -1,  end = 100, step = 0.1, width=self.wwidth//8)
        self.hβslider       = Slider(title=f"Hβ", bar_color='firebrick',orientation='vertical',
                                     background=self.oiii, direction='rtl',
                                     value = -1, start = -1,  end = 100, step = 0.1, width=self.wwidth//8)
        self.oiiislider     = Slider(title=f"O[III]", bar_color='firebrick',orientation='vertical',
                                     background=self.hβ, direction='rtl',
                                     value = -1, start = -1, end = 100, step = 0.1, width=self.wwidth//8)
        self.hαslider       = Slider(title=f"Hα", bar_color='firebrick',orientation='vertical',
                                     background=self.hα, direction='rtl',
                                     value = -1, start = -1,  end = 100, step = 0.1, width=self.wwidth//8)

        self.nearslider     .on_change('value', lambda attr, old, new: self.update_slider ("near_value"   , attr, old, new))
        self.wheatslider    .on_change('value', lambda attr, old, new: self.update_slider ("wheat_value"  , attr, old, new))
        self.augflatslider  .on_change('value', lambda attr, old, new: self.update_slider ("augflat_value", attr, old, new))
        self.flatslider     .on_change('value', lambda attr, old, new: self.update_slider ("flat_value"   , attr, old, new))
        self.hβslider       .on_change('value', lambda attr, old, new: self.update_slider ("hbeta_value"  , attr, old, new))
        self.oiiislider     .on_change('value', lambda attr, old, new: self.update_slider ("oiii_value"   , attr, old, new))
        self.hαslider       .on_change('value', lambda attr, old, new: self.update_slider ("halpha_value" , attr, old, new))

######################################### associated text inputs ###################################

        self.wheatvalue     = TextInput(title='GoW'   ,width=twidth)
        self.nearvalue      = TextInput(title='NeAr'  ,width=twidth)
        self.augvalue       = TextInput(title='Boost' ,width=twidth)
        self.flatsvalue     = TextInput(title='Flat'  ,width=twidth)
        self.hβvalue        = TextInput(title='Hβ'    ,width=twidth)
        self.oiiivalue      = TextInput(title='O[III]',width=twidth)
        self.hαvalue        = TextInput(title='Hα'    ,width=twidth)

        self.wheatvalue     .on_change("value",lambda attr, old, new: self.update_wheatvalue ("wheat_value"   , attr, old, new))
        self.nearvalue      .on_change("value",lambda attr, old, new: self.update_nearvalue  ("near_value"  , attr, old, new))
        self.augvalue       .on_change("value",lambda attr, old, new: self.update_augvalue   ("augflat_value", attr, old, new))
        self.flatsvalue     .on_change("value",lambda attr, old, new: self.update_flatsvalue ("flat_value"   , attr, old, new))
        self.hβvalue        .on_change("value",lambda attr, old, new: self.update_hβvalue    ("hbeta_value"  , attr, old, new))
        self.oiiivalue      .on_change("value",lambda attr, old, new: self.update_oiiivalue  ("oiii_value"   , attr, old, new))
        self.hαvalue        .on_change("value",lambda attr, old, new: self.update_hαvalue    ("halpha_value" , attr, old, new))

        self.textfields = dict([ ("wheat_value"   , self.wheatvalue  ),   # map the membername to its textinput widget
                                 ("near_value"    , self.nearvalue   ),
                                 ("augflat_value" , self.augvalue    ),
                                 ("flat_value"    , self.flatsvalue  ),
                                 ("hbeta_value"   , self.hβvalue     ),
                                 ("oiii_value"    , self.oiiivalue   ),
                                 ("halpha_value"  , self.hαvalue     )
                              ])

########################################## Actions #################################################

        # // coordinate with lampcheckboxes_handler
        self.onbutton       = Button    (align='end', label=f"On",  disabled=False,
                                                   button_type="warning", width=5*pwidth)
        self.offbutton      = Button    (align='end', label=f"Off",  disabled=False,
                                                   button_type="success", width=5*pwidth)
        self.recordbutton   = Button    (align='end', label=f"Record",  disabled=False,
                                                   button_type="success", width=2*pwidth)

        self.onbutton       .on_click (lambda : self.update_onbutton())
        self.offbutton      .on_click (lambda : self.update_offbutton())
        self.recordbutton   .on_click (lambda : self.update_recordbutton())

########################################### textinput actions ######################################

    # react to a textinput's change

    def update_wheatvalue(self,valname,attr,old,new):       # BokehKzinRing.update_wheatvalue()
        """update corresponding  slider"""
        self.wheatslider.value             = float(new)
        self.slider_values.values[valname] = new

    ### BokehKzinRing.update_wheatvalue()

    def update_nearvalue(self,valname,attr,old,new):        # BokehKzinRing.update_nearvalue()
        """update corresponding near slider"""
        self.nearslider.value              = float(new)
        self.slider_values.values[valname] = new

    ### BokehKzinRing.update_nearvalue()

    def update_augvalue(self,valname,attr,old,new):         # BokehKzinRing.update_augvalue()
        """update corresponding augflats slider"""
        self.augflatslider.value           = float(new)
        self.slider_values.values[valname] = new

    ### BokehKzinRing.update_augvalue()

    def update_flatsvalue(self,valname,attr,old,new):       # BokehKzinRing.update_flatsvalue()
        """update corresponding flats slider"""
        self.flatslider.value              = float(new)
        self.slider_values.values[valname] = new

    ### BokehKzinRing.update_flatsvalue()

    def update_hβvalue(self,valname,attr,old,new):          # BokehKzinRing.update_hβvalue()
        """update corresponding hβvalue slider"""
        self.hβvalue.value                 = float(new)
        self.slider_values.values[valname] = new

    ### BokehKzinRing.update_hβvalue()

    def update_oiiivalue(self,valname,attr,old,new):        # BokehKzinRing.update_oiiivalue()
        """update corresponding oiiivalue slider"""
        self.oiiislider.value              = float(new)
        self.slider_values.values[valname] = new

    ### BokehKzinRing.update_oiiivalue()

    def update_hαvalue(self,valname,attr,old,new):          # BokehKzinRing.update_hαvalue()
        """update corresponding  hαvalue slider"""
        self.hαvalue.value                 = float(new)
        self.slider_values.values[valname] = new

    ### BokehKzinRing.update_hαvalue()

#############################################################################

    def update_recordbutton(self):                          # BokehGrating::cupdate_slider()
        """Send the state to a database somewhere"""
        query = self.slider_values.insertquery()
        self.display.display(f"""Record Not Implemented\n{query}""")

    ### BokehGrating.update_recordbutton()

    def update_slider(self,memberval,attr,old,new):         # BokehGrating::cupdate_slider()
        """The slider changes.
        Remember the new slider value and send it.
        Update the text field too.
        This is a call by a lambda from many sliders, sending its
        corresponding value into the mix."""
        self. slider_values.values[memberval] = new
        self.textfields[memberval].value      = f"{new}"

    ### BokehGrating.update_slider()

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
        devstate   = dict( [ ( "wheat"   , f'"{self.slider_values.values["wheat_value"   ]}"'), # Tungstun
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
        d2         = dict([(f"{self.name}", gadgetcmd)])     # Add in my decice (instance with in one instrument) name
        d3         = dict([(f"{self.flexname}", d2)])        # Add in my 'Instrument' name (vis-a-vis other instruments)
        jdict      = json.dumps(d3)                          # make string image
        self.display.display(f'{jdict}')                    # send it to browser DIV, and off to communications port.

    ### BokehKzinRing.send_state()

    def layout(self):                                       # BokehKzinRing::layout()
        """Get the layout in gear"""
        return (row ( column ( #self.LampCheckBoxes,             # Physical layout the user.
                            row(
                              column(self.hβslider,      self.hβvalue),                    # Marker for BLUE  LED  - broad band led
                              column(self.oiiislider,    self.oiiivalue),                  # Marker for GREEN LED
                              column(self.hαslider,      self.hαvalue),                    # Marker for REF   LED

                              Spacer(width=10, height=self.wwidth//2, background='black'),

                              column(self.nearslider,    self.nearvalue),                  # Relco -

                              Spacer(width=10, height=self.wwidth//2, background='black'),

                              column(self.augflatslider, self.augvalue),                   # ... add in some BLUE LED boost
                              column(self.wheatslider,   self.wheatvalue),                 # Tungstun flat
                              column(self.flatslider,    self.flatsvalue)),                # ... and/or toss in WHITE LIGHT LED

                              Spacer(width=self.wwidth, height=5, background='black'),

                              row(self.onbutton,self.offbutton,self.recordbutton),
                              row(self.profiles)
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
