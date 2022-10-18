#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# (wg-python-fix-pdbrc)

### HEREHEREHERE

import os
import optparse
import sys
import re
import numpy as np
import pandas as pd
import json



#############################################################################
#
#  /home/git/external/FlexSpec1/Code/FlexSpec/UserInterface/FlexEEPROM.py
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
# __all__     = ['FlexEEPROMException','FlexEEPROM']   # list of quoted items to export
# class FlexEEPROMException(Exception):
#     def __init__(self,message,errors=None):
#     @staticmethod
#     def __format__(e):
# class FlexEEPROM(object):
#     #__slots__ = [''] # add legal instance variables
#     def __init__(self, pjson: str = "{}"):                  # FlexEEPROM::__init__()
#     def setdefault(self):                                   # FlexEEPROM::setdefault()
#     def parserawjson(self):                                 # FlexEEPROM::parserawjson()
#     def debug(self,msg="",skip=[],os=sys.stderr):           # FlexEEPROM::debug()
# if __name__ == "__main__":
#
#
#
#
#############################################################################
__doc__ = """

/home/git/external/FlexSpec1/Code/FlexSpec/UserInterface/FlexEEPROM.py
[options] files...



"""


__author__  = 'Wayne Green'
__version__ = '0.1'
__all__     = ['FlexEEPROMException','FlexEEPROM']   # list of quoted items to export

##############################################################################
# Example of the JSON string.
#
# { eeprom : { process : flexspec : {....devices ....} } }
# eepromdef["eeprom"]["process"]
#
# the entire def needs ~2048 bytes. 
# grating is the big one ~528 and counting. A fluffy float could kill it.
#
#
##############################################################################
eepromdef = """{
    "eeprom": {
        "process": {
            "flexspec": {
                "name"        : "FlexSpec1",
                "owner"       : "indef",
                "contact"     : "indef",
                "serialno"    : "indef",
                "coderevision": "indef",
                "installdate" : "indef",
                "updatedate"  : "indef",
                "toc": {
                    "flexspec"   : "(0    ,1024)",
                    "guidecamera": "(1024 ,1024)",
                    "slit"       : "(2048 ,1024)",
                    "fraunhofer" : "(3072 ,1024)",
                    "grating"    : "(4096 ,1024)",
                    "camera"     : "(5120 ,1024)"
                }
            },
            "guidecamera": {
                "vendor"      : "indef",
                "serialumber" : "indef",
                "pixelsize"   : "indef",
                "lens1"       : "indef",
                "lens2"       : "indef",
                "ccdsum"      : "(1,1)",
                "slotoffset"  : "indef"
            },
            "slit": {
                "vendor"      : "ovio",
                "serialno"    : "indef",
                "widthmicrons": "indef"
            },
            "fraunhofer": {
                "baffleheight": "indef",
                "bafflewidth" : "indef",
                "baffleoffset": "indef"
            },
            "grating": {
                "name"        : "Thorlabs_500_600_25_0",
                "vendor"      : "Thorlabs",
                "catalogid"   : "GR25-0605",
                "length"      : "25.0",
                "height"      : "25.0",
                "thickness"   : "6.0",
                "lmm"         : "600",
                "cwave"       : "500",
                "blaze"       : "8.617",
                "dispersion"  : "1.65",
                "tcoeff"      : "8.0",
                "home"        : "indef",
                "offset"      : "indef",
                "other"       : "indef"
            },
            "camera": {
                "vendor"      : "indef",
                "serialno"    : "indef",
                "pixelsize"   : "indef",
                "backfocus"   : "indef",
                "ccdsum"      : "(1,1)",
                "lensdesc"    : "indef",
                "lensaperture": "indef",
                "lensfl"      : "indef",
                "tempsetting" : "indef"
            }
        }
    }
}
"""

##############################################################################
# FlexEEPROMException
#
##############################################################################
class FlexEEPROMException(Exception):
    """Special exception to allow differentiated capture of exceptions"""
    def __init__(self,message,errors=None):
        super(FlexEEPROMException,self).__init__("FlexEEPROM "+ message)
        self.errors = errors
    @staticmethod
    def __format__(e):
        return f" FlexEEPROM: {e.__str__()}\n"
