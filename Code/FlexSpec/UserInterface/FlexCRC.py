#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# (wg-astroconda3-pdb)      # CONDA Python3
# (wg-python-fix-pdbrc)
#
# (compile (format "python -m py_compile %s" (buffer-file-name)))
### HEREHEREHERE

import sys
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
#     def __init__(self,payload : str = ""):                  # FlexCRC::__init__()
#     def add(self, charstr : (str)) -> 'self':               # FlexCRC::add()
#     def crc(self,genstr=None) -> (str,bytes):                  # FlexCRC::crc()
#     def debug(self,msg="",skip=[],os=sys.stderr) -> 'FlexCRC': # FlexCRC::debug()
#     @staticmethod
#     def calccrc(payload : str) -> bytes:
# if __name__ == "__main__":
#     def traverse(i,kk,json):
#
#
#
# 2022-10-30T06:42:46-0600 wlg
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
# testjson - from the local pier15.building3.example.com, to the
#   remote sit at "Haydrians Pub" to the device "flexspec_rodda"
#   (Arduino's name) with several things to dispatch there.  the
#   receipt return path is :
#     (Nano 33)"flexspec_rodda" -> (Rpi)"Haydrians Pub" -> (Rpi)pier15.building3.example.com
##############################################################################
testjson={"pier15.building3.example.com" :
    { "Haydrians Pub":
       {"flexspec_rodda":
           { "ovioslit"    : {"process" : {"slit" : "20","illuminator" : "0","receipt" : "1"}},
             "grating"     : {"process" : {"grating" : "300l/mm","cwave" : "5000","home" : "0","receipt" : "1"}},
             "ovioslit"    : {"process" : {"slit" : "70","illuminator" : "0","receipt" : "1"}},
             "ovioslit"    : {"process" : {"slit" : "70","illuminator" : "1","receipt" : "1"}},
             "grating"     : {"process" : {"grating" : "600l/mm","cwave" : "5544","home" : "0","receipt" : "1"}},
             "guider"      : {"process" : {"position" : "0.4568","direction" : "0","speed" : "0.32","home" : "0","receipt" : "1"}},
             "guider"      : {"process" : {"position" : "0.4568","direction" : "0","speed" : "0.32","home" : "1","receipt" : "1"}},
             "guider"      : {"process" : {"position" : "0.4600","direction" : "1","speed" : "0.32","home" : "0","receipt" : "1"}},
             "collimator"  : {"process" : {"position" : "0.3390","direction" : "0","speed" : "0.1","home" : "0","receipt" : "1"}},
             "collimator"  : {"process" : {"position" : "0.3380","direction" : "0","speed" : "0.1","home" : "0","receipt" : "1"}},
             "collimator"  : {"process" : {"position" : "0.3390","direction" : "1","speed" : "0.1","home" : "0","receipt" : "1"}},
             "collimator"  : {"process" : {"position" : "0.3390","direction" : "1","speed" : "0.1","home" : "0","receipt" : "1"}},
             "camerafocus" : {"process" : {"camerafocus" : "0","receipt" : "1"}},
             "camerafocus" : {"process" : {"camerafocus" : "0","receipt" : "1"}},
             "imu"         : {"process" : {"read" : "0","home" : "1","pangle" : "59.594","receipt" : "1"}},
             "imu"         : {"process" : {"read" : "1","home" : "0","pangle" : "39.9","receipt" : "1"}},
           }
       }
    }
}

