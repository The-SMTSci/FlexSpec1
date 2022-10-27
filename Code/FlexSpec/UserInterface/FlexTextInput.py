#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Test with:
# bokeh serve FlexTextInput.py --unused-session-lifetime 3600000
# (wg-python-fix-pdbrc)
#
# (compile (format "python -m py_compile %s" (buffer-file-name)))
#
### HEREHEREHERE

import os
import sys
import io
import re
import json

from FlexPublish          import fakedisplay

from bokeh.layouts        import column, row, Spacer
from bokeh.models         import TextInput
from bokeh.models         import CustomJS, Div
from bokeh.models.widgets import Tabs, Panel


#############################################################################
#
#  /home/git/external/SAS_NA1_3D_Spectrograph/Code/FlexTextInput.py
#
# (toggle-input-method)
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
# class FlexTextInputException(Exception):
#     def __init__(self,message,errors=None):
#     @staticmethod
#     def __format__(e):
# class FlexTextInput(object):
#     def __init__(self,pname = ""):                          # FlexTextInput::__init__()
#     def update_text(attr, old, new):                        # FlexTextInput.update_text()
#     def debug(self,msg="",skip=[],os=sys.stderr):           # FlexTextInput::debug()
#     def send_state(self):                                   # FlexTextInput.send_state()
#     def layout(self):
#
#
#############################################################################
__doc__ = """

/home/git/external/SAS_NA1_3D_Spectrograph/Code/FlexTextInput.py

[options] files...

This class manages textinput communications. Ideally,
a message will be sent to server onchanges with this field.

Select the slider, fine-tune with keyboard arrows.

"""

__author__  = 'Wayne Green'
__version__ = '0.1'
__all__     = ['FlexTextInput','FlexTextInputException']   # list of quoted items to export


##############################################################################
# FlexTextInputException
#
##############################################################################
class FlexTextInputException(Exception):
    """Special exception to allow differentiated capture of exceptions"""
    def __init__(self,message,errors=None):
        super(FlexTextInputException,self).__init__("FlexTextInput "+ message)
        self.errors = errors
    @staticmethod
    def __format__(e):
        return f" FlexTextInput: {e.__str__()}\n"
# FlexTextInputException


##############################################################################
# FlexTextInput
#
##############################################################################
class FlexTextInput(object):
    """ Make a specialized TextInput box, ease of access in FlexSpec
    This is a tricky one to use.
    """

    def __init__(self,pname = "",                           # FlexTextInput::__init__()
                 display        = fakedisplay,
                 width   : int  = 200,
                 enabled : bool =True):
        """FlexTextInput - A way for the user to send information to the
        dispatch server.
        """

        self.flexname       = pname                       # The name of this box
        self.wwidth         = width                       # the width
        self.enabled        = enabled                     # is text input enabled
        self.oldtext        = None                        # remember old text
        self.display        = display                     # the display portal to the dispatch server
        
        self.fstitle        = TextInput(value=f"{self.flexname}", background='Black',
                                 disabled=self.enabled, width=self.wwidth)

        self.fstitle.js_on_change('value', lambda attr, old, new: self.update_text_slider (attr, old, new))

    ### FlexTextInput.__init__()

    def update_text(attr, old, new):                        # FlexTextInput.update_text()
        """new should be the new value for the text"""
        self.oldtext = self.text
        self.text    = new

    ### FlexTextInput.update_text()

    def debug(self,msg="",skip=[],os=sys.stderr):           # FlexTextInput::debug()
        """Help with momentary debugging, file to fit.
           msg  -- special tag for this call
           skip -- the member variables to ignore
           os   -- output stream: may be IOStream etc.
        """
        import pprint
        print("FlexTextInput - %s " % msg, file=os)
        for key,value in self.__dict__.items():
            if(key in skip):
               continue
            print(f'{key:20s} =',file=os,end='')
            pprint.pprint(value,stream=os,indent=4)
        return self

    ### FlexTextInput.debug()

    def send_state(self):                                   # FlexTextInput.send_state()
        """Send the state to Bokeh server"""
        devstate  = dict([("attribute", f'{self.text.strip()}')])
        gadgetcmd = dict([("process" , devstate)])
        d2        = dict([(f"{self.name}", gadgetcmd)])     # Add in my decice (instance with in one instrument) name
        d3        = dict([(f"{self.flexname}", d2)])        # Add in my 'Instrument' name (vis-a-vis other instruments
        jdict     = json.dumps(d3)
        print(f"FlexTextInput.send_state: {jdict}")         # debugging for now
        self.display.display(f'{jdict}')

    ### FlexTextInput.send_state

    def layout(self):
        """Do the layout"""
        return row(self.text)
    ### FlexTextInput.send_state()

   # (wg-python-properties properties)

# class FlexTextInput

##############################################################################
#                                    Main
#                               Regression Tests
##############################################################################
# HEREHEREHERE
if(0):
    from bokeh.io             import curdoc

    opts = optparse.OptionParser(usage="%prog "+__doc__)

    opts.add_option("-v", "--verbose", action="store_true", dest="verboseflag",
                   default=False,
                   help="<bool>     be verbose about work.")

    (options, args) = opts.parse_args()


#    curdoc().add_root(column(kzin1.layout(), kzin2.layout()))
#    curdoc().theme = 'dark_minimal'
#    curdoc().title = "Lamp1 Test"
