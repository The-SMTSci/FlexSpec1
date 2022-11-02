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
from urllib.parse    import urlparse

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
manage the network credentials between the browser and the flexdispatch
server.

"""


__author__  = 'Wayne Green'
__version__ = '0.1'
__all__     = ['FlexNetwork','FlexNetworkException']   # list of quoted items to export


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
# dumpurl - Start of a dumper for any encoded HTML traffic we send/receive
#
##############################################################################
__dumper_code = """
  elisp snippets for playing with the code.
  (setq str "{\"grating\" : {\"kzin\" : {\"halpha\" : \"1\"}}}")
  (setq str "{\"kzin\" : {\"halpha\" : \"1\"}}")
  (progn
      (setq str (replace-regexp-in-string "[\"]" "%22" str))
      (setq str (replace-regexp-in-string "[{]"  "%7B" str))
      (setq str (replace-regexp-in-string "[}]"  "%7D" str))
      (setq str (replace-regexp-in-string "[:]"  "%3A" str))
      (setq str (replace-regexp-in-string "[ ]"  "%20" str))
      (insert str)
  )
"""
def _dumpurl(x):                                            # def dumpurl()
    print(f"scheme   = {x.scheme}"  )
    print(f"hostname = {x.hostname}")
    print(f"port     = {x.port}"    )
    print(f"path     = {x.path}"    )
    print(f"query    = {x.query}"   )
    print(f"\nnetloc = {x.netloc}"  )
    print(f"params   = {x.params}"  )
    print(f"fragment = {x.fragment}")
    print(f"username = {x.username}")
    print(f"password = {x.password}")

### def dumpurl()

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
    urlre  = re.compile(r'')

    def __init__(self, flexname : 'Insrument' ,                        # FlexNetwork::__init__()
                       username = None,                     # the user's name
                       password = None,                     # password
                       hostip   = None,                     # the URL for the spectrpgraph
                       display  = fakedisplay,              # the display for our logging
                       width    = 200):                     # the default width
        """Get the details together and manage network"""
        #super().__init__()
        # (wg-python-property-variables)
        self.flexname        = flexname
        self.width           = width
        self.connected       = False
        self.display         = display
        self.connection      = None

        self.url_scheme      = None                         # the parts from url parse
        self.url_hostname    = None
        self.url_port        = None
        self.url_path        = None
        self.url_query       = None
        self.url_netloc      = None
        self.url_params      = None
        self.url_username    = None
        self.url_fragment    = None
        self.url_password    = None



        self.parsedurl       = None

        self.username        = username
        self.password        = password
        self.hostip          = hostip       # determined from the connect; passed to dispatch server


        self.connectionfield = TextInput    (title='Host URL',placeholder="flexspec://pier15.gao.flexspec.app:/help",
                                             width=self.width)  # parse
        self.userfield       = TextInput    (title='Username',width=self.width)
        self.passwordfield   = PasswordInput(title='Password',width=self.width)
        self.connectbutton   = Button       (label="Login"   ,width=self.width,  disabled=False, button_type="danger")

        self.connectionfield  .on_change("value",lambda attr, old, new: self.update_connectionfield(attr, old, new))
        self.userfield        .on_change("value",lambda attr, old, new: self.update_userfield(attr, old, new))
        self.passwordfield    .on_change("value",lambda attr, old, new: self.update_passwordfield(attr, old, new))
        self.connectbutton    .on_click(lambda : self.update_connectbutton ())

    ### FlexNetwork.__init__()

    def update_connectionfield(self,attr,old,new):              # Network::update_connectbutton()
        try:
            v = urlparse(new)
        except ValueError as ve:
            #bad parse
            self.connectionfield.value = f"{ve.__str__()}"

        self.connection = new

    def update_userfield(self,attr,old,new):                    # Network::update_connectbutton()
        self.username = new

    def update_passwordfield(self,attr,old,new):                # Network::update_connectbutton()
        self.password = new

    def update_connectbutton(self):                             # Network::update_connectbutton()
        """Update the home command. """
        self.send_state()
        self.connected = True

    def parseurl(self):
        """Parse the URL field
        https://flexspec1.readthedocs.io/en/latest/
        https://pier15.example.com:6563/roddaflex/?grating=%7B%22kzin%22%20%3A%20%7B%22halpha%22%20%3A%20%221%22%7D%7D

        """
        rawurl = self.connectionfield.value
        self.url_scheme      = rawurl.scheme                # spell out the return stuff
        self.url_hostname    = rawurl.hostname              # for clarity
        self.url_port        = rawurl.port
        self.url_path        = rawurl.path
        self.url_query       = rawurl.query
        self.url_netloc      = rawurl.netloc
        self.url_params      = rawurl.params
        self.url_username    = rawurl.username
        self.url_fragment    = rawurl.fragment
        self.url_password    = rawurl.password

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
        loginstate = dict ([ ("host"      , self.connectionfield.value ),
                             ("uname"     , self.username              ),
                             ("password"  , self.password              ),
                             ("receipt"   , "1"                        )
                           ])
        netcmd = dict([("process", loginstate)])
        d2     = dict([(f"{self.flexname.flexname}", netcmd)])
        jdict  = json.dumps(d2)    # {"process" : {"network" : {...host, uname, passwd, receipt=1...}
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