testjsonstring="""{"pier15.building3.example.com": {"Haydrians Pub": {"flexspec_rodda": {"ovioslit": {"process": {"slit": "70", "illuminator": "1", "receipt": "1"}}, "grating": {"process": {"grating": "600l/mm", "cwave": "5544", "home": "0", "receipt": "1"}}, "guider": {"process": {"position": "0.4600", "direction": "1", "speed": "0.32", "home": "0", "receipt": "1"}}, "collimator": {"process": {"position": "0.3390", "direction": "1", "speed": "0.1", "home": "0", "receipt": "1"}}, "camerafocus": {"process": {"camerafocus": "0", "receipt": "1"}}, "imu": {"process": {"read": "1", "home": "0", "pangle": "39.9", "receipt": "1"}}}}}}"""


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
# FlexCRC - Given a JSON string payload, consistent with the FlexSpec
#   protocol; compute the CRC.
##############################################################################
class FlexCRC(object):
    """ Make a CRC for a given string.
        May call static method calccrc(str) without needing an instance.
    """

    def __init__(self, payload : str = ""):                  # FlexCRC::__init__()
        """FlexCRC Usages:
           Use a transient instance to grab a CRC
              FlexCRC('{"kzing" : {"halpha" : 1}}').crc()
           Make a non-transient instance to grab a CRC but keep c as instance!
              (c := FlexCRC('{"my spec" : {"kzin" : {"halpha" : 1}}}').crc()
           Start an instance and add as we go:
              c = FlexCRC('{"my spec" : ')
              c.add('{"kzin" : {"halpha" : 1}}')
              c.add(myBokehObj.payload)
              crc = c.add('}').crc
              ...
        """
        if(not isinstance(payload,str)):
            raise FlexCRCException("Object is not string")
        self._payload         = payload
        self._payloadbytes    = None        # fill in with self.crc()
        self._crc             = None
        self._crcstring       = None
        self._crcbytes        = None
        _                     = self.crc()  # side-effect set above member vars

    ### FlexCRC.__init__()

    def add(self, charstr : (str)) -> 'self':               # FlexCRC::add()
        """Add a character or string to the mix.
        Raises TypeError if bytes are added.
        """
        self._payload += charstr

        return self

    ### FlexCRC::add()

    def crc(self,genstr=None) -> (str,bytes):                  # FlexCRC::crc()
        """Class member, return hex string with the payload.
        If genstr is provided, set the internal payload to this
        value and return its crc.

        b   = inst.crc() gets the bytes        image  bytes*8
        _,s = inst.crc() gets the string       image  8*utf-8 chars
        b,s = inst.crc() gets bytes and string images

        8 utf-8 characters, representing values of each nybble
        of an CRC32 checksum presented in Big Endian format.
        Zero padded for case len < 28 bits when that it happens.
        zlib.crc32(bytes([0])) = 3523407757 log(3523407757)/log(2) 31.7  bits
        zlib.crc32(bytes([ord('c')])) log(112844655 )/log(2) 26.75 bits
        payload = "hello neurotic world"
        crcstr = "%08X" % zlib.crc32(payload.encode())
        payload = ""
        "%08X" % zlib.crc32(payload.encode()) "00000000"
        zlib.crc32(payload.encode()) = 0

        """
        # magic mumble to make that happen. f-strings no hex!
        if(genstr is not None):
            self._payload = genstr                  # pick up with local value.
        payload               = self._payload                         # payload's string image
        self._payloadbytes    = payload.encode()                # payload's bytes image
        self._crc             = zlib.crc32(self._payloadbytes)  # its (current) crc as int
        self._crcstring       = ("%08X" % self._crc)
        self._crcbytes        = ("%08X" % self._crc).encode() # as a string

        return (self._crcbytes,self._crcstring) # bytes,_ = x.crc() does trick.

    ### FlexCRC::crc()

    def debug(self,msg="",skip=[],os=sys.stderr) -> 'FlexCRC': # FlexCRC::debug()
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

    @staticmethod
    def calccrc(payload : str) -> bytes:
        """Make a CRC from the string without an instance"""

        return ("%08X" % zlib.crc32(payload.encode())).encode()

    ### FlexCRC::calccrc() static.

# class FlexCRC

##############################################################################
#                                    Main
#                               Regression Tests
##############################################################################
# HEREHEREHERE
if __name__ == "__main__":
    import optparse
    opts = optparse.OptionParser(usage="%prog "+__doc__)

    opts.add_option("-v", "--verbose", action="store_true", dest="verboseflag",
                   default=False,
                   help="<bool>     be verbose about work.")

    (options, args) = opts.parse_args()
    import io
    import pprint

if(1):
    def traverse(i,kk,json):
        """Walk the test tree"""
        for k,v in json.items():
            #print(type(v))
            qk = k
            if(' ' in k):
                qk = f"'{k}'"
            if(isinstance(v,type({}))):
                if(kk == ''):
                    traverse(i+1,f"{qk}", v)
                else:
                    traverse(i+1,f"{kk} -> {qk}", v)
                #print(f"{i:3d} {k} = ",end='')
                #pprint.pprint(v,indent=4)
                #print()
            else:
                print(f"  {kk} {k} = {v}",end='\n')
    print("Dispatch routes for test:")
    js = json.dumps(testjson)
    print(f"testjson {testjson}")
    traverse(1,'',testjson)


    gen = FlexCRC(testjsonstring)
    gen.debug()
    bs,st = gen.crc()
    print(f"gen'ed crc bytes={bs} string={st}")

    print("\nbinary message:")
    RS  = bytes([30])
    SOH = bytes([1])
    STX = bytes([2])
    ETX = bytes([3])
    print(f"""{RS}{SOH}{bs}{STX}{testjsonstring}{ETX}""")

