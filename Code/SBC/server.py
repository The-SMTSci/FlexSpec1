#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# (wg-python-fix-pdbrc)

### HEREHEREHERE
import socket
import time
#import systemd.daemon

import optparse             # flexibility for non-systemd starting.

__doc__ = """

/home/git/external/FlexSpec1/Code/SBC/server.py
[options] files... The Postmaster for FlexSpec1



"""

__author__  = 'Wayne Green'
__version__ = '0.1'


HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)
flag = 1



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
    if(options.verboseflag):
        print(f"server.py: {HOST}")
        print(f"server.py: {PORT}")

    print("server.py: FlexSpec1 server started.")
    time.sleep(100)
    #systemd.daemon.notify('READY=1')

    while(flag):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            conn, addr = s.accept()
            with conn:
                print('server.py: Connection from:', addr)
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    conn.sendall(data)
                    print(f"{data}")
                    if(data == b'end'):
                        flag = 0
            print("server.py: Connection transaction complete.")
    
    print("Socket complete, exiting")
