#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# (wg-python-fix-pdbrc)
# (compile (format "python -m py_compile %s" (buffer-file-name)))


### HEREHEREHERE

import os
import optparse
import sys
import re
import time
import socket
import logging

from bokeh.layouts        import column, row, Spacer
from bokeh.models         import Button, Div

HOST = '127.0.0.1'  # The server's hostname or IP address 127.0.0.1 skips resolve
PORT = 65432        # The port used by the server

#############################################################################
#
#  /home/git/external/SAS_NA1_3D_Spectrograph/Code/FlexPublish.py
#
#emacs helpers
#
# (wg-python-toc)
#
# __doc__ = """
# __author__  = 'Wayne Green'
# __version__ = '0.1'
# __all__     = ['FlexPublishException','FlexPublish','fakedisplay']   # list of quoted items to export
# class fakedisplay(object):
#    def display(self,*kwds):
#    def clear(self,*kwds):
#    def read(self,*kwds):
#    def layout(self,*kwds):
#    def postmessage(*kwds):
#    def send(*kwds):
# class FlexPublishException(Exception):
#     def __init__(self,message,errors=None):
#     @staticmethod
#     def __format__(e):
# def _fulltimestamp():
# class FlexPublish(object):
#     def __init__(self,                                # FlexPublish::__init__()
#     def configure(self,**kwds):                       # FlexPublish.configure()
#     def update_clear(self):                           # FlexPublish::update_clear()
#     def clear(self):                                  # FlexPublish.clear
#     def send(self,payload):                           # FlexPublish.send()
#     def postmessage(self,                             # FlexPublish.postmessage()
#     def display(self,msg : str = "\n",color='Bisque'): # FlexPublish.display
#     def message(self,jsonstr : str = "") -> 'self':   # FlexPublish.message()
#     def read(self):                                   # FlexPublish.read()
#     def layout(self):
#     def debug(self,msg="",skip=[],os=sys.stderr):     # FlexPublish::debug()
#
#
#
# 2022-11-09T07:40:36-0700 wlg - added postmessage
#############################################################################
__doc__ = """

/home/git/external/SAS_NA1_3D_Spectrograph/Code/Publish.py

No regression.

Send the string to the socket connection with the Flex dispatch server.
Receive data from that device, return to caller. One instance of
this class is shared between items that communicate with their
own backend server.

In addition, manage a real/fake Bokeh Div for display of messages.

An instance should not be inherited.


"""

__author__  = 'Wayne Green'
__version__ = '0.1'
__all__     = ['FlexPublishException','FlexPublish','fakedisplay']   # list of quoted items to export

_tfmt = '%Y-%m-%dT%H:%M:%S'

#############################################################################
# fakedisplay - place holder for early debugging. Retained.
#############################################################################
class fakedisplay(object):
   """Do-nothing place holder for testing Publish. Keep in sync with FlexPublish
   class
   """
   def display(self,*kwds):
       pass
   def clear(self,*kwds):
       pass
   def read(self,*kwds):
       pass
   def layout(self,*kwds):
       return row()
   def postmessage(*kwds):
      pass
   def send(*kwds):
      pass

# fakedisplay

##############################################################################
# FlexPublishException
#
##############################################################################
class FlexPublishException(Exception):
    """Special exception to allow differentiated capture of exceptions"""
    def __init__(self,message,errors=None):
        super(FlexPublishException,self).__init__("FlexPublish "+ message)
        self.errors = errors
    @staticmethod
    def __format__(e):
        return f" FlexPublish: {e.__str__()}\n"

# FlexPublishException

#############################################################################
# fulltimestamp -- blortch out a timestamp
#############################################################################
def _fulltimestamp():
   """Given a pdate, assume format suited for datetime and use it. Otherwise,
   use """
   return time.strftime(_tfmt,time.gmtime())

# fulltimestamp

_HOST = '127.0.0.1'  # Default server's hostname or IP address Isolate to localhost
_PORT = 65432        # Default port used by the server


