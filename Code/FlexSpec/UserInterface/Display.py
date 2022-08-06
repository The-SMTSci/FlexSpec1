#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# (wg-python-fix-pdbrc)

### HEREHEREHERE

import os
import optparse
import sys
import re
import time
import socket

from bokeh.layouts        import column, row, Spacer
from bokeh.models         import Button, Div

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

#############################################################################
#
#  /home/git/external/SAS_NA1_3D_Spectrograph/Code/Display.py
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

/home/git/external/SAS_NA1_3D_Spectrograph/Code/Display.py

No regression.

Manage a Bokeh Div for display of messages. One instance shared
between various things.

The instance should not be inherited, but a class member.


"""

__author__  = 'Wayne Green'
__version__ = '0.1'
__all__     = ['FlexDisplayException','FlexDisplay','fakedisplay']   # list of quoted items to export

_tfmt = '%Y-%m-%dT%H:%M:%S'
#############################################################################
# fakedisplay
#############################################################################
class fakedisplay(object):
   """Placeholder for things"""
   def display(self,*kwds):
       pass
   def clear(self,*kwds):
       pass
   def read(self,*kwds):
       pass
   def layout(self,*kwds):
       return row()

# fakedisplay

##############################################################################
# FlexDisplayException
#
##############################################################################
class FlexDisplayException(Exception):
    """Special exception to allow differentiated capture of exceptions"""
    def __init__(self,message,errors=None):
        super(FlexDisplayException,self).__init__("FlexDisplay "+ message)
        self.errors = errors
    @staticmethod
    def __format__(e):
        return f" FlexDisplay: {e.__str__()}\n"
# FlexDisplayException

#############################################################################
# fulltimestamp -- blortch out a timestamp
#############################################################################
def fulltimestamp():
   """Given a pdate, assume format suited for datetime and use it. Otherwise,
   use """
   return time.strftime(_tfmt,time.gmtime())

# fulltimestamp


##############################################################################
# FlexDisplay
#
##############################################################################
class FlexDisplay(object):
    """ Add an DIV element for use by more than one outfit.
    Assemble the messages, then clear etc. A debug fashion
    for a tabbed-panel.
    """
    #__slots__ = [''] # add legal instance variables
    # (setq properties `("" ""))

    brre     = re.compile(r'\n')                         # used to convert newline to <br/>

    def __init__(self, 
                 name    : str = "",
                 display : str = fakedisplay,
                 width   : int = 300):               # FlexDisplay::__init__()
        """Initialize this class."""
        #super().__init__()
        # (wg-python-property-variables)
        self.message           = ""
        self.wwidth            = width
        self.panel             = Div       (text="Msg", width=self.wwidth,
                                            style={'overflow-y':'scroll','height':'500px'},
                                            background='Bisque')
        self.clear_button      = Button    ( label="Clear",  disabled=False,
                                             button_type="warning", width=self.wwidth)
        self.clear_button       .on_click (lambda : self.update_clear())

    ### FlexDisplay.__init__()

    def update_clear(self):                           # FlexDisplay::update_clear()
        """Update the parallactic angle. Disabled in interface.
        Allow a clear button in a column for the panel."""
        self.message           = ""
        self.display("Cleared.")

    ### FlexDisplay.update_clear()

    def clear(self):                                  # FlexDisplay.clear
        """Clean the conent and div. Permit one of the
        subscribers to clear for all."""
        self.message = ""
        self.panel.text       = message
        return self

    ### FlexDisplay.clear

    def send(self,msg):
       """Connect to socket and send the message."""
       try:
           with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
               s.connect((HOST, PORT))
               s.sendall(msg.encode())
               data = s.recv(1024)
       except Exception as e:
           print(f"Display Send Error: {HOST} {PORT}\n{msg}")
           print(f"{e.__str__()}")
           s.close()

    def display(self,msg : str = "\n",color='Bisque'):                 # FlexDisplay.display
        """append to content display to the div """
        self.panel.background = color
        ts                    = fulltimestamp()
        self.message          = self.message  + f'\n# {ts}\n' + msg + "\n"
        self.panel.text       = FlexDisplay.brre.sub("<br/>",f'{self.message}')
        self.send(msg)
        return self

    ### FlexDisplay.display()

    def read(self):                                   # FlexDisplay.read()
        """Return the original accumulated messages sans
        formatting."""
        return self.message
        return self

    ### FlexDisplay.read()

    def layout(self):
       """Return the basic layout element for the Div"""
       return column(self.panel,self.clear_button)

    ### FlexDisplay.layout()

    def debug(self,msg="",skip=[],os=sys.stderr):     # FlexDisplay::debug()
        """Help with momentary debugging, file to fit.
           msg  -- special tag for this call
           skip -- the member variables to ignore
           os   -- output stream: may be IOStream etc.
        """
        import pprint
        print("FlexDisplay - %s " % msg, file=os)
        for key,value in self.__dict__.items():
            if(key in skip):
               continue
            print(f'{key:20s} =',file=os,end='')
            pprint.pprint(value,stream=os,indent=4)
        return self

    ### FlexDisplay.debug()

    __FlexDisplay_debug = debug  # really preserve our debug name if we're inherited


# class FlexDisplay

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

    print("No regression", file=sys.stderr)


