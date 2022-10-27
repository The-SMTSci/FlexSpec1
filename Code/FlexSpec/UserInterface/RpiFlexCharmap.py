#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  /home/wayne/play/Wayne/RpiFlexCharmap.py
#
# class RpiFlexCharmap(object):
# class RpiStateMachine:
#
#
#
#
#
# (wg-python-fix-pdbrc)
#
# (compile (format "python -m py_compile %s" (buffer-file-name)))
# (compile (format "%s" (buffer-file-name)))
### HEREHEREHERE

import os
import optparse
import sys
import re

#############################################################################
#
#  /home/wayne/play/Wayne/RpiFlexCharmap.py
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
# __doc__ = """
# __author__  = 'Wayne Green'
# __version__ = '0.1'
# __all__     = ['','']   # list of quoted items to export
# class RpiFlexCharmapException(Exception):
#     def __init__(self,message,errors=None):
#     @staticmethod
#     def __format__(e):
# class RpiFlexCharmap(object):
#     class bytes.
#     def __init__(self):                                     # RpiFlexCharmap::__init__()
#     def __get__(self,ch : bytes) -> bytes:                       # RpiFlexCharmap.__get__()
#     @staticmethod
#     def validjson(val : bytes):
#     def debug(self,msg="",skip=[],os=sys.stderr):           # RpiFlexCharmap::debug()
# class RpiFlexStateMachineException(Exception):
#     def __init__(self,message,errors=None):
#     @staticmethod
#     def __format__(e):
# class RpiStateMachine:
#     class ASCIIControl:
#     class MessageStatus:                                    # RpiStateMachine.MessageStatus
#         @staticmethod
#         def xlatestate(st : int):                           # RpiStateMachine.MessageStatus.xlatestate()
#     def __init__(self,maxcount : int = 512):
#     def reset(self):
#     def trackstate(self,newstate):                          # RpiStateMachine.trackstate()
#     def reportstate(self):                                  # RpiStateMachine.reportstate()
#     def idlestate(rawch : bytes) -> MessageStatus:
#     def getcrc(ch : bytes) ->MessageStatus:
#     def havecrc(ch : bytes) ->MessageStatus:
#     def active(ch : bytes) ->MessageStatus:
#     def full(ch : bytes) ->MessageStatus:
#     def error(ch : bytes) ->MessageStatus:
#     def validjson(self,txt : str):
# if __name__ == "__main__":
#     def _testRpiFlexCharmap():
#     def _teststatemachine():
#
#
#
#############################################################################
__doc__ = """

/home/wayne/play/Wayne/RpiFlexCharmap.py
[options] files...



"""


__author__  = 'Wayne Green'
__version__ = '0.1'
__all__     = ['RpiFlexCharmap',
               'RpiFlexCharmapException'
              ]   # list of quoted items to export


##############################################################################
# RpiFlexCharmapException
#
##############################################################################
class RpiFlexCharmapException(Exception):
    """Special exception to allow differentiated capture of exceptions"""
    def __init__(self,message,errors=None):
        super(RpiFlexCharmapException,self).__init__("RpiFlexCharmap"+ message)
        self.errors = errors
    @staticmethod
    def __format__(e):
        return f" RpiFlexCharmap: {e.__str__()}\n"
# RpiFlexCharmapException


