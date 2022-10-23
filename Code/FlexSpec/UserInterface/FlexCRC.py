#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# (wg-python-fix-pdbrc)
#
# (compile (format "python -m py_compile %s" (buffer-file-name)))
### HEREHEREHERE

import os
import sys
import re
import zlib
import json


#############################################################################
#
#  FlexSpec1/Code/FlexSpec/UserInterface/FlexCRC.py
#
#emacs helpers
# (insert (format "\n# %s " (buffer-file-name)))
#
#
# (wg-python-toc)
#
# __doc__ = """
# __author__  = 'Wayne Green'
# __version__ = '0.1'
# __all__     = ['FlexCRC','FlexCRCException']   # list of quoted items to export
# class FlexCRCException(Exception):
#     def __init__(self,message,errors=None):
#     @staticmethod
#     def __format__(e):
# class FlexCRC(object):
#     #__slots__ = [''] # add legal instance variables
#     def __init__(self,payload):                             # FlexCRC::__init__()
#     def add(self,charstr):                                  # FlexCRC::add()
#     def crc(self):                                          # FlexCRC::crc()
#     @staticmethod
#     def calccrc(payload : str):
#     def debug(self,msg="",skip=[],os=sys.stderr):           # FlexCRC::debug()
# if __name__ == "__main__":
#
#
#
#############################################################################
__doc__ = """

/home/git/external/FlexSpec1/Code/FlexSpec/UserInterface/FlexCRC.py
[options] files...

Tie to the CRC generation/check in the FlexSpec C++ code.

"""


__author__  = 'Wayne Green'
__version__ = '0.1'
__all__     = ['FlexCRC','FlexCRCException']   # list of quoted items to export


##############################################################################
# FlexCRCException
#
##############################################################################
class FlexCRCException(Exception):
    """Special exception to allow differentiated capture of exceptions"""
    def __init__(self,message,errors=None):
        super(FlexCRCException,self).__init__("FlexCRC "+ message)
        self.errors = errors
    @staticmethod
    def __format__(e):
        return f" FlexCRC: {e.__str__()}\n"
# FlexCRCException


##############################################################################
# FlexCRC
#
##############################################################################
class FlexCRC(object):
    """ Make a CRC for a given string.
        May call static method calccrc(str) without needing an instance.
    """

    def __init__(self,payload):                             # FlexCRC::__init__()
        """Initialize this class."""
        if(not isinstance(payload,str)):
            raise FlexCRCException("Object is not string")
        self._payload = payload
        self._rawcrc = payload.encode() # convert to bytes
        self._crc    = zlib.crc32(self._rawcrc)
        self._crcstring = ("%08X" % self._crc).encode()

    ### FlexCRC.__init__()

    def add(self,charstr):                                  # FlexCRC::add()
        """Add a character or string to the mix"""
        self._payload += charstr
        return self
    ### FlexCRC::add()

    def crc(self):                                          # FlexCRC::crc()
        """Class member, return hex string with the payload"""

        return ("%08X" % zlib.crc32(self._payload.encode())).encode()

    ### FlexCRC::crc()

    @staticmethod
    def calccrc(payload : str):
        """Make a CRC from the string without an instance"""
        return ("%08X" % zlib.crc32(payload.encode())).encode()

    def debug(self,msg="",skip=[],os=sys.stderr):           # FlexCRC::debug()
        """Help with momentary debugging, file to fit.
           msg  -- special tag for this call
           skip -- the member variables to ignore
           os   -- output stream: may be IOStream etc.
        """
        import pprint
        print("FlexCRC - %s " % msg, file=os)
        for key,value in self.__dict__.items():
            if(key in skip):
               continue
            print(f'{key:20s} =',file=os,end='')
            pprint.pprint(value,stream=os,indent=4)
        return self

    ### FlexCRC.debug()

    __FlexCRC_debug = debug  # really preserve our debug name if we're inherited

   # (wg-python-properties properties)

# class FlexCRC


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
    gen = FlexCRC("hello there")
    gen.debug()
    print(f"gen'ed crc {gen.crc()}")


