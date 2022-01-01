#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# (wg-python-fix-pdbrc)

### HEREHEREHERE
from __future__ import annotations

import os
import optparse
import sys
import re
import numpy as np
import pandas as pd
from astropy.io import fits
import socket

from typing import NewType, TypeVar
npRadianArray = NewType('bpRadianArray',np.array)  # define some better module types
millimeter    = TypeVar('millimeter',int, float)
centimeter    = TypeVar('centimeter',int, float)
angstrom      = NewType('angstrom', float)
percent       = TypeVar('percent',int,float)

#############################################################################
# 
# git FlexSpec1/Code/FlexSpec/ClientServer/FS1Client.py 
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

/home/git/external/SAS_NA1_3D_Spectrograph/Code/clientserver/FA1Client.py
[options] files...

"""

__author__  = 'Wayne Green'
__version__ = '0.1'
# from FS1Client import FA1Client,FA1ClientException
__all__     = ['FA1Client','FA1ClientException']   # list of quoted items to export

# https://www.techwithtim.net/tutorials/socket-programming/
# THIS IS THE CLIENT


##############################################################################
# FA1ClientException
#
##############################################################################
class FA1ClientException(Exception):
    """Special exception to allow differentiated capture of exceptions"""
    def __init__(self,message,errors=None):
        super(FA1ClientException,self).__init__("FA1Client "+ message)
        self.errors = errors
    @staticmethod
    def __format__(e):
        return f" FA1Client: {e.__str__()}\n"
# FA1ClientException

##############################################################################
# FA1Client
#
##############################################################################
class FA1Client(object):
    """ A client to connect out to a server somewhere.
    """
 
    DEFAULT_DISCONNECT  = "!DISCONNECT!"  # signal server to close
    DEFAULT_MESSAEGSIZE = 64
    DEFAULT_SERVER      = "localhost"     # should be a remote IP address.
    DEFAULT_PORT        = 45654

    def __init__(self, server         : str  = None, # FA1Client::__init__()
                       port           : int  = None,
                       msgsize        : int  = None,
                       disconnect_msg : str  = None,
                       name           : str  = None   # user supplied name
                 ):
        """FA1Client (server, port, msgsize [,name]) Connect to (server,port)
        and exchange messages of format=utf-8 between the server.

        """
        #super().__init__()
        # (wg-python-property-variables)
        self.SERVER             = server         or FA1Client.DEFAULT_SERVER
        self.PORT               = port           or FA1Client.DEFAULT_PORT
        self.MESSAGESIZE        = msgsize        or FA1Client.DEFAULT_MESSAEGSIZE
        self.DISCONNECT_MESSAGE = disconnect_msg or FA1Client.DEFAULT_DISCONNECT
        self.FORMAT             = 'utf-8'  # force this
        self._ADDR              = (self.SERVER, self.PORT)   # use a tuple
        self.client             = None

    ### FA1Client.__init__()

    def connect(self) -> FA1Client :                         # FA1Client.connect()
        """Make the connection, start listening"""
        if(self.client is None):
                                                    # Fammily         Type
            self.client             = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect(ADDR)  # connect, not bind.

        return self

    ### FA1Client.connect()

    def send(self,mag) -> str :                             # FA1Client.send()
        """Send a message, return a response as string
        Our convention may have a JSON string returned"""
        message        = msg.encode(self.FORMAT)  # encode then into a bytes format.
        msg_length     = len(message)
        send_length    = str(msg_length).encode(self.FORMAT)
        send_length   += b' ' * (self.MESSAGESIZE - len(send_length)) # The '*' pads
        if(self.client is None):
            raise FA1ClientException(f"FA1Client not connected. {self.debug()}  ")

        self.client.send(send_length) # this will block, response lets us send
        self.client.send(message)     # the payload message.
        received = client.recv(2048).decode(self.FORMAT)

        return received

    ### FA1Client.send()

    def disconnect(self) -> FA1Client :                      # FA1Client.disconnect()
        """Just set the client to None"""
        self.client = None

        return self

    ### FA1Client.disconnect()

    def debug(self,msg="",skip=[],os=sys.stderr) -> FA1Client :           # FA1Client::debug()
        """Help with momentary debugging, file to fit.
           msg  -- special tag for this call
           skip -- the member variables to ignore
           os   -- output stream: may be IOStream etc.
        """
        import pprint
        print("FA1Client - %s " % msg, file=os)
        for key,value in self.__dict__.items():
            if(key in skip):
               continue
            print(f'{key:20s} =',file=os,end='')
            pprint.pprint(value,stream=os,indent=4)

        return self

    ### FA1Client.debug()

    __FA1Client_debug = debug  # really preserve our debug name if we're inherited

   # (wg-python-properties properties)

# class FA1Client


##############################################################################
#                                    Main
#                               Regression Tests
##############################################################################
# HEREHEREHERE
if __name__ == "__main__":
    opts = optparse.OptionParser(usage="%prog "+__doc__)

#import optparse


    opts = optparse.OptionParser(usage="%prog"+__doc__)


    opts.add_option("-s", "--server",    action="store", dest="serverhost",
                    default="localhost",
                    help="<str IP host>   the hostname or address.")

    opts.add_option("-p", "--port",    action="store", dest="port",
                    default=5476,
                    help="<int>       port address for host.")

    opts.add_option("-v", "--verboseflag",    action="store", dest="verboseflag",
                    default=False,
                    help="<bool>        be chatty about work.")

    (options, args) = opts.parse_args()

    try:
        msg  = f"serverhost {options.serverhost}"
        host = options.serverhost
        msg  = f"port should be an int {options.port}"
        port = int(options.port)
    except Exception as e:
        if(options.verboseflag):
            print(f"FA1Client Regression - fail for {msg}")
            raise

    testclient = FA1Client(host,port)  # PDB-DEBUG

    testclient.send("Hello World!")
    input()                    # example uses a blank return to progress
    testclient.send("Hello Everyone!")
    input()
    testclient.send(f"Hello os.getenv('USER')!")
    
    testclient.send(DISCONNECT_MESSAGE)

    sys.exit(0) # PDB-DEBUG
