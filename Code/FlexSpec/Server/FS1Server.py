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
import socket
import threading

#############################################################################
# git FlexSpec1/Code/FlexSpec/ClientServer/FS1Server.py 
#  
#
#emacs helpers
# (insert (format "\n# %s " (buffer-file-name)))
#
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

  clientserver/FS1Server.py
[options] files...

The FS1Server is a class that listens on a port on 'this' machine
(its a server); for messages of fixed length utf-8 characers.
If it sees the message starting with disconnect_msg it will stop
the loop and hangup.

https://stackoverflow.com/questions/6380057/python-binding-socket-address-already-in-use


"""

__author__  = 'Wayne Green'
__version__ = '0.1'
# from FS1Server import FS1Server, FS1ServerException
__all__     = ['FS1Server','FS1ServerException']

##############################################################################
# FS1ServerException
#
##############################################################################
class FS1ServerException(Exception):
    """Special exception to allow differentiated capture of exceptions"""
    def __init__(self,message,errors=None):
        super(FS1ServerException,self).__init__("FS1Server "+ message)
        self.errors = errors
    @staticmethod
    def __format__(e):
        return f" FS1Server: {e.__str__()}\n"
# FS1ServerException

##############################################################################
# FS1Server
#
##############################################################################
class FS1Server(object):
    """ Make a server side for FS1Server.
    """
    #__slots__ = [''] # add legal instance variables
    # (setq properties `("" ""))

    DEFAULT_MESSAGESIZE = 256              # a message is always 64 bytes, this example
    DEFAULT_SERVER      = socket.gethostbyname(socket.gethostname())
    DEFAULT_PORT        = 45654            # my cute port address
    ADDR                = (DEFAULT_SERVER, DEFAULT_PORT)   # use a tuple
    FORMAT              = 'utf-8'          # basic ASCII like strings
    DEFAULT_DISCONNECT  = "!DISCONNECT!"   # signal server to close

    def __init__(self, port           : int  = None, # FS1Server::__init__()
                       msgsize        : int  = None,
                       disconnect_msg : str  = None,
                       serverip       : str  = None,  # '127.0.0.1',
                       ostream        : _io.TextIOWrapper = sys.stdout
                ):
        """Defaults to localhost, and to port 45654"""

        self.PORT               = port           or FS1Server.DEFAULT_PORT
        self.SERVER             = serverip       or FS1Server.DEFAULT_SERVER
        self.MESSAGESIZE        = msgsize        or FS1Server.DEFAULT_MESSAGESIZE
        self.DISCONNECT_MESSAGE = disconnect_msg or FS1Server.DEFAULT_DISCONNECT
        self.FORMAT             = 'utf-8'        # force this
        self._ADDR              = (self.SERVER, self.PORT)   # use a tuple
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(self._ADDR)             # bind these two using the tuple
        self.ostream            = ostream        # place for print to dump things.

    ### FS1Server.__init__()

    def debug(self, msg="", skip=[], os=sys.stderr):           # FS1Server::debug()
        """Help with momentary debugging, file to fit.
           msg  -- special tag for this call
           skip -- the member variables to ignore
           os   -- output stream: may be IOStream etc.
        """
        import pprint
        print("FS1Server - %s " % msg, file=os)
        for key,value in self.__dict__.items():
            if(key in skip):
               continue
            print(f'{key:20s} =', file=os, end='')
            pprint.pprint(value,stream=os,indent=4)
        return self

    ### FS1Server.debug()

    __FS1Server_debug = debug  # really preserve our debug name if we're inherited

    @staticmethod
    def handle_client(conn, addr):
        """Method is on a separate thread. Handle the single connection with a
        thread (below) Messages are two exchanges, one is the pad
        "length", the last is the padded message
        client -> "ing(len)" + b' ' * FS1Server.MESSAGESIZE - (sizeof msg)
        result = client -> 'payload' + b' ' * FS1Server.MESSAGESIZE - (sizeof payload)

        """
        print(f"[NEW CONNECTION] {addr} connected.",file=self.ostream)

        connected = True
        while connected:
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if msg_length:  # the first message has a None so skip that one
                msg_length = int(msg_length)                       # blocks
                msg        = conn.recv(msg_length).decode(FORMAT)  # blocks
                if msg == FS1Server.DISCONNECT_MESSAGE:
                    connected = False
                if(1): print(f"[{addr}] {msg}")
                conn.send("Msg received".encode(FORMAT))  # reply something to client.

        conn.close() # close the current connection, exit this thread,

    # handle_client

    def start(self):
        """Allow the socket to start listening for connections.
        This winds up being a thread."""
        self.server.listen()
        if(1): print(f"[LISTENING] Server is listening on {self.SERVER}",file=sys.stderr)
        while True:
            conn, addr = self.server.accept()  # server.accept 'blocks' until the connection
            print("conn ",conn)
            thread     = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
            if(1): print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}",file=sys.stderr)
    # start

    def write(self,msg):
        """Pass along msg to subclass"""
        pass

    def read(self,character):
        """Get a message from sub-class. Follow some protocol."""
        raise FS1ServerException("FS1Server::read Unimplemented.")
        #pass

# class FS1Server

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

    print("hello")   # PDB-DEBUG
    testserver = FS1Server()
    print("[STARTING] server is starting...")
    testserver.debug()
    testserver.start()

