#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# (wg-python-fix-pdbrc)

### HEREHEREHERE

import os
import optparse
import sys
import re
from FS1Server import FS1Server, FS1ServerException


##############################################################################
# TestFS1ServerException
#
##############################################################################
class TestFS1ServerException(Exception):
    """Special exception to allow differentiated capture of exceptions"""
    def __init__(self,message,errors=None):
        super(TestFS1ServerException,self).__init__("TestFS1Server "+ message)
        self.errors = errors
    @staticmethod
    def __format__(e):
        return f" TestFS1Server: {e.__str__()}\n"
# TestFS1ServerException


##############################################################################
# TestFS1Server - Extend the FS1Server.
#
##############################################################################
class TestFS1Server(FS1Server):
    """ A test of the FS1Server class
    """
    #__slots__ = [''] # add legal instance variables
    # (setq properties `("" ""))
    def __init__(self):                               # TestFS1Server::__init__()
        """Initialize this class."""
        super().__init__()
        # (wg-python-property-variables)

    ### TestFS1Server.__init__()


    def debug(self,msg="",skip=[],os=sys.stderr):           # TestFS1Server::debug()
        """Help with momentary debugging, file to fit.
           msg  -- special tag for this call
           skip -- the member variables to ignore
           os   -- output stream: may be IOStream etc.
        """
        import pprint
        print("TestFS1Server - %s " % msg, file=os)
        for key,value in self.__dict__.items():
            if(key in skip):
               continue
            print(f'{key:20s} =',file=os,end='')
            pprint.pprint(value,stream=os,indent=4)
        return self

    ### TestFS1Server.debug()

    __TestFS1Server_debug = debug  # really preserve our debug name if we're inherited

   # (wg-python-properties properties)

# class TestFS1Server



#############################################################################
#
#  /home/git/external/FlexSpec1/Code/FlexSpec/ClientServer/Regression_FS1Server.py
#
#emacs helpers
# (insert (format "\n# %s " (buffer-file-name)))
#
# (wg-python-toc)
#
#############################################################################
__doc__ = """

FlexSpec/ClientServer/Regression_FS1Server.py
[options] files...



"""

__author__  = 'Wayne Green'
__version__ = '0.1'


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

    #if(len(args) != 0 ):
    #    for a in args:
    #        if('*' in a):
    #            import glob
    #            args.append(glob.glob(a))
    print("hello")
    try:
        server = TestFS1Server()
        server.start()
    except Exception as e:
        print(f"Exception {e.__str__()}")



