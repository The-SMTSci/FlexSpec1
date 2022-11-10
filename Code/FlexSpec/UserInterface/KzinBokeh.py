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
from bokeh.models         import CheckboxButtonGroup, ColumnDataSource, Slider, TextInput, Button
from bokeh.models         import Tooltip, CustomJS, Div
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
#     def __init__(self, flexname : str = "Default",          # BokehKzinRing::__init__()
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
# 2022-11-08T07:48:24-0700 - moved to new instrumnet as name concept.
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

    brre        = re.compile(r'\n')                         # used to convert newline to <br/>

    ##################################################################
    #  SliderValues an Internal instance placeholder to sidestep
    #  call by reference in python.
    ##################################################################
    class SliderValues(object):                             # BokehKzinRing.SliderValues
        """Manage object values"""
        def __init__(self):
            self.values = dict(( # the storage location for current
            ('GoW'    ,"0"),    # state of the Bokeh idea of the Kzin gadget...
            ('NeAr'   ,"0"),    # manipulated by the sliders/text fields etc below.
            ('Boost'  ,"0"),    # there is a shutter that needs to be here.
            ('Flat'   ,"0"),    # named for the textfield
            ('Hβ'     ,"0"),
            ('O[III]' ,"0"),
            ('Hα'     ,"0")
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

    # BokehKzinRing.SliderValues

    ##################################################################
    #  BokehKzinRing Class
    #
    ##################################################################
    def __init__(self, instrument : 'Flex_Instrument',          # BokehKzinRing::__init__()
                 gadgetname   : str = "kzin",
                 display          : 'FlexPublish' = fakedisplay,
                 width            : int = 250,
                 shutter          : 'FlexShutter' = None):
        """Setup the UI, manage the callbacks, layout, messaging etc for the
        Kzin widget."""

        self.wwidth              = width               # overall width of the display area
        self.display             = display.display     # the FlexPublish display widget
        self.flexname            = instrument.flexname # the string that is the instrument's gadgetname
        self.gadgetname          = gadgetname          # 
        self.display             = instrument.display  # FlexPublish to send text to
        self.receipt             = 1                   # always ask for an update
        self.shutter             = shutter             # if one is in the mix

        self.slider_values       = BokehKzinRing.SliderValues()

        self.gowcolor            = 'darkkhaki'         # manage the slider color values in one place
        self.nearcolor           = 'fuchsia'           # https://docs.bokeh.org/en/latest/docs/reference/colors.html
        self.boostcolor          = 'dodgerblue'
        self.flatcolor           = 'silver'
        self.oiii                = 'mediumslateblue'
        self.hβ                  = 'lime'
        self.hα                  = 'firebrick'
        pwidth                   = self.wwidth//12                       # uniform width/spacing
        twidth                   = self.wwidth//8


######################################### associated text inputs ###################################

        self.wheatvalue     = TextInput(title='GoW'   ,width=twidth)   # Text fields titles are THE SAME as the slicers
        self.nearvalue      = TextInput(title='NeAr'  ,width=twidth)
        self.augvalue       = TextInput(title='Boost' ,width=twidth)
        self.flatsvalue     = TextInput(title='Flat'  ,width=twidth)
        self.hβvalue        = TextInput(title='Hβ'    ,width=twidth)
        self.oiiivalue      = TextInput(title='O[III]',width=twidth)
        self.hαvalue        = TextInput(title='Hα'    ,width=twidth)

        self.wheatvalue     .on_change("value", lambda attr, old, new: self.update_textfield (self.wheatvalue    , attr, old, new))
        self.nearvalue      .on_change("value", lambda attr, old, new: self.update_textfield (self.nearvalue     , attr, old, new))
        self.augvalue       .on_change("value", lambda attr, old, new: self.update_textfield (self.augvalue      , attr, old, new))
        self.flatsvalue     .on_change("value", lambda attr, old, new: self.update_textfield (self.flatsvalue    , attr, old, new))
        self.hβvalue        .on_change("value", lambda attr, old, new: self.update_textfield (self.hβvalue       , attr, old, new))
        self.oiiivalue      .on_change("value", lambda attr, old, new: self.update_textfield (self.oiiivalue     , attr, old, new))
        self.hαvalue        .on_change("value", lambda attr, old, new: self.update_textfield (self.hαvalue       , attr, old, new))



        self.textfields = dict([ ("wheat_value"   , self.wheatvalue  ),   # map the membername to its textinput widget
                                 ("near_value"    , self.nearvalue   ),
                                 ("augflat_value" , self.augvalue    ),
                                 ("flat_value"    , self.flatsvalue  ),
                                 ("hbeta_value"   , self.hβvalue     ),
                                 ("oiii_value"    , self.oiiivalue   ),
                                 ("halpha_value"  , self.hαvalue     )
                              ])

######################################### Bokeh Sliders ############################################

        self.wheatslider    = Slider(title=f"GoW", bar_color='firebrick', orientation='vertical',
                                     background=self.gowcolor, direction='rtl',
                                     value = -1, start = -1,  end = 100, step = 0.1, width=self.wwidth//8)
        self.nearslider     = Slider(title=f"Cal", bar_color='firebrick', orientation='vertical',
                                     background=self.nearcolor, direction='rtl',
                                     value = -1, start = -1,  end = 100, step = 0.1, width=self.wwidth//8)
        self.augflatslider  = Slider(title=f"UV", bar_color='firebrick', orientation='vertical',
                                     background=self.boostcolor, direction='rtl',
                                     value = -1, start = -1,  end = 100, step = 0.1, width=self.wwidth//8)
        self.flatslider     = Slider(title=f"Flat", bar_color='firebrick', orientation='vertical',
                                     background=self.flatcolor, direction='rtl',
                                     value = -1, start = -1,  end = 100, step = 0.1, width=self.wwidth//8)
        self.hβslider       = Slider(title=f"Hβ", bar_color='firebrick',orientation='vertical',
                                     background=self.oiii, direction='rtl',
                                     value = -1, start = -1,  end = 100, step = 100, width=self.wwidth//8)
        self.oiiislider     = Slider(title=f"O[III]", bar_color='firebrick',orientation='vertical',
                                     background=self.hβ, direction='rtl',
                                     value = -1, start = -1, end = 100, step = 100, width=self.wwidth//8)
        self.hαslider       = Slider(title=f"Hα", bar_color='firebrick',orientation='vertical',
                                     background=self.hα, direction='rtl',
                                     value = -1, start = -1,  end = 100, step = 100, width=self.wwidth//8)

        # slider                                                       single func   working on  widget  with values
        self.wheatslider    .on_change('value', lambda attr, old, new: self.update_slider (self.wheatvalue , attr, old, new))
        self.nearslider     .on_change('value', lambda attr, old, new: self.update_slider (self.nearvalue, attr, old, new))
        self.augflatslider  .on_change('value', lambda attr, old, new: self.update_slider (self.augvalue  , attr, old, new))
        self.flatslider     .on_change('value', lambda attr, old, new: self.update_slider (self.flatsvalue, attr, old, new))
        self.hβslider       .on_change('value', lambda attr, old, new: self.update_slider (self.hβvalue   , attr, old, new))
        self.oiiislider     .on_change('value', lambda attr, old, new: self.update_slider (self.oiiivalue , attr, old, new))
        self.hαslider       .on_change('value', lambda attr, old, new: self.update_slider (self.hαvalue   , attr, old, new))

########################################## Actions #################################################
        self.configurations = ["Recent", "Default"]
        self.savebutton     = Button    (label=f"Save",  align='end', disabled=False,
                                              button_type="success", width=pwidth)
        self.resetbutton    = Button    (label=f"Reset",  align='end', disabled=False,
                                              button_type="success", width=pwidth)
        self.onbutton       = Button    (label=f"On", align='end',  disabled=False,
                                                   button_type="warning", width=5*pwidth)
        self.offbutton      = Button    (label=f"Off",  align='end', disabled=False,
                                                   button_type="success", width=5*pwidth)

        self.profiles            = Select(title="Load Recent Configuration", options = self.configurations, width = self.wwidth)

        self.savebutton    .on_click (lambda : self.update_savebutton())
        self.resetbutton   .on_click (lambda : self.update_resetbutton())
        self.onbutton      .on_click (lambda : self.update_onbutton())
        self.offbutton     .on_click (lambda : self.update_offbutton())

###################################################################################################
        #self.resettip            = Tooltip(content="Reset to off (-1) do not send to instrument.", position="right", target=self.resetbutton)


########################################### textinput actions ######################################
        self._reset()                                                  # mimic behavior of reset value.

        ### BokehGrating.__init__()

    # react to a textinput's change

    def update_textfield(self,widget,attr,old,new):        # BokehGrating.update_textfield()
        """For the widget, update the text field,
        then using the widget.name remember the new value"""
        widget.value = f"{new}"
        self.slider_values.values[widget.name] = new

    ### BokehGrating.update_textfield()

    def _reset(self):                                      # BokehGrating._reset()
        """Reset the widgets"""
        self.wheatslider    .value = -1
        self.nearslider     .value = -1
        self.augflatslider  .value = -1
        self.flatslider     .value = -1
        self.hβslider       .value = -1
        self.oiiislider     .value = -1
        self.hαslider       .value = -1

    ### BokehGrating._reset()

    def update_resetbutton(self):                          # BokehGrating::cresetbutton()
        """Reset the sliders, but do not send anything."""
        query = self.slider_values.insertquery()
        # all sliders and text = -1
        self._reset()

    ### BokehGrating.update_resetbutton()

    def update_savebutton(self):                          # BokehGrating::csavebutton()
        """Send the state to a database somewhere"""
        query = self.slider_values.insertquery()
        self.display.display(f"""Record Not Implemented\n{query}""")

    ### BokehGrating.update_savebutton()

    def update_slider(self,textfield,attr,old,new):         # BokehGrating::cupdate_slider()
        """The slider changes.
        Remember the new slider value and send it.
        Update the text field too.
        This is a call by a lambda from many sliders, sending its
        corresponding value into the mix."""
        self. slider_values.values[textfield.name] = new
        textfield.value                       = f"{new}"

    ### BokehGrating.update_slider()

    def update_offbutton(self):                             # BokehKzinRing::update_offbutton()
        """Set internal variables to off."""
        self.onoff = 0
        msg = self.send_state()

    ### BokehKzinRing.update_offbutton()

    def update_onbutton(self):                              # BokehKzinRing::update_button_in()
        """update_onbutton Button via an event lambda"""
        #os = io.StringIO()
        #self.debug(f"{self.gadgetname} Debug",skip=['varmap'], os=os)
        #os.seek(0)
        self.display.display(BokehKzinRing.brre.sub("<br/>",f"Things in onbutton{dir(self.onbutton._property_values)}"))
        self.onoff = 1
        msg = self.send_state()

    ### BokehKzinRing.update_onbutton()

    def update_debugbtn(self):                              # BokehKzinRing::update_button_in()
        """update_debugbtn Button via an event lambda"""
        os = io.StringIO()
        self.debug(f"{self.gadgetname} Debug", os=os)
        os.seek(0)
        self.display.display(BokehKzinRing.brre.sub("<br/>",os.read()))

    ### BokehKzinRing.update_edebugbtn()

    def send_state(self):                                   # BokehKzinRing::send_state()
        """Several ways to send things
           schematic  2021-08-27T11:32:01-0600
        """
        #                    JSON TXT      Bokeh                    PY Variable
        devstate   = dict( [ ( "wheat"   , f'"{self.slider_values.values["GoW"    ]}"'), # Tungstun
                             ( "callamp" , f'"{self.slider_values.values["NeAr"   ]}"'), # CAL Relco
                             ( "hbeta"   , f'"{self.slider_values.values["Hβ"     ]}"'), # M3 BLUE LED
                             ( "oiii"    , f'"{self.slider_values.values["O[III]" ]}"'), # M2 GREEN LED
                             ( "halpha"  , f'"{self.slider_values.values["Hα"     ]}"'), # M1 RED LED
                             ( "uvboost" , f'"{self.slider_values.values["Boost"  ]}"'), # Blue boost
                             ( "flat"    , f'"{self.slider_values.values["Flat"   ]}"'), # MID WHITE LED
                             ( "state"   , f'"{self.onoff}"'),                           # State  ON/OFF
                             ( "receipt" , f'"{self.receipt}"')                          # get update
                           ])

        gadgetcmd  = dict([("process", devstate)])
        d2         = dict([(f"{self.gadgetname}", gadgetcmd)])     # Add in my decice (instance with in one instrument) gadgetname
        d3         = dict([(f"{self.flexname}", d2)])        # Add in my 'Instrument' gadgetname (vis-a-vis other instruments)
        jdict      = json.dumps(d3)                          # make string image

        self.display.display(f'{jdict}')                     # send it to browser DIV, and off to communications port.

    ### BokehKzinRing.send_state()

    def layout(self):                                       # BokehKzinRing::layout()
        """Get the layout in gear"""
        spacer = Spacer(width=self.wwidth, height=2, background='black')
        return (row ( column ( #self.LampCheckBoxes,             # Physical layout the user.
                            row(
                                column(self.hβslider,      self.hβvalue),                    # Marker for BLUE  LED  - broad band led
                                column(self.oiiislider,    self.oiiivalue),                  # Marker for GREEN LED
                                column(self.hαslider,      self.hαvalue),                    # Marker for REF   LED

                                Spacer(width=10, height=self.wwidth//2, background='black'), # vertical separator 

                                column(self.nearslider,    self.nearvalue),                  # Relco -

                                Spacer(width=10, height=self.wwidth//2, background='black'), # vertical separator 

                                column(self.augflatslider, self.augvalue),                   # ... add in some BLUE LED boost
                                column(self.wheatslider,   self.wheatvalue),                 # Tungstun flat
                                column(self.flatslider,    self.flatsvalue)                  # ... and/or toss in WHITE LIGHT LED
                                ),
                            row(self.onbutton,self.offbutton,self.resetbutton),
                            row(self.savebutton, Spacer(width=5,background='white'),self.profiles), # The configurations
                            #row(self.shutter.layout()][self.shutter is None])          # hack shutter if needed
                            self.shutter.layout()          # hack shutter if needed
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

    __BokehKzinRing_debug = debug  # really preserve our debug gadgetname if we're inherited

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