# FlexEEPROMException


##############################################################################
# FlexEEPROM
#
##############################################################################
class FlexEEPROM(object):
    """ Handle the EEPROM

    """
    #__slots__ = [''] # add legal instance variables
    # (setq properties `("" ""))
    # Coordinate the keys we want to use.
    eepromkeys = [ "s_camera"           ,  "s_camerasensor" , "s_collimator", 
                   "s_collimatorsensor" , "s_flexspec"      , "s_grating", 
                   "s_gratingsensor"    , "s_guider"        , "s_kzin" , "s_pangle", 
                   "s_slit"             , "s_slitsensor"
                 ]

    # The record size to allocate for each widget
    sizes =      { "s_camera"           : 1024,
                   "s_camerasensor"     : 1024,
                   "s_collimator"       : 1024,
                   "s_collimatorsensor" : 1024,
                   "s_flexspec"         : 2048,
                   "s_grating"          : 1024,
                   "s_gratingsensor"    : 1024,
                   "s_guider"           : 1024,
                   "s_kzin"             : 1024,
                   "s_pangle"           :  512,
                   "s_slit"             : 1024,
                   "s_slitsensor"       : 1024
                }

    def __init__(self, pjson: str = "{}"):                  # FlexEEPROM::__init__()
        """Initialize this class."""
        #super().__init__()
        # (wg-python-property-variables)
        self.rawjson       = pjson
        self.image         = None
        self.instrument    = {}
        self.eepromtoc     = {}
        self.devices       = {}   # 

    ### FlexEEPROM.__init__()

    def setdefault(self):                                   # FlexEEPROM::setdefault()
        """Hack to pound in eepromdef as example"""
        self.rawjson = eepromdef
        return self
    ### FlexEEPROM.setdefault()

    def parserawjson(self):                                 # FlexEEPROM::parserawjson()
        """The raw json -- see eepromdef above"""
        try:
            msg = "image";      self.image      = json.loads(self.rawjson)
            msg = "devices";    self.devices    = self.image['eeprom']['process'] # dict of all devices
            msg = "instrument"; self.instrument = self.devices['flexspec'] # is a self-device
            msg = "eepromtoc";  self.eepromtoc  = self.instrument['toc']   # all other devices
        except Exception as e:
            raise FlexEEPROMException(f"FlexEEPROM.parserawjson() - {msg} failure",e)
            
        return self
    ### FlexEEPROM.parserawjson()

    def debug(self,msg="",skip=[],os=sys.stderr):           # FlexEEPROM::debug()
        """Help with momentary debugging, file to fit.
           msg  -- special tag for this call
           skip -- the member variables to ignore
           os   -- output stream: may be IOStream etc.
        """
        import pprint
        print("FlexEEPROM - %s " % msg, file=os)
        for key,value in self.__dict__.items():
            if(key in skip):
               continue
            print(f'{key:20s} =',file=os,end='')
            pprint.pprint(value,stream=os,indent=4)
        return self

    ### FlexEEPROM.debug()

    __FlexEEPROM_debug = debug  # really preserve our debug name if we're inherited

   # (wg-python-properties properties)

   @staticmethod
   def makecpptable(os=sys.stdout)                        # FlexEEPROM.makecpptable()
      """Generate the table from these internal variables. The record block
         consists of:
         0(2)      -- the number of bytes in any record stored here. Excess is ignored.
        _2(size-2) -- the actual space to hold the blocks.
      """
      offs = 2        # skip the magic cookie
      for k,v in sizes.items():
         print(f"    {{&FlexConstants::{k:18s}   , new FlexEEPROMRecord<16>(FlexConstants::{k:18} .c_str(), {offs+v:6d}, {v:5d})}},")
         offs += v
   ### FlexEEPROM.makecpptable()

# class FlexEEPROM

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
    fstest = FlexEEPROM(eepromdef)
    fstest.setdefault().parserawjson().debug()
