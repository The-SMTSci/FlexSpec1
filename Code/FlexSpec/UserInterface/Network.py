#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# (wg-python-fix-pdbrc)

### HEREHEREHERE

import os
import optparse
import sys
import re
import json
from FlexPublish          import fakedisplay

from bokeh                import events
from bokeh.events         import ButtonClick
from bokeh.io             import curdoc
from bokeh.layouts        import column, row, Spacer
from bokeh.models         import ColumnDataSource, Slider, TextInput, Button, PasswordInput
from bokeh.models         import Spacer
from bokeh.models         import CustomJS, Div
from bokeh.plotting       import figure
from bokeh.models         import RadioGroup
from bokeh.models         import Select
from bokeh.models.widgets import Tabs, Panel


#############################################################################
#
#  /home/git/external/FlexSpec1/Code/FlexSpec/UserInterface/Network.py
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

/home/git/external/FlexSpec1/Code/FlexSpec/UserInterface/Network.py
[options] files...



"""


__author__  = 'Wayne Green'
__version__ = '0.1'
__all__     = ['','']   # list of quoted items to export


##############################################################################
# FlexNetworkException
#
##############################################################################
class FlexNetworkException(Exception):
    """Special exception to allow differentiated capture of exceptions"""
    def __init__(self,message,errors=None):
        super(FlexNetworkException,self).__init__("FlexNetwork "+ message)
        self.errors = errors
    @staticmethod
    def __format__(e):
        return f" FlexNetwork: {e.__str__()}\n"
# FlexNetworkException


##############################################################################
# FlexNetwork
#
# Username
# password
# hostip
# port
#
#
#
##############################################################################
class FlexNetwork(object):
    """ Handle the  username, password, host ip, port
    """
    #__slots__ = [''] # add legal instance variables
    # (setq properties `("" ""))
    def __init__(self, flexname,                        # FlexNetwork::__init__()
                       name     = "Network",
                       username = None,
                       password = None,
                       hostip   = None,
                       port     = None,
                       display  = fakedisplay,
                       width    = 200):
        """Get the details together and manage network"""
        #super().__init__()
        # (wg-python-property-variables)
        self.flexname        = flexname
        self.name            = name
        self.width           = width
        self.connected       = False
        self.display         = display
        self.connection      = None

        self.username        = username
        self.password        = password
        self.hostip          = hostip       # determined from the connect; passed to dispatch server
        self.port            = port         # dispatch loops back with success of the login

        self.connectionfield = TextInput    (title='Host Path',width=self.width)
        self.userfield       = TextInput    (title='Username',width=self.width)
        self.passwordfield   = PasswordInput(title='Password',width=self.width)
        self.connectbutton   = Button       (label="Login"   ,width=self.width//2,  disabled=False, button_type="default")

        self.connectionfield  .on_change("value",lambda attr, old, new: self.update_connectionfield(attr, old, new))
        self.userfield        .on_change("value",lambda attr, old, new: self.update_userfield(attr, old, new))
        self.passwordfield    .on_change("value",lambda attr, old, new: self.update_passwordfield(attr, old, new))
        self.connectbutton    .on_click(lambda : self.update_connectbutton ())

    ### FlexNetwork.__init__()

    def update_connectionfield(self,attr,old,new):              # Network::update_connectbutton()
        self.connectionfield = new

    def update_userfield(self,attr,old,new):                    # Network::update_connectbutton()
        self.username = new

    def update_passwordfield(self,attr,old,new):                # Network::update_connectbutton()
        self.password = new

    def update_connectbutton(self):                             # Network::update_connectbutton()
        """Update the home command. """
        self.send_state()
        self.connected = True

    ### Network.update_connectbutton()

    def layout(self):                                           # Network::layout()
        """Create the layout"""
        return(row ( column ( self.connectionfield,
                              self.userfield    ,
                              self.passwordfield,
                             row(self.connectbutton)
                            )  ))

    ### Network.layout()

    def send_state(self):                                       # Network.send_state()
        loginstate = dict ([ ("User Name",self.username),
                             ("Password",self.password)
                           ])
        netcmd = dict([("Process", loginstate), ("RRR" , 0)])
        d2 = dict([(f"{self.name}", netcmd)])
        d3 = dict([(f"{self.flexname}", d2)])
        jdict = json.dumps(d3)
        self.display.display(f'{jdict}')

    ### Network.send_state()

    def debug(self,msg="",skip=[],os=sys.stderr):           # FlexNetwork::debug()
        """Help with momentary debugging, file to fit.
           msg  -- special tag for this call
           skip -- the member variables to ignore
           os   -- output stream: may be IOStream etc.
        """
        import pprint
        print("FlexNetwork - %s " % msg, file=os)
        for key,value in self.__dict__.items():
            if(key in skip):
               continue
            print(f'{key:20s} =',file=os,end='')
            pprint.pprint(value,stream=os,indent=4)

        return self

    ### FlexNetwork.debug()

    __FlexNetwork_debug = debug  # really preserve our debug name if we're inherited

   # (wg-python-properties properties)

# class FlexNetwork



##############################################################################
#                                    Main
#                               Regression Tests
##############################################################################
# HEREHEREHERE
if __name__ == "__main__":
    opts = optparse.OptionParser(usage="%prog "+__doc__)

    opts.add_option("-v", "--verbose", action="store_true", dest="verboseflag",
                   default=False,
                   help="<bool>     be verbose about work.")

    (options, args) = opts.parse_args()

    # (wg-python-atfiles)
    for filename in args:
        with open(filename,'r') if filename else sys.stdin as f:
            for l in f:
                if('#' in l):
                    continue
                parts = map(str.strip,l.split())

