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


def flexserve():
    """Tie bokeh to serial port"""
    pass



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
    HOST        = options.hostname
    PORT        = options.portnumber

    verboseflag = options.verboseflag

    if(verboseflag):
        print(f"FlexSpec1 dispatch-server.py: {HOST}")
        print(f"FlexSpec1 dispatch-server.py: {PORT}")

    print("FlexSpec1 dispatch-server.py: FlexSpec1 server started.")
    time.sleep(1)
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
