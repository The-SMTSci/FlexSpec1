#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# (wg-python-fix-pdbrc)

### HEREHEREHERE
import socket
import time
import sys
import abc
import serial
#import systemd.daemon

import optparse             # flexibility for non-systemd starting.

__doc__ = """

/home/git/external/FlexSpec1/Code/SBC/server.py
[options] files... The Postmaster for FlexSpec1

localhost usually resolves to 127.0.0.1, use 127.0.0.1 for faster work

    HOST
    HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
    SERIALPORT
    flag = 1

"""

__author__  = 'Wayne Green'
__version__ = '0.1'

HOST = '0.0.0.0'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)
SERIALPORT=None     # declare a serialport

_flag = 1           # local flag to halt the processing loop
                    # triggered if data == b'end'


##############################################################################
# InstrumentException
#
##############################################################################
class InstrumentException(Exception):
    """Special exception to allow differentiated capture of exceptions"""
    def __init__(self,message,errors=None):
        super(InstrumentException,self).__init__("Instrument "+ message)
        self.errors = errors
    @staticmethod
    def __format__(e):
        return f" Instrument: {e.__str__()}\n"
# InstrumentException


##############################################################################
# Instrument
#
##############################################################################
class Instrument(object):
    """ Tie a logical name to physical port management details.
       open   - Establish the status for the port
       close  - Not recommended (pass)
       read   - read a string from the interface
       write  - write string to interface
       Report - return a report for this device
    """
    #__slots__ = [''] # add legal instance variables
    # (setq properties `("" ""))
    def __init__(self,name :str = "FlexSpec"):              # Instrument::__init__()
        """Initialize this class."""
        #super().__init__()
        # (wg-python-property-variables)
        self.name = name

    ### Instrument.__init__()

    def open  (): pass
    def close (): pass
    def read  (): pass
    def write (): pass
    def Report(): pass


    def debug(self,msg="",skip=[],os=sys.stderr):           # Instrument::debug()
        """Help with momentary debugging, file to fit.
           msg  -- special tag for this call
           skip -- the member variables to ignore
           os   -- output stream: may be IOStream etc.
        """
        import pprint
        print("Instrument - %s " % msg, file=os)
        for key,value in self.__dict__.items():
            if(key in skip):
               continue
            print(f'{key:20s} =',file=os,end='')
            pprint.pprint(value,stream=os,indent=4)
        return self

    ### Instrument.debug()

    __Instrument_debug = debug  # really preserve our debug name if we're inherited

   # (wg-python-properties properties)

# class Instrument


##############################################################################
#                                    Main
#                               Regression Tests
##############################################################################
# HEREHEREHERE
if __name__ == "__main__":
    opts = optparse.OptionParser(usage="%prog "+__doc__)

    opts.add_option("-i", "--host", action="store", dest="hostname",
                   default='127.0.0.1',
                   help="<ip Address>     be verbose about work.")

    opts.add_option("-p", "--port", action="store", dest="portnumber",
                   default=65432,
                   help="<int>     port number.")

    opts.add_option("-v", "--verbose", action="store_true", dest="verboseflag",
                   default=False,
                   help="<bool>     be verbose about work.")

    (options, args) = opts.parse_args()
    HOST = options.hostname
    PORT = options.portnumber

    verboseflag = options.verboseflag

    if(verboseflag):
        print(f"FlexSpec1 dispatch-server.py: {HOST}")
        print(f"FlexSpec1 dispatch-server.py: {PORT}")

    print("FlexSpec1 dispatch-server.py: FlexSpec1 server started.")
    time.sleep(100)
    #systemd.daemon.notify('READY=1')
    flag = True
    if(verboseflag):
       msg = "starting loop" ; print(f"msg flag = {flag}")
    while(flag):
        try:
            if(verboseflag):
                msg = "opening socket" ; print(f"msg")
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                if(verboseflag):
                    msg = "bind" ; print(f"{msg}")
                s.bind((HOST, PORT))
                if(verboseflag):
                    msg = "listen" ; print(f"{msg}")
                s.listen()
                if(verboseflag):
                    msg = "accept" ; print(f"{msg}")
                conn, addr = s.accept()
                with conn:
                    print('FlexSpecServer.py: Connection from:', addr)
                    while True:
                        if(verboseflag):
                            msg = "data" ; print(f"{msg} conn={conn} addr={addr}")
                        data = conn.recv(1024)
                        if not data:
                            break
                        conn.sendall(data)
                        print(f"FlexSpecServer: {data}")        # local console
                        if(data == b'end'):
                            flag = 0
                print("FlexSpec1 dispatch-server.py: Connection transaction complete.")
        except Exception as e:
            print(f"FlexSpecServer ERROR: {e.__str__()}")
    
    print("Socket complete, exiting")