##############################################################################
# RpiFlexCharmap
#
##############################################################################
class RpiFlexCharmap(object):
    """ A class to make sure we have legal characters, that are of python type
    class bytes.
    """
    validJSONcharsBytes = [  # OK Python really hates bytes.
          #   0              1            2            3               4            5               6             7             8              9            a             b             c            s               e            f
          bytes([0]),   bytes([0]),   bytes([0]),   bytes([0]),    bytes([0]),   bytes([0]),    bytes([0]),   bytes([0]),   bytes([0]),   bytes([0]),   bytes([0]),   bytes([0]),   bytes([0]),   bytes([0]),   bytes([0]),   bytes([0]),   # 0
          bytes([0]),   bytes([0]),   bytes([0]),   bytes([0]),    bytes([0]),   bytes([0]),    bytes([0]),   bytes([0]),   bytes([0]),   bytes([0]),   bytes([0]),   bytes([0]),   bytes([0]),   bytes([0]),   bytes([0]),   bytes([0]),   # 1
          bytes([32]),  bytes([0]),   bytes([34]),  bytes([0]),    bytes([0]),   bytes([0]),    bytes([0]),   bytes([39]),  bytes([40]),  bytes([41]),  bytes([0]),   bytes([0]),   bytes([44]),  bytes([0]),   bytes([0]),   bytes([0]),   # 2
          bytes([48]),  bytes([49]),  bytes([50]),  bytes([51]),   bytes([52]),  bytes([53]),   bytes([54]),  bytes([55]),  bytes([56]),  bytes([57]),  bytes([58]),  bytes([0]),   bytes([0]),   bytes([0]),   bytes([0]),   bytes([0]),   # 3
          bytes([0]),   bytes([65]),  bytes([66]),  bytes([67]),   bytes([68]),  bytes([69]),   bytes([70]),  bytes([71]),  bytes([72]),  bytes([73]),  bytes([74]),  bytes([75]),  bytes([76]),  bytes([77]),  bytes([78]),  bytes([79]),  # 4
          bytes([80]),  bytes([81]),  bytes([82]),  bytes([83]),   bytes([84]),  bytes([85]),   bytes([86]),  bytes([87]),  bytes([88]),  bytes([89]),  bytes([90]),  bytes([91]),  bytes([0]),   bytes([93]),  bytes([0]),   bytes([0]),   # 5
          bytes([0]),   bytes([97]),  bytes([98]),  bytes([99]),   bytes([100]), bytes([101]),  bytes([102]), bytes([103]), bytes([104]), bytes([105]), bytes([106]), bytes([107]), bytes([108]), bytes([109]), bytes([110]), bytes([111]), # 6
          bytes([112]), bytes([113]), bytes([114]), bytes([115]),  bytes([116]), bytes([117]),  bytes([118]), bytes([119]), bytes([120]), bytes([121]), bytes([122]), bytes([123]), bytes([0]),   bytes([125]), bytes([0]),   bytes([0]),   # 7
          bytes([0]),   bytes([0]),   bytes([0]),   bytes([0]),     bytes([0]),  bytes([0]),    bytes([0]),   bytes([0]),   bytes([0]),   bytes([0]),   bytes([0]),   bytes([0]),   bytes([0]),   bytes([0]),   bytes([0]),   bytes([0]),   # 8
          bytes([0]),   bytes([0]),   bytes([0]),   bytes([0]),    bytes([0]),    bytes([0]),   bytes([0]),   bytes([0]),   bytes([0]),   bytes([0]),   bytes([0]),   bytes([0]),   bytes([0]),   bytes([0]),   bytes([0]),   bytes([0]),   # 9
          bytes([0]),   bytes([0]),   bytes([0]),   bytes([0]),    bytes([0]),   bytes([0]),    bytes([0]),   bytes([0]),   bytes([0]),   bytes([0]),   bytes([0]),   bytes([0]),   bytes([0]),   bytes([0]),   bytes([0]),   bytes([0]),   # a
          bytes([0]),   bytes([0]),   bytes([0]),   bytes([0]),    bytes([0]),   bytes([0]),    bytes([0]),   bytes([0]),   bytes([0]),   bytes([0]),   bytes([0]),   bytes([0]),   bytes([0]),   bytes([0]),   bytes([0]),   bytes([0]),   # b
          bytes([0]),   bytes([0]),   bytes([0]),   bytes([0]),    bytes([0]),   bytes([0]),    bytes([0]),   bytes([0]),   bytes([0]),   bytes([0]),   bytes([0]),   bytes([0]),   bytes([0]),   bytes([0]),   bytes([0]),   bytes([0]),   # c
          bytes([0]),   bytes([0]),   bytes([0]),   bytes([0]),    bytes([0]),   bytes([0]),    bytes([0]),   bytes([0]),   bytes([0]),   bytes([0]),   bytes([0]),   bytes([0]),   bytes([0]),   bytes([0]),   bytes([0]),   bytes([0]),   # d
          bytes([0]),   bytes([0]),   bytes([0]),   bytes([0]),    bytes([0]),   bytes([0]),    bytes([0]),   bytes([0]),   bytes([0]),   bytes([0]),   bytes([0]),   bytes([0]),   bytes([0]),   bytes([0]),   bytes([0]),   bytes([0]),   # e
          bytes([0]),   bytes([0]),   bytes([0]),   bytes([0]),    bytes([0]),   bytes([0]),    bytes([0]),   bytes([0]),   bytes([0]),   bytes([0]),   bytes([0]),   bytes([0]),   bytes([0]),   bytes([0]),   bytes([0]),   bytes([0])    # f
        ]

    # iterating over bytes returns ints not bytes ch=b'3' so ch[0] is 51 character code!
    # bb = mystr.encode() bb[n] comes back as int not bytes.
    validJSONchars = [  # OK Python really hates bytes.
          # 0    1    2    3     4    5     6    7    8    9    a    b    c    s    e    f
            0,   0,   0,   0,    0,   0,    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   # 0
            0,   0,   0,   0,    0,   0,    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   # 1
           32,   0,  34,   0,    0,   0,    0,   39,  40,  41,  0,   0,  44,   0,   0,   0,   # 2
           48,  49,  50,  51,   52,  53,   54,  55,  56,  57,  58,  0,    0,   0,   0,   0,   # 3
            0,  65,  66,  67,   68,  69,   70,  71,  72,  73,  74,  75,  76,  77,  78,  79,  # 4
           80,  81,  82,  83,   84,  85,   86,  87,  88,  89,  90,  91,   0,  93,   0,   0,   # 5
            0,  97,  98,  99,  100, 101,  102, 103, 104, 105, 106, 107, 108, 109, 110, 111, # 6
          112, 113, 114, 115,  116, 117,  118, 119, 120, 121, 122, 123,   0, 125,   0,   0,   # 7
            0,   0,   0,   0,    0,   0,    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   # 8
            0,   0,   0,   0,    0,   0,    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   # 9
            0,   0,   0,   0,    0,   0,    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   # a
            0,   0,   0,   0,    0,   0,    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   # b
            0,   0,   0,   0,    0,   0,    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   # c
            0,   0,   0,   0,    0,   0,    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   # d
            0,   0,   0,   0,    0,   0,    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   # e
            0,   0,   0,   0,    0,   0,    0,   0,   0,   0,   0,   0,   0,   0,   0,   0    # f
        ]

    def __init__(self):                                     # RpiFlexCharmap::__init__()
        """Initialize this class."""
        #super().__init__()
        # (wg-python-property-variables)

    ### RpiFlexCharmap.__init__()

    def __get__(self,ch : bytes) -> bytes:                       # RpiFlexCharmap.__get__()
        """ Array operator  inst[ch]
        If ch > 0 and ch M 256 return value"""
        ret = None
        if(isinstance(ch, b'0')):
            if(len(ch) == 1):
                ret = RpiFlexCharmap.validJSONchars[ch[0]]    # return char code or zero = illegal
            else:
                raise ValueError(f"RpiFlexCharmap.__get__(): expecting single byte, got {len(ch)}")
        else:
            raise ValueError(f"RpiFlexCharmap.__get__(): param has to be of 'class bytes', found {type(ch)}")
        return ret

    #### RpiFlexCharmap.__get__()

    @staticmethod
    def validjson(val : bytes):
        """Check if the byte string is valid."""
        bads = []                  # track bad locations
        ret = False                # assume the worst
        #print(f"{val}")
        if(isinstance(val,bytes)):
            for i in range(len(val)):
                ch = val[i]
                #ch = bytes([val[i]])
                #print(f"testing {type(ch)}; {chr(ch)} {RpiFlexCharmap.validJSONchars[ch]== b'0'}")
                if( RpiFlexCharmap.validJSONchars[ch] == 0):
                    bads.append(i)
            if(len(bads) != 0):
                raise RpiFlexCharmapException(f"RpiFlexCharmap.validjson(): bad locations = {bads}")
        else:
            raise ValueError(f"RpiFlexCharmap.validjson(): param has to be of 'class bytes', found {type(ch)}")
        ret = len(bads) == 0
        return ret                               # or we exception'ed out

    ### RpiFlexCharmap.validjson()

    def debug(self,msg="",skip=[],os=sys.stderr):           # RpiFlexCharmap::debug()
        """Help with momentary debugging, file to fit.
           msg  -- special tag for this call
           skip -- the member variables to ignore
           os   -- output stream: may be IOStream etc.
        """
        import pprint
        print("RpiFlexCharmap - %s " % msg, file=os)
        for key,value in self.__dict__.items():
            if(key in skip):
               continue
            print(f'{key:20s} =',file=os,end='')
            pprint.pprint(value,stream=os,indent=4)
        return self

    ### RpiFlexCharmap.debug()

# class RpiFlexCharmap

##############################################################################
#                                    Main
#                               Regression Tests
##############################################################################
# HEREHEREHERE
if __name__ == "__main__":

    ##############################################################################
    # _testRpiFlexCharmap  - a local to here test.
    #
    ##############################################################################
    def _testRpiFlexCharmap():
        """Test the map"""
        good  =  "" # []
        bads  = 0
        for i in range(len(RpiFlexCharmap.validJSONchars)):
            ch = RpiFlexCharmap.validJSONchars[i]   # test the [] operator
            if(ch == 0):
                bads+= 1
            else:
                good += chr(ch)

        #print(f"Good chars: |{''.join(map(bytes.decode,good))}|")
        print(f"Good chars: |{good}|")
        print(f"Bad chars : {bads}")
    ### def _testRpiFlexCharmap()


    opts = optparse.OptionParser(usage="%prog "+__doc__)

    opts.add_option("-v", "--verbose", action="store_true", dest="verboseflag",
                   default=False,
                   help="<bool>     be verbose about work.")

    (options, args) = opts.parse_args()

    _testRpiFlexCharmap()