##############################################################################
# FlexPublish
#
##############################################################################
class FlexPublish(object):
    """ Add a DIV element for use by more than one widget.
    Assemble the messages, then clear etc. A debug fashion
    for a tabbed-panel.
    Use 'postmessage() to put text into the display without
    server intervention.
    """

    brre     = re.compile(r'\n')            # Convert newline to HTML <br/>

    def __init__(self,                                # FlexPublish::__init__()
                 name    : str = "",
                 display : str = fakedisplay,
                 width   : int = 300,       # hack width
                 host    : str = _HOST,     # hostname or url
                 port    : str = _PORT      # the port that is needed
                ) -> 'self':
        """The FlexPublish class handles sending content to the backend
        server, displaying any responses. It also allows posting a message
        (postmessage) from within the code without the backend server."""

        self.message           = ""          # build up the message here. The internal log
        self.messagecnt        = 1           # form a runnning variable for messages
        self.host              = host        # ip address of the host
        self.port              = int(port)   # ducktype port as string/int
        self.wwidth            = width       # the width of the Div

        self.panel             = Div       (text="Msg", width=self.wwidth,
                                            style={'overflow-y':'auto','height':'500px'},
                                            background='Bisque')
        self.clear_button      = Button    ( label="Clear",  disabled=False,
                                             button_type="warning", width=self.wwidth)
        self.clear_button       .on_click (lambda : self.update_clear())

    ### FlexPublish.__init__()

    def configure(self,**kwds):                       # FlexPublish.configure()
        """initialize by keywords:
        host  string  the IP4 address of the host (default to localhost)
        port  the default port                    (default to 65432)
        """
        for k,v in kwds:
            if(k == "host"):
                self.host = v
            elif(k == "port"):
               self.port = int(v)
            # else ignore

    ### FlexPublish.configure()

    def update_clear(self):                           # FlexPublish::update_clear()
        """clear the interface.
        Allow a clear button in a column for the panel."""
        self.message           = ""
        self.panel.text       = FlexPublish.brre.sub("<br/>",self.message)

    ### FlexPublish.update_clear()

    def clear(self):                                  # FlexPublish.clear
        """Clean the conent and div. Permit one of the
        subscribers to clear for all."""
        self.message      = ""
        self.panel.text   = message
        self.messagecnt   = 1                   # reset the message count

        return self

    ### FlexPublish.clear

    def send(self,payload):                           # FlexPublish.send()
        """Connect to socket and send the message., Return the data.
        Designd to be called by self.display
        """
        logging.info("FlexPublish.send() starting")
        data = "CONNECTION FAILURE"             # assume the worst
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                #msg = "settimeout"
                #s.settimeout(1.5)              # seconds
                msg = "connect"
                s.connect((HOST, PORT))         # requires a tuple.
                msg = "sendall"
                s.sendall(payload.encode())     # sends bytes type
                msg = "recv"
                data = s.recv(1024)             # the returned data.
        except socket.timeout as to:
            data = f"FlexPublish: ERROR: Timeout Error to.__str__()"
            print(data)
            data = data.encode()                 # this needs to be bytes
            s.close()
        except Exception as e:
            data = f"FlexPublish: ERROR: Publish Send Error: {HOST} {PORT}\n{e.__str__()}\n{payload}\nerrmsg={msg}\n"
            print(data)
            print(f"{e.__str__()}")             # local console
            data = data.encode()                # this needs to be bytes
            s.close()
        logging.info("FlexPublish.send() complete")
        return data                             # return data or errors as bytes

    ### FlexPublish.send()

    def postmessage(self,                             # FlexPublish.postmessage()
                    msg : str = "\n",
                    color='Bisque'): # FlexPublish.postmessage
        """Append a user 'message' to the panel's div.
        Color allows for warnings, errrors etc.
        Does not interact with the dispatcher."""
        self.panel.background = color
        ts                    = _fulltimestamp()
        self.message          = self.message  +   + f'\n# {ts}\n' + f'msg{self.messagecnt} = {msg}' + "\n" # prep response
        self.panel.text       = FlexPublish.brre.sub("<br/>",self.message)   # put the text into display div
        self.messagecnt       += 1                                           # increment the variable.

        return self

    ### FlexPublish.postmessage()

    def display(self,msg : str = "\n",color='Bisque'): # FlexPublish.display
        """Send the message and append the response to the panel's div.
        Color allows for warnings, errrors etc."""
        self.panel.background = color
        ts                    = _fulltimestamp()
        retmsg                = self.send(msg).decode()                      # send the message to the dispatcher get response
        self.message          = self.message  + f'\n# {ts}\n' + f'msg{self.messagecnt} = {retmsg}' + "\n" # prep response
        self.panel.text       = FlexPublish.brre.sub("<br/>",self.message)   # put the text into display div
        self.messagecnt       += 1                                           # increment the variable.

        return retmsg

    ### FlexPublish.display()

    def message(self,jsonstr : str = "") -> 'self':   # FlexPublish.message()
       """Place to display something."""
       FlexPublish.brre.sub("<br/>",message)

       return self

    ### FlexPublish.message()

    def read(self):                                   # FlexPublish.read()
        """Return the original accumulated messages sans
        formatting."""

        return self.data

    ### FlexPublish.read()

    def layout(self):
       """Return the basic layout element for the Div"""

       return column(self.panel,self.clear_button)

    ### FlexPublish.layout()

    def debug(self,msg="",skip=[],os=sys.stderr):     # FlexPublish::debug()
        """Help with momentary debugging, file to fit.
           msg  -- special tag for this call
           skip -- the member variables to ignore
           os   -- output stream: may be IOStream etc.
        """
        import pprint
        print("FlexPublish - %s " % msg, file=os)
        for key,value in self.__dict__.items():
            if(key in skip):
               continue
            print(f'{key:20s} =',file=os,end='')
            pprint.pprint(value,stream=os,indent=4)

        return self

# class FlexPublish

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

    print("No regression", file=sys.stderr)


