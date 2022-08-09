#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# (wg-python-fix-pdbrc)

import os
import sys
import json

#############################################################################
#
#  SAS_NA1_3D_Spectrograph/V2-FS1Code/GratingDefinition.py
#
# GratingDefinition.py -- catalog of the Thorlabs with some synthetic information.
#
# (compile "pydoc3 ./GratingDefinition.py")
#
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

Data for Bokeh matching the Gratings available herein.

"""


__author__  = 'Wayne Green'
__version__ = '0.1'
__all__     = ['GratingDefinition','GratingDefinitionException'] # of quoted items to export


### HEREHEREHERE

##############################################################################
# GratingDefinitionException
#
##############################################################################
class GratingDefinitionException(Exception):
    """Special exception to allow differentiated capture of exceptions"""
    def __init__(self,message,errors=None):
        super(GratingDefinitionException,self).__init__("GratingDefinition "+ message)
        self.errors = errors
    @staticmethod
    def __format__(e):
        return f" GratingDefinition: {e.__str__()}\n"
# GratingDefinitionException


##############################################################################
# GratingDefinition
#
##############################################################################
class GratingDefinition(object):
    """ Manage a grating's definition. 
    """
    #__slots__ = [''] # add legal instance variables
    # (setq properties `("" ""))
    def __init__(self,pname: str, definition : dict):                               # GratingDefinition::__init__()
        """The definition is a dictionary, matched to C++ in FlexSpec code."""
        #super().__init__()
        # (wg-python-property-variables)
        self.name        = pname
        self. definition = definition
    ### GratingDefinition.__init__()


    def debug(self,msg="",skip=[],os=sys.stderr):           # GratingDefinition::debug()
        """Help with momentary debugging, file to fit.
           msg  -- special tag for this call
           skip -- the member variables to ignore
           os   -- output stream: may be IOStream etc.
        """
        import pprint
        print("GratingDefinition - %s " % msg, file=os)
        for key,value in self.definition.items():
            if(key in skip):
               continue
            print(f'{key:20s} =',file=os,end='')
            pprint.pprint(value,stream=os,indent=4)
        return self

    ### GratingDefinition.debug()

    def json(self):
        return json.dumps(self.definition)

   # (wg-python-properties properties)

# class GratingDefinition

# Data:

Thorlabs_Thorlabs_400_1200_25_0 = { "name"         : "Thorlabs_400_1200_25_0",
                                    "vendor"       : "Thorlabs",
                                    "catalogid"    : "GR25-1204",
                                    "length"       : "25.0",
                                    "height"       : "25.0",
                                    "thickness"    : "6.0",
                                    "lmm"          : "1200",
                                    "cwave"        : "400",
                                    "blaze"        : "13.883",
                                    "dispersion"   : "0.81",
                                    "tcoeff"       : "8.0",
                                  }


Thorlabs_Thorlabs_400_1200_50_0 = { "name"         : "Thorlabs_400_1200_50_0",
                                    "vendor"       : "Thorlabs",
                                    "catalogid"    : "GR50-1204",
                                    "length"       : "50.0",
                                    "height"       : "50.0",
                                    "thickness"    : "9.5",
                                    "lmm"          : "1200",
                                    "cwave"        : "400",
                                    "blaze"        : "13.883",
                                    "dispersion"   : "0.81",
                                    "tcoeff"       : "8.0",
                                  }

Thorlabs_Thorlabs_500_300_12_7 = {  "name"         : "Thorlabs_500_300_12_7",
                                    "vendor"       : "Thorlabs",
                                    "catalogid"    : "GR13-0305",
                                    "length"       : "12.7",
                                    "height"       : "12.7",
                                    "thickness"    : "6.0",
                                    "lmm"          : "300",
                                    "cwave"        : "500",
                                    "blaze"        : "4.3",
                                    "dispersion"   : "3.32",
                                    "tcoeff"       : "8.0",
                                  }

Thorlabs_Thorlabs_500_300_25_0 = {  "name"         : "Thorlabs_500_300_25_0",
                                    "vendor"       : "Thorlabs",
                                    "catalogid"    : "GR25-0305",
                                    "length"       : "25.0",
                                    "height"       : "25.0",
                                    "thickness"    : "6.0",
                                    "lmm"          : "300",
                                    "cwave"        : "500",
                                    "blaze"        : "4.3",
                                    "dispersion"   : "3.32",
                                    "tcoeff"       : "8.0",
                                  }

Thorlabs_Thorlabs_500_300_50_0 = {  "name"         : "Thorlabs_500_300_50_0",
                                    "vendor"       : "Thorlabs",
                                    "catalogid"    : "GR50-0305",
                                    "length"       : "50.0",
                                    "height"       : "50.0",
                                    "thickness"    : "9.5",
                                    "lmm"          : "300",
                                    "cwave"        : "500",
                                    "blaze"        : "4.3",
                                    "dispersion"   : "3.32",
                                    "tcoeff"       : "8.0",
                                  }

Thorlabs_Thorlabs_500_600_12_7 = {  "name"         : "Thorlabs_500_600_12_7",
                                    "vendor"       : "Thorlabs",
                                    "catalogid"    : "GR13-0605",
                                    "length"       : "12.7",
                                    "height"       : "12.7",
                                    "thickness"    : "6.0",
                                    "lmm"          : "600",
                                    "cwave"        : "500",
                                    "blaze"        : "8.617",
                                    "dispersion"   : "1.65",
                                    "tcoeff"       : "8.0",
                                  }

Thorlabs_Thorlabs_500_600_25_0 = {  "name"         : "Thorlabs_500_600_25_0",
                                    "vendor"       : "Thorlabs",
                                    "catalogid"    : "GR25-0605",
                                    "length"       : "25.0",
                                    "height"       : "25.0",
                                    "thickness"    : "6.0",
                                    "lmm"          : "600",
                                    "cwave"        : "500",
                                    "blaze"        : "8.617",
                                    "dispersion"   : "1.65",
                                    "tcoeff"       : "8.0",
                                  }

Thorlabs_Thorlabs_500_600_50_0 = {  "name"         : "Thorlabs_500_600_50_0",
                                    "vendor"       : "Thorlabs",
                                    "catalogid"    : "GR50-0605",
                                    "length"       : "50.0",
                                    "height"       : "50.0",
                                    "thickness"    : "9.5",
                                    "lmm"          : "600",
                                    "cwave"        : "500",
                                    "blaze"        : "8.617",
                                    "dispersion"   : "1.65",
                                    "tcoeff"       : "8.0",
                                  }

Thorlabs_Thorlabs_500_1200_12_7 = { "name"         : "Thorlabs_500_1200_12_7",
                                    "vendor"       : "Thorlabs",
                                    "catalogid"    : "GR13-1205",
                                    "length"       : "12.7",
                                    "height"       : "12.7",
                                    "thickness"    : "6.0",
                                    "lmm"          : "1200",
                                    "cwave"        : "500",
                                    "blaze"        : "17.45",
                                    "dispersion"   : "0.8",
                                    "tcoeff"       : "8.0",
                                  }

Thorlabs_Thorlabs_500_1200_25_0 = { "name"         : "Thorlabs_500_1200_25_0",
                                    "vendor"       : "Thorlabs",
                                    "catalogid"    : "GR25-1205",
                                    "length"       : "25.0",
                                    "height"       : "25.0",
                                    "thickness"    : "6.0",
                                    "lmm"          : "1200",
                                    "cwave"        : "500",
                                    "blaze"        : "17.45",
                                    "dispersion"   : "0.8",
                                    "tcoeff"       : "8.0",
                                  }

Thorlabs_Thorlabs_500_1200_50_0 = { "name"         : "Thorlabs_500_1200_50_0",
                                    "vendor"       : "Thorlabs",
                                    "catalogid"    : "GR50-1205",
                                    "length"       : "50.0",
                                    "height"       : "50.0",
                                    "thickness"    : "9.5",
                                    "lmm"          : "1200",
                                    "cwave"        : "500",
                                    "blaze"        : "17.45",
                                    "dispersion"   : "0.8",
                                    "tcoeff"       : "8.0",
                                  }

Thorlabs_Thorlabs_500_1800_12_7 = { "name"         : "Thorlabs_500_1800_12_7",
                                    "vendor"       : "Thorlabs",
                                    "catalogid"    : "GR13-1850",
                                    "length"       : "12.7",
                                    "height"       : "12.7",
                                    "thickness"    : "6.0",
                                    "lmm"          : "1800",
                                    "cwave"        : "500",
                                    "blaze"        : "26.733",
                                    "dispersion"   : "0.5",
                                    "tcoeff"       : "8.0",
                                  }

Thorlabs_Thorlabs_500_1800_25_0 = { "name"         : "Thorlabs_500_1800_25_0",
                                    "vendor"       : "Thorlabs",
                                    "catalogid"    : "GR25-1850",
                                    "length"       : "25.0",
                                    "height"       : "25.0",
                                    "thickness"    : "6.0",
                                    "lmm"          : "1800",
                                    "cwave"        : "500",
                                    "blaze"        : "26.733",
                                    "dispersion"   : "0.5",
                                    "tcoeff"       : "8.0",
                                  }

Thorlabs_Thorlabs_500_1800_50_0 = { "name"         : "Thorlabs_500_1800_50_0",
                                    "vendor"       : "Thorlabs",
                                    "catalogid"    : "GR50-1850",
                                    "length"       : "50.0",
                                    "height"       : "50.0",
                                    "thickness"    : "9.5",
                                    "lmm"          : "1800",
                                    "cwave"        : "500",
                                    "blaze"        : "26.733",
                                    "dispersion"   : "0.5",
                                    "tcoeff"       : "8.0",
                                  }

Thorlabs_Thorlabs_300_300_25 = {  "name"         : "Thorlabs_300_300_25",
                                  "vendor"       : "Thorlabs",
                                  "catalogid"    : "GR25-0303",
                                  "length"       : "25",
                                  "height"       : "25",
                                  "thickness"    : "6",
                                  "lmm"          : "300",
                                  "cwave"        : "300",
                                  "blaze"        : "2.567",
                                  "dispersion"   : "3.33",
                                  "tcoeff"       : "8.0",
                                  }

Thorlabs_Thorlabs_300_600_50 = {  "name"         : "Thorlabs_300_600_50",
                                  "vendor"       : "Thorlabs",
                                  "catalogid"    : "GR50-0603",
                                  "length"       : "50",
                                  "height"       : "50",
                                  "thickness"    : "9.5",
                                  "lmm"          : "600",
                                  "cwave"        : "300",
                                  "blaze"        : "5.15",
                                  "dispersion"   : "1.67",
                                  "tcoeff"       : "8.0",
                                  }

Thorlabs_Thorlabs_300_1200_12_7 = { "name"         : "Thorlabs_300_1200_12_7",
                                    "vendor"       : "Thorlabs",
                                    "catalogid"    : "GR13-1203",
                                    "length"       : "12.7",
                                    "height"       : "12.7",
                                    "thickness"    : "6",
                                    "lmm"          : "1200",
                                    "cwave"        : "300",
                                    "blaze"        : "10.367",
                                    "dispersion"   : "0.82",
                                    "tcoeff"       : "8.0",
                                  }




thorlabsmap = dict([
   ("Thorlabs_Thorlabs_400_1200_25_0" , GratingDefinition("Thorlabs_Thorlabs_400_1200_25_0" , Thorlabs_Thorlabs_400_1200_25_0  ) ), 
   ("Thorlabs_Thorlabs_400_1200_50_0" , GratingDefinition("Thorlabs_Thorlabs_400_1200_50_0" , Thorlabs_Thorlabs_400_1200_50_0  ) ), 
   ("Thorlabs_Thorlabs_500_300_12_7"  , GratingDefinition("Thorlabs_Thorlabs_500_300_12_7"  , Thorlabs_Thorlabs_500_300_12_7   ) ), 
   ("Thorlabs_Thorlabs_500_300_25_0"  , GratingDefinition("Thorlabs_Thorlabs_500_300_25_0"  , Thorlabs_Thorlabs_500_300_25_0   ) ), 
   ("Thorlabs_Thorlabs_500_300_50_0"  , GratingDefinition("Thorlabs_Thorlabs_500_300_50_0"  , Thorlabs_Thorlabs_500_300_50_0   ) ), 
   ("Thorlabs_Thorlabs_500_600_12_7"  , GratingDefinition("Thorlabs_Thorlabs_500_600_12_7"  , Thorlabs_Thorlabs_500_600_12_7   ) ), 
   ("Thorlabs_Thorlabs_500_600_25_0"  , GratingDefinition("Thorlabs_Thorlabs_500_600_25_0"  , Thorlabs_Thorlabs_500_600_25_0   ) ), 
   ("Thorlabs_Thorlabs_500_600_50_0"  , GratingDefinition("Thorlabs_Thorlabs_500_600_50_0"  , Thorlabs_Thorlabs_500_600_50_0   ) ), 
   ("Thorlabs_Thorlabs_500_1200_12_7" , GratingDefinition("Thorlabs_Thorlabs_500_1200_12_7" , Thorlabs_Thorlabs_500_1200_12_7  ) ), 
   ("Thorlabs_Thorlabs_500_1200_25_0" , GratingDefinition("Thorlabs_Thorlabs_500_1200_25_0" , Thorlabs_Thorlabs_500_1200_25_0  ) ), 
   ("Thorlabs_Thorlabs_500_1200_50_0" , GratingDefinition("Thorlabs_Thorlabs_500_1200_50_0" , Thorlabs_Thorlabs_500_1200_50_0  ) ), 
   ("Thorlabs_Thorlabs_500_1800_12_7" , GratingDefinition("Thorlabs_Thorlabs_500_1800_12_7" , Thorlabs_Thorlabs_500_1800_12_7  ) ), 
   ("Thorlabs_Thorlabs_500_1800_25_0" , GratingDefinition("Thorlabs_Thorlabs_500_1800_25_0" , Thorlabs_Thorlabs_500_1800_25_0  ) ), 
   ("Thorlabs_Thorlabs_500_1800_50_0" , GratingDefinition("Thorlabs_Thorlabs_500_1800_50_0" , Thorlabs_Thorlabs_500_1800_50_0  ) ), 
   ("Thorlabs_Thorlabs_300_300_25"    , GratingDefinition("Thorlabs_Thorlabs_300_300_25"    , Thorlabs_Thorlabs_300_300_25     ) ), 
   ("Thorlabs_Thorlabs_300_600_50"    , GratingDefinition("Thorlabs_Thorlabs_300_600_50"    , Thorlabs_Thorlabs_300_600_50     ) ), 
   ("Thorlabs_Thorlabs_300_1200_12_7" , GratingDefinition("Thorlabs_Thorlabs_300_1200_12_7" , Thorlabs_Thorlabs_300_1200_12_7  ) )  
  ])

Edmund_48_461 = {    "name"          : "600 Grooves, 12.5 x 25mm, 500nm Ruled Diffraction Grating",
                     "vendor"        : "Edmund Optics",
                     "serialno"      : "48-461",
                     "lmm"           : "600",
                     "cwave"         : "500",
                     "blaze"         : "8.62",
                     "thickness"     : "0.5",
                     "length"        : "12.5",
                     "height"        : "25",
                     "dispersion"    : "0.0",
                     "tcoeff"        : "8.0"
                }


Edmund_41_039 = {    "name"          : "1200 Grooves, 12.5 x 25mm, 250nm Ruled Diffraction Grating",
                     "vendor"        : "Edmund Optics",
                     "serialno"      : "41-039",
                     "lmm"           : "1200",
                     "cwave"         : "250",
                     "blaze"         : "8.62",
                     "thickness"     : "0.5",
                     "length"        : "12.5",
                     "height"        : "25",
                     "dispersion"    : "0.0",
                     "tcoeff"        : "8.0"
                }


Edmund_41_048 = {    "name"          : "1200 Grooves, 12.5 x 25mm, 400nm Ruled Diffraction Grating",
                     "vendor"        : "Edmund Optics",
                     "serialno"      : "41-048",
                     "lmm"           : "1200",
                     "cwave"         : "400",
                     "blaze"         : "13.88",
                     "thickness"     : "0.5",
                     "length"        : "12.5",
                     "height"        : "25",
                     "dispersion"    : "0.0",
                     "tcoeff"        : "8.0"
                }


Edmund_43_004 = {    "name"          : "1200 Grooves, 12.5 x 25mm, 500nm Ruled Diffraction Grating",
                     "vendor"        : "Edmund Optics",
                     "serialno"      : "43-004",
                     "lmm"           : "1200",
                     "cwave"         : "500",
                     "blaze"         : "17.45",
                     "thickness"     : "0.5",
                     "length"        : "12.5",
                     "height"        : "25",
                     "dispersion"    : "0.0",
                     "tcoeff"        : "8.0"
                }


Edmund_43_209 = {    "name"          : "1200 Grooves, 12.5 x 25mm, 750nm Ruled Diffraction Grating",
                     "vendor"        : "Edmund Optics",
                     "serialno"      : "43-209",
                     "lmm"           : "1200",
                     "cwave"         : "750",
                     "blaze"         : "26.73",
                     "thickness"     : "0.5",
                     "length"        : "12.5",
                     "height"        : "25",
                     "dispersion"    : "0.0",
                     "tcoeff"        : "8.0"
                }


Edmund_64_397 = {    "name"          : "150 Grooves, 12.7mm Square, 500nm Ruled Diffraction Grating",
                     "vendor"        : "Edmund Optics",
                     "serialno"      : "64-397",
                     "lmm"           : "150",
                     "cwave"         : "500",
                     "blaze"         : "2.13",
                     "thickness"     : "0.5",
                     "length"        : "12.7",
                     "height"        : "12.7",
                     "dispersion"    : "0.0",
                     "tcoeff"        : "8.0"
                }


Edmund_43_737 = {    "name"          : "300 Grooves, 12.7mm Square, 300nm Ruled Diffraction Grating",
                     "vendor"        : "Edmund Optics",
                     "serialno"      : "43-737",
                     "lmm"           : "300",
                     "cwave"         : "300",
                     "blaze"         : "2.57",
                     "thickness"     : "0.5",
                     "length"        : "12.7",
                     "height"        : "12.7",
                     "dispersion"    : "0.0",
                     "tcoeff"        : "8.0"
                }


Edmund_64_398 = {    "name"          : "300 Grooves, 12.7mm Square, 500nm Ruled Diffraction Grating",
                     "vendor"        : "Edmund Optics",
                     "serialno"      : "64-398",
                     "lmm"           : "300",
                     "cwave"         : "500",
                     "blaze"         : "4.30",
                     "thickness"     : "0.5",
                     "length"        : "12.7",
                     "height"        : "12.7",
                     "dispersion"    : "0.0",
                     "tcoeff"        : "8.0"
                }


Edmund_43_739 = {    "name"          : "600 Grooves, 12.7mm Square, 250nm Ruled Diffraction Grating",
                     "vendor"        : "Edmund Optics",
                     "serialno"      : "43-739",
                     "lmm"           : "600",
                     "cwave"         : "250",
                     "blaze"         : "4.30",
                     "thickness"     : "0.5",
                     "length"        : "12.7",
                     "height"        : "12.7",
                     "dispersion"    : "0.0",
                     "tcoeff"        : "8.0"
                }


Edmund_43_741 = {    "name"          : "600 Grooves, 12.7mm Square, 300nm Ruled Diffraction Grating",
                     "vendor"        : "Edmund Optics",
                     "serialno"      : "43-741",
                     "lmm"           : "600",
                     "cwave"         : "300",
                     "blaze"         : "5.15",
                     "thickness"     : "0.5",
                     "length"        : "12.7",
                     "height"        : "12.7",
                     "dispersion"    : "0.0",
                     "tcoeff"        : "8.0"
                }


Edmund_43_742 = {    "name"          : "600 Grooves, 12.7mm Square, 500nm Ruled Diffraction Grating",
                     "vendor"        : "Edmund Optics",
                     "serialno"      : "43-742",
                     "lmm"           : "600",
                     "cwave"         : "500",
                     "blaze"         : "8.62",
                     "thickness"     : "0.5",
                     "length"        : "12.7",
                     "height"        : "12.7",
                     "dispersion"    : "0.0",
                     "tcoeff"        : "8.0"
                }


Edmund_43_744 = {    "name"          : "600 Grooves, 12.7mm Square, 750nm Ruled Diffraction Grating",
                     "vendor"        : "Edmund Optics",
                     "serialno"      : "43-744",
                     "lmm"           : "600",
                     "cwave"         : "750",
                     "blaze"         : "13.00",
                     "thickness"     : "0.5",
                     "length"        : "12.7",
                     "height"        : "12.7",
                     "dispersion"    : "0.0",
                     "tcoeff"        : "8.0"
                }


Edmund_43_748 = {    "name"          : "600 Grooves, 12.7mm Square, 1600nm Ruled Diffraction Grating",
                     "vendor"        : "Edmund Optics",
                     "serialno"      : "43-748",
                     "lmm"           : "600",
                     "cwave"         : "1600",
                     "blaze"         : "28.68",
                     "thickness"     : "0.5",
                     "length"        : "12.7",
                     "height"        : "12.7",
                     "dispersion"    : "0.0",
                     "tcoeff"        : "8.0"
                }


Edmund_43_771 = {    "name"          : "600 Grooves, 12.7mm Square, 400nm Ruled Diffraction Grating",
                     "vendor"        : "Edmund Optics",
                     "serialno"      : "43-771",
                     "lmm"           : "600",
                     "cwave"         : "400",
                     "blaze"         : "6.88",
                     "thickness"     : "0.5",
                     "length"        : "12.7",
                     "height"        : "12.7",
                     "dispersion"    : "0.0",
                     "tcoeff"        : "8.0"
                }


Edmund_43_745 = {    "name"          : "600 Grooves, 12.7mm Square, 1000nm Ruled Diffraction Grating",
                     "vendor"        : "Edmund Optics",
                     "serialno"      : "43-745",
                     "lmm"           : "600",
                     "cwave"         : "1000",
                     "blaze"         : "17.45",
                     "thickness"     : "0.5",
                     "length"        : "12.7",
                     "height"        : "12.7",
                     "dispersion"    : "0.0",
                     "tcoeff"        : "8.0"
                }


Edmund_64_399 = {    "name"          : "900 Grooves, 12.7mm Square, 500nm Ruled Diffraction Grating",
                     "vendor"        : "Edmund Optics",
                     "serialno"      : "64-399",
                     "lmm"           : "900",
                     "cwave"         : "500",
                     "blaze"         : "13.00",
                     "thickness"     : "0.5",
                     "length"        : "12.7",
                     "height"        : "12.7",
                     "dispersion"    : "0.0",
                     "tcoeff"        : "8.0"
                }


Edmund_43_750 = {    "name"          : "1200 Grooves, 12.7mm Square, 250nm Ruled Diffraction Grating",
                     "vendor"        : "Edmund Optics",
                     "serialno"      : "43-750",
                     "lmm"           : "1200",
                     "cwave"         : "250",
                     "blaze"         : "8.62",
                     "thickness"     : "0.5",
                     "length"        : "12.7",
                     "height"        : "12.7",
                     "dispersion"    : "0.0",
                     "tcoeff"        : "8.0"
                }


Edmund_48_464 = {    "name"          : "1200 Grooves, 12.7mm Square, 400nm Ruled Diffraction Grating",
                     "vendor"        : "Edmund Optics",
                     "serialno"      : "48-464",
                     "lmm"           : "1200",
                     "cwave"         : "400",
                     "blaze"         : "13.88",
                     "thickness"     : "0.5",
                     "length"        : "12.7",
                     "height"        : "12.7",
                     "dispersion"    : "0.0",
                     "tcoeff"        : "8.0"
                }


Edmund_43_751 = {    "name"          : "1200 Grooves, 12.7mm Square, 500nm Ruled Diffraction Grating",
                     "vendor"        : "Edmund Optics",
                     "serialno"      : "43-751",
                     "lmm"           : "1200",
                     "cwave"         : "500",
                     "blaze"         : "17.45",
                     "thickness"     : "0.5",
                     "length"        : "12.7",
                     "height"        : "12.7",
                     "dispersion"    : "0.0",
                     "tcoeff"        : "8.0"
                }


Edmund_43_752 = {    "name"          : "1200 Grooves, 12.7mm Square, 750nm Ruled Diffraction Grating",
                     "vendor"        : "Edmund Optics",
                     "serialno"      : "43-752",
                     "lmm"           : "1200",
                     "cwave"         : "750",
                     "blaze"         : "26.73",
                     "thickness"     : "0.5",
                     "length"        : "12.7",
                     "height"        : "12.7",
                     "dispersion"    : "0.0",
                     "tcoeff"        : "8.0"
                }


Edmund_43_753 = {    "name"          : "1200 Grooves, 12.7mm Square, 1000nm Ruled Diffraction Grating",
                     "vendor"        : "Edmund Optics",
                     "serialno"      : "43-753",
                     "lmm"           : "1200",
                     "cwave"         : "1000",
                     "blaze"         : "36.87",
                     "thickness"     : "0.5",
                     "length"        : "12.7",
                     "height"        : "12.7",
                     "dispersion"    : "0.0",
                     "tcoeff"        : "8.0"
                }


Edmund_64_400 = {    "name"          : "1800 Grooves, 12.7mm Square, 240nm Ruled Diffraction Grating",
                     "vendor"        : "Edmund Optics",
                     "serialno"      : "64-400",
                     "lmm"           : "1800",
                     "cwave"         : "240",
                     "blaze"         : "12.48",
                     "thickness"     : "0.5",
                     "length"        : "12.7",
                     "height"        : "12.7",
                     "dispersion"    : "0.0",
                     "tcoeff"        : "8.0"
                }


Edmund_64_402 = {    "name"          : "150 Grooves, 25mm Square, 500nm Ruled Diffraction Grating",
                     "vendor"        : "Edmund Optics",
                     "serialno"      : "64-402",
                     "lmm"           : "150",
                     "cwave"         : "500",
                     "blaze"         : "2.13",
                     "thickness"     : "0.5",
                     "length"        : "25",
                     "height"        : "25",
                     "dispersion"    : "0.0",
                     "tcoeff"        : "8.0"
                }


Edmund_64_403 = {    "name"          : "300 Grooves, 25mm Square, 500nm Ruled Diffraction Grating",
                     "vendor"        : "Edmund Optics",
                     "serialno"      : "64-403",
                     "lmm"           : "300",
                     "cwave"         : "500",
                     "blaze"         : "4.30",
                     "thickness"     : "0.5",
                     "length"        : "25",
                     "height"        : "25",
                     "dispersion"    : "0.0",
                     "tcoeff"        : "8.0"
                }


Edmund_43_740 = {    "name"          : "600 Grooves, 25mm Square, 250nm Ruled Diffraction Grating",
                     "vendor"        : "Edmund Optics",
                     "serialno"      : "43-740",
                     "lmm"           : "600",
                     "cwave"         : "250",
                     "blaze"         : "4.30",
                     "thickness"     : "0.5",
                     "length"        : "25",
                     "height"        : "25",
                     "dispersion"    : "0.0",
                     "tcoeff"        : "8.0"
                }


Edmund_43_001 = {    "name"          : "600 Grooves, 25mm Square, 300nm Ruled Diffraction Grating",
                     "vendor"        : "Edmund Optics",
                     "serialno"      : "43-001",
                     "lmm"           : "600",
                     "cwave"         : "300",
                     "blaze"         : "5.15",
                     "thickness"     : "0.5",
                     "length"        : "25",
                     "height"        : "25",
                     "dispersion"    : "0.0",
                     "tcoeff"        : "8.0"
                }


Edmund_43_743 = {    "name"          : "600 Grooves, 25mm Square, 500nm Ruled Diffraction Grating",
                     "vendor"        : "Edmund Optics",
                     "serialno"      : "43-743",
                     "lmm"           : "600",
                     "cwave"         : "500",
                     "blaze"         : "8.62",
                     "thickness"     : "0.5",
                     "length"        : "25",
                     "height"        : "25",
                     "dispersion"    : "0.0",
                     "tcoeff"        : "8.0"
                }


Edmund_41_028 = {    "name"          : "600 Grooves, 25mm Square, 750nm Ruled Diffraction Grating",
                     "vendor"        : "Edmund Optics",
                     "serialno"      : "41-028",
                     "lmm"           : "600",
                     "cwave"         : "750",
                     "blaze"         : "13.00",
                     "thickness"     : "0.5",
                     "length"        : "25",
                     "height"        : "25",
                     "dispersion"    : "0.0",
                     "tcoeff"        : "8.0"
                }


Edmund_43_207 = {    "name"          : "600 Grooves, 25mm Square, 1000nm Ruled Diffraction Grating",
                     "vendor"        : "Edmund Optics",
                     "serialno"      : "43-207",
                     "lmm"           : "600",
                     "cwave"         : "1000",
                     "blaze"         : "17.45",
                     "thickness"     : "0.5",
                     "length"        : "25",
                     "height"        : "25",
                     "dispersion"    : "0.0",
                     "tcoeff"        : "8.0"
                }


Edmund_43_747 = {    "name"          : "600 Grooves, 25mm Square, 1250nm Ruled Diffraction Grating",
                     "vendor"        : "Edmund Optics",
                     "serialno"      : "43-747",
                     "lmm"           : "600",
                     "cwave"         : "1250",
                     "blaze"         : "22.02",
                     "thickness"     : "0.5",
                     "length"        : "25",
                     "height"        : "25",
                     "dispersion"    : "0.0",
                     "tcoeff"        : "8.0"
                }


Edmund_43_749 = {    "name"          : "600 Grooves, 25mm Square, 1600nm Ruled Diffraction Grating",
                     "vendor"         : "Edmund Optics",
                     "serialno"       : "43-749",
                     "lmm"            : "600",
                     "cwave"          : "1600",
                     "blaze"          : "28.68",
                     "thickness"      : "0.5",
                     "length"         : "25",
                     "height"         : "25",
                     "dispersion"     : "0.0",
                     "tcoeff"         : "8.0"
                }


Edmund_64_404 = {    "name"          : "900 Grooves, 25mm Square, 500nm Ruled Diffraction Grating",
                     "vendor"         : "Edmund Optics",
                     "serialno"       : "64-404",
                     "lmm"            : "900",
                     "cwave"          : "500",
                     "blaze"          : "13.00",
                     "thickness"      : "0.5",
                     "length"         : "25",
                     "height"         : "25",
                     "dispersion"     : "0.0",
                     "tcoeff"         : "8.0"
                }


Edmund_41_037 = {    "name"          : "1200 Grooves, 25mm Square, 250nm Ruled Diffraction Grating",
                     "vendor"         : "Edmund Optics",
                     "serialno"       : "41-037",
                     "lmm"            : "1200",
                     "cwave"          : "250",
                     "blaze"          : "8.62",
                     "thickness"      : "0.5",
                     "length"         : "25",
                     "height"         : "25",
                     "dispersion"     : "0.0",
                     "tcoeff"         : "8.0"
                }


Edmund_41_046 = {    "name"          : "1200 Grooves, 25mm Square, 400nm Ruled Diffraction Grating",
                     "vendor"         : "Edmund Optics",
                     "serialno"       : "41-046",
                     "lmm"            : "1200",
                     "cwave"          : "400",
                     "blaze"          : "13.88",
                     "thickness"      : "0.5",
                     "length"         : "25",
                     "height"         : "25",
                     "dispersion"     : "0.0",
                     "tcoeff"         : "8.0"
                }


Edmund_43_005 = {    "name"          : "1200 Grooves, 25mm Square, 500nm Ruled Diffraction Grating",
                     "vendor"         : "Edmund Optics",
                     "serialno"       : "43-005",
                     "lmm"            : "1200",
                     "cwave"          : "500",
                     "blaze"          : "17.45",
                     "thickness"      : "0.5",
                     "length"         : "25",
                     "height"         : "25",
                     "dispersion"     : "0.0",
                     "tcoeff"         : "8.0"
                }


Edmund_43_210 = {    "name"          : "1200 Grooves, 25mm Square, 750nm Ruled Diffraction Grating",
                     "vendor"         : "Edmund Optics",
                     "serialno"       : "43-210",
                     "lmm"            : "1200",
                     "cwave"          : "750",
                     "blaze"          : "26.73",
                     "thickness"      : "0.5",
                     "length"         : "25",
                     "height"         : "25",
                     "dispersion"     : "0.0",
                     "tcoeff"         : "8.0"
                }


Edmund_43_754 = {    "name"          : "1200 Grooves, 25mm Square, 1000nm Ruled Diffraction Grating",
                     "vendor"         : "Edmund Optics",
                     "serialno"       : "43-754",
                     "lmm"            : "1200",
                     "cwave"          : "1000",
                     "blaze"          : "36.87",
                     "thickness"      : "0.5",
                     "length"         : "25",
                     "height"         : "25",
                     "dispersion"     : "0.0",
                     "tcoeff"         : "8.0"
                }


Edmund_48_460 = {    "name"          : "600 Grooves, 30mm Square, 400nm Ruled Diffraction Grating",
                     "vendor"        : "Edmund Optics",
                     "serialno"      : "48-460",
                     "lmm"           : "600",
                     "cwave"         : "400",
                     "blaze"         : "6.88",
                     "thickness"     : "0.5",
                     "length"        : "30",
                     "height"        : "30",
                     "dispersion"    : "0.0",
                     "tcoeff"        : "8.0"
                }


Edmund_46_075 = {    "name"          : "600 Grooves, 30mm Square, 500nm Ruled Diffraction Grating",
                     "vendor"        : "Edmund Optics",
                     "serialno"      : "46-075",
                     "lmm"           : "600",
                     "cwave"         : "500",
                     "blaze"         : "8.62",
                     "thickness"     : "0.5",
                     "length"        : "30",
                     "height"        : "30",
                     "dispersion"    : "0.0",
                     "tcoeff"        : "8.0"
                }


Edmund_55_258 = {    "name"          : "600 Grooves, 30mm Square, 750nm Ruled Diffraction Grating",
                     "vendor"        : "Edmund Optics",
                     "serialno"      : "55-258",
                     "lmm"           : "600",
                     "cwave"         : "750",
                     "blaze"         : "13.00",
                     "thickness"     : "0.5",
                     "length"        : "30",
                     "height"        : "30",
                     "dispersion"    : "0.0",
                     "tcoeff"        : "8.0"
                }


Edmund_46_076 = {    "name"          : "600 Grooves, 30mm Square, 1250nm Ruled Diffraction Grating",
                     "vendor"        : "Edmund Optics",
                     "serialno"      : "46-076",
                     "lmm"           : "600",
                     "cwave"         : "1250",
                     "blaze"         : "22.02",
                     "thickness"     : "0.5",
                     "length"        : "30",
                     "height"        : "30",
                     "dispersion"    : "0.0",
                     "tcoeff"        : "8.0"
                }


Edmund_55_259 = {    "name"          : "600 Grooves, 30mm Square, 1600nm Ruled Diffraction Grating",
                     "vendor"        : "Edmund Optics",
                     "serialno"      : "55-259",
                     "lmm"           : "600",
                     "cwave"         : "1600",
                     "blaze"         : "28.68",
                     "thickness"     : "0.5",
                     "length"        : "30",
                     "height"        : "30",
                     "dispersion"    : "0.0",
                     "tcoeff"        : "8.0"
                }


Edmund_55_260 = {    "name"          : "1200 Grooves, 30mm Square, 250nm Ruled Diffraction Grating",
                     "vendor"        : "Edmund Optics",
                     "serialno"      : "55-260",
                     "lmm"           : "1200",
                     "cwave"         : "250",
                     "blaze"         : "8.62",
                     "thickness"     : "0.5",
                     "length"        : "30",
                     "height"        : "30",
                     "dispersion"    : "0.0",
                     "tcoeff"        : "8.0"
                }


Edmund_46_077 = {    "name"          : "1200 Grooves, 30mm Square, 500nm Ruled Diffraction Grating",
                     "vendor"        : "Edmund Optics",
                     "serialno"      : "46-077",
                     "lmm"           : "1200",
                     "cwave"         : "500",
                     "blaze"         : "17.45",
                     "thickness"     : "0.5",
                     "length"        : "30",
                     "height"        : "30",
                     "dispersion"    : "0.0",
                     "tcoeff"        : "8.0"
                }


Edmund_46_078 = {    "name"          : "1200 Grooves, 30mm Square, 750nm Ruled Diffraction Grating",
                     "vendor"        : "Edmund Optics",
                     "serialno"      : "46-078",
                     "lmm"           : "1200",
                     "cwave"         : "750",
                     "blaze"         : "26.73",
                     "thickness"     : "0.5",
                     "length"        : "30",
                     "height"        : "30",
                     "dispersion"    : "0.0",
                     "tcoeff"        : "8.0"
                }


Edmund_48_459 = {    "name"          : "300 Grooves, 50mm Square, 300nm Ruled Diffraction Grating",
                     "vendor"        : "Edmund Optics",
                     "serialno"      : "48-459",
                     "lmm"           : "300",
                     "cwave"         : "300",
                     "blaze"         : "2.57",
                     "thickness"     : "0.5",
                     "length"        : "50",
                     "height"        : "50",
                     "dispersion"    : "0.0",
                     "tcoeff"        : "8.0"
                }


Edmund_41_021 = {    "name"          : "600 Grooves, 12.5 x 25mm, 400nm Ruled Diffraction Grating",
                     "vendor"        : "Edmund Optics",
                     "serialno"      : "41-021",
                     "lmm"           : "600",
                     "cwave"         : "400",
                     "blaze"         : "6.88",
                     "thickness"     : "0.5",
                     "length"        : "12.5",
                     "height"        : "25",
                     "dispersion"    : "0.0",
                     "tcoeff"        : "8.0"
                }


Edmund_41_020 = {    "name"          : "600 Grooves, 12.5 x 25mm, 750nm Ruled Diffraction Grating",
                     "vendor"        : "Edmund Optics",
                     "serialno"      : "41-020",
                     "lmm"           : "600",
                     "cwave"         : "750",
                     "blaze"         : "13.00",
                     "thickness"     : "0.5",
                     "length"        : "12.5",
                     "height"        : "25",
                     "dispersion"    : "0.0",
                     "tcoeff"        : "8.0"
                }


Edmund_43_746 = {    "name"          : "600 Grooves, 12.7mm Square, 1250nm Ruled Diffraction Grating",
                     "vendor"        : "Edmund Optics",
                     "serialno"      : "43-746",
                     "lmm"           : "600",
                     "cwave"         : "1250",
                     "blaze"         : "22.02",
                     "thickness"     : "0.5",
                     "length"        : "12.7",
                     "height"        : "12.7",
                     "dispersion"    : "0.0",
                     "tcoeff"        : "8.0"
                }


Edmund_43_738 = {    "name"          : "300 Grooves, 25mm Square, 300nm Ruled Diffraction Grating",
                     "vendor"        : "Edmund Optics",
                     "serialno"      : "43-738",
                     "lmm"           : "300",
                     "cwave"         : "300",
                     "blaze"         : "2.57",
                     "thickness"     : "0.5",
                     "length"        : "25",
                     "height"        : "25",
                     "dispersion"    : "0.0",
                     "tcoeff"        : "8.0"
                }


Edmund_41_019 = {    "name"          : "600 Grooves, 25mm Square, 400nm Ruled Diffraction Grating",
                     "vendor"        : "Edmund Optics",
                     "serialno"      : "41-019",
                     "lmm"           : "600",
                     "cwave"         : "400",
                     "blaze"         : "6.88",
                     "thickness"     : "0.5",
                     "length"        : "25",
                     "height"        : "25",
                     "dispersion"    : "0.0",
                     "tcoeff"        : "8.0"
                }


Edmund_64_405 = {    "name"          : "1800 Grooves, 25mm Square, 240nm Ruled Diffraction Grating",
                     "vendor"        : "Edmund Optics",
                     "serialno"      : "64-405",
                     "lmm"           : "1800",
                     "cwave"         : "240",
                     "blaze"         : "12.48",
                     "thickness"     : "0.5",
                     "length"        : "25",
                     "height"        : "25",
                     "dispersion"    : "0.0",
                     "tcoeff"        : "8.0"
                }


Edmund_43_002 = {    "name"          : "600 Grooves, 50mm Square, 300nm Ruled Diffraction Grating",
                     "vendor"        : "Edmund Optics",
                     "serialno"      : "43-002",
                     "lmm"           : "600",
                     "cwave"         : "300",
                     "blaze"         : "5.15",
                     "thickness"     : "0.5",
                     "length"        : "50",
                     "height"        : "50",
                     "dispersion"    : "0.0",
                     "tcoeff"        : "8.0"
                }


Edmund_41_016 = {    "name"          : "600 Grooves, 50mm Square, 400nm Ruled Diffraction Grating",
                     "vendor"        : "Edmund Optics",
                     "serialno"      : "41-016",
                     "lmm"           : "600",
                     "cwave"         : "400",
                     "blaze"         : "6.88",
                     "thickness"     : "0.5",
                     "length"        : "50",
                     "height"        : "50",
                     "dispersion"    : "0.0",
                     "tcoeff"        : "8.0"
                }


Edmund_48_462 = {    "name"          : "600 Grooves, 50mm Square, 500nm Ruled Diffraction Grating",
                     "vendor"        : "Edmund Optics",
                     "serialno"      : "48-462",
                     "lmm"           : "600",
                     "cwave"         : "500",
                     "blaze"         : "8.62",
                     "thickness"     : "0.5",
                     "length"        : "50",
                     "height"        : "50",
                     "dispersion"    : "0.0",
                     "tcoeff"        : "8.0"
                }


Edmund_41_025 = {    "name"          : "600 Grooves, 50mm Square, 750nm Ruled Diffraction Grating",
                     "vendor"        : "Edmund Optics",
                     "serialno"      : "41-025",
                     "lmm"           : "600",
                     "cwave"         : "750",
                     "blaze"         : "13.00",
                     "thickness"     : "0.5",
                     "length"        : "50",
                     "height"        : "50",
                     "dispersion"    : "0.0",
                     "tcoeff"        : "8.0"
                }


Edmund_43_208 = {    "name"          : "600 Grooves, 50mm Square, 1000nm Ruled Diffraction Grating",
                     "vendor"        : "Edmund Optics",
                     "serialno"      : "43-208",
                     "lmm"           : "600",
                     "cwave"         : "1000",
                     "blaze"         : "17.45",
                     "thickness"     : "0.5",
                     "length"        : "50",
                     "height"        : "50",
                     "dispersion"    : "0.0",
                     "tcoeff"        : "8.0"
                }


Edmund_48_463 = {    "name"          : "600 Grooves, 50mm Square, 1250nm Ruled Diffraction Grating",
                     "vendor"        : "Edmund Optics",
                     "serialno"      : "48-463",
                     "lmm"           : "600",
                     "cwave"         : "1250",
                     "blaze"         : "22.02",
                     "thickness"     : "0.5",
                     "length"        : "50",
                     "height"        : "50",
                     "dispersion"    : "0.0",
                     "tcoeff"        : "8.0"
                }

Edmund_41_034 = {    "name"          : "1200 Grooves, 50mm Square, 250nm Ruled Diffraction Grating",
                     "vendor"        : "Edmund Optics",
                     "serialno"      : "41-034",
                     "lmm"           : "1200",
                     "cwave"         : "250",
                     "blaze"         : "8.62",
                     "thickness"     : "0.5",
                     "length"        : "50",
                     "height"        : "50",
                     "dispersion"    : "0.0",
                     "tcoeff"        : "8.0"
                }


Edmund_41_043 = {    "name"          : "1200 Grooves, 50mm Square, 400nm Ruled Diffraction Grating",
                     "vendor"        : "Edmund Optics",
                     "serialno"      : "41-043",
                     "lmm"           : "1200",
                     "cwave"         : "400",
                     "blaze"         : "13.88",
                     "thickness"     : "0.5",
                     "length"        : "50",
                     "height"        : "50",
                     "dispersion"    : "0.0",
                     "tcoeff"        : "8.0"
                }


Edmund_43_006 = {    "name"          : "1200 Grooves, 50mm Square, 500nm Ruled Diffraction Grating",
                     "vendor"        : "Edmund Optics",
                     "serialno"      : "43-006",
                     "lmm"           : "1200",
                     "cwave"         : "500",
                     "blaze"         : "17.45",
                     "thickness"     : "0.5",
                     "length"        : "50",
                     "height"        : "50",
                     "dispersion"    : "0.0",
                     "tcoeff"        : "8.0"
                }


Edmund_43_211 = { "name"             : "1200 Grooves, 50mm Square, 750nm Ruled Diffraction Grating",
                     "vendor"        : "Edmund Optics",
                     "serialno"      : "43-211",
                     "lmm"           : "1200",
                     "cwave"         : "750",
                     "blaze"         : "26.73",
                     "thickness"     : "0.5",
                     "length"        : "50",
                     "height"        : "50",
                     "dispersion"    : "0.0",
                     "tcoeff"        : "8.0"
                }

edmundmap = dict([
   ("Edmund_48_461" ,GratingDefinition("Edmund_48_461" , Edmund_48_461 ) ),
   ("Edmund_41_039" ,GratingDefinition("Edmund_41_039" , Edmund_41_039 ) ),
   ("Edmund_41_048" ,GratingDefinition("Edmund_41_048" , Edmund_41_048 ) ),
   ("Edmund_43_004" ,GratingDefinition("Edmund_43_004" , Edmund_43_004 ) ),
   ("Edmund_43_209" ,GratingDefinition("Edmund_43_209" , Edmund_43_209 ) ),
   ("Edmund_64_397" ,GratingDefinition("Edmund_64_397" , Edmund_64_397 ) ),
   ("Edmund_43_737" ,GratingDefinition("Edmund_43_737" , Edmund_43_737 ) ),
   ("Edmund_64_398" ,GratingDefinition("Edmund_64_398" , Edmund_64_398 ) ),
   ("Edmund_43_739" ,GratingDefinition("Edmund_43_739" , Edmund_43_739 ) ),
   ("Edmund_43_741" ,GratingDefinition("Edmund_43_741" , Edmund_43_741 ) ),
   ("Edmund_43_742" ,GratingDefinition("Edmund_43_742" , Edmund_43_742 ) ),
   ("Edmund_43_744" ,GratingDefinition("Edmund_43_744" , Edmund_43_744 ) ),
   ("Edmund_43_748" ,GratingDefinition("Edmund_43_748" , Edmund_43_748 ) ),
   ("Edmund_43_771" ,GratingDefinition("Edmund_43_771" , Edmund_43_771 ) ),
   ("Edmund_43_745" ,GratingDefinition("Edmund_43_745" , Edmund_43_745 ) ),
   ("Edmund_64_399" ,GratingDefinition("Edmund_64_399" , Edmund_64_399 ) ),
   ("Edmund_43_750" ,GratingDefinition("Edmund_43_750" , Edmund_43_750 ) ),
   ("Edmund_48_464" ,GratingDefinition("Edmund_48_464" , Edmund_48_464 ) ),
   ("Edmund_43_751" ,GratingDefinition("Edmund_43_751" , Edmund_43_751 ) ),
   ("Edmund_43_752" ,GratingDefinition("Edmund_43_752" , Edmund_43_752 ) ),
   ("Edmund_43_753" ,GratingDefinition("Edmund_43_753" , Edmund_43_753 ) ),
   ("Edmund_64_400" ,GratingDefinition("Edmund_64_400" , Edmund_64_400 ) ),
   ("Edmund_64_402" ,GratingDefinition("Edmund_64_402" , Edmund_64_402 ) ),
   ("Edmund_64_403" ,GratingDefinition("Edmund_64_403" , Edmund_64_403 ) ),
   ("Edmund_43_740" ,GratingDefinition("Edmund_43_740" , Edmund_43_740 ) ),
   ("Edmund_43_001" ,GratingDefinition("Edmund_43_001" , Edmund_43_001 ) ),
   ("Edmund_43_743" ,GratingDefinition("Edmund_43_743" , Edmund_43_743 ) ),
   ("Edmund_41_028" ,GratingDefinition("Edmund_41_028" , Edmund_41_028 ) ),
   ("Edmund_43_207" ,GratingDefinition("Edmund_43_207" , Edmund_43_207 ) ),
   ("Edmund_43_747" ,GratingDefinition("Edmund_43_747" , Edmund_43_747 ) ),
   ("Edmund_43_749" ,GratingDefinition("Edmund_43_749" , Edmund_43_749 ) ),
   ("Edmund_64_404" ,GratingDefinition("Edmund_64_404" , Edmund_64_404 ) ),
   ("Edmund_41_037" ,GratingDefinition("Edmund_41_037" , Edmund_41_037 ) ),
   ("Edmund_41_046" ,GratingDefinition("Edmund_41_046" , Edmund_41_046 ) ),
   ("Edmund_43_005" ,GratingDefinition("Edmund_43_005" , Edmund_43_005 ) ),
   ("Edmund_43_210" ,GratingDefinition("Edmund_43_210" , Edmund_43_210 ) ),
   ("Edmund_43_754" ,GratingDefinition("Edmund_43_754" , Edmund_43_754 ) ),
   ("Edmund_48_460" ,GratingDefinition("Edmund_48_460" , Edmund_48_460 ) ),
   ("Edmund_46_075" ,GratingDefinition("Edmund_46_075" , Edmund_46_075 ) ),
   ("Edmund_55_258" ,GratingDefinition("Edmund_55_258" , Edmund_55_258 ) ),
   ("Edmund_46_076" ,GratingDefinition("Edmund_46_076" , Edmund_46_076 ) ),
   ("Edmund_55_259" ,GratingDefinition("Edmund_55_259" , Edmund_55_259 ) ),
   ("Edmund_55_260" ,GratingDefinition("Edmund_55_260" , Edmund_55_260 ) ),
   ("Edmund_46_077" ,GratingDefinition("Edmund_46_077" , Edmund_46_077 ) ),
   ("Edmund_46_078" ,GratingDefinition("Edmund_46_078" , Edmund_46_078 ) ),
   ("Edmund_48_459" ,GratingDefinition("Edmund_48_459" , Edmund_48_459 ) ),
   ("Edmund_41_021" ,GratingDefinition("Edmund_41_021" , Edmund_41_021 ) ),
   ("Edmund_41_020" ,GratingDefinition("Edmund_41_020" , Edmund_41_020 ) ),
   ("Edmund_43_746" ,GratingDefinition("Edmund_43_746" , Edmund_43_746 ) ),
   ("Edmund_43_738" ,GratingDefinition("Edmund_43_738" , Edmund_43_738 ) ),
   ("Edmund_41_019" ,GratingDefinition("Edmund_41_019" , Edmund_41_019 ) ),
   ("Edmund_64_405" ,GratingDefinition("Edmund_64_405" , Edmund_64_405 ) ),
   ("Edmund_43_002" ,GratingDefinition("Edmund_43_002" , Edmund_43_002 ) ),
   ("Edmund_41_016" ,GratingDefinition("Edmund_41_016" , Edmund_41_016 ) ),
   ("Edmund_48_462" ,GratingDefinition("Edmund_48_462" , Edmund_48_462 ) ),
   ("Edmund_41_025" ,GratingDefinition("Edmund_41_025" , Edmund_41_025 ) ),
   ("Edmund_43_208" ,GratingDefinition("Edmund_43_208" , Edmund_43_208 ) ),
   ("Edmund_48_463" ,GratingDefinition("Edmund_48_463" , Edmund_48_463 ) ),
   ("Edmund_41_034" ,GratingDefinition("Edmund_41_034" , Edmund_41_034 ) ),
   ("Edmund_41_043" ,GratingDefinition("Edmund_41_043" , Edmund_41_043 ) ),
   ("Edmund_43_006" ,GratingDefinition("Edmund_43_006" , Edmund_43_006 ) ),
   ("Edmund_43_211" ,GratingDefinition("Edmund_43_211" , Edmund_43_211 ) )
]) # edmundmap


##############################################################################
#                                    Main
#                               Regression Tests
##############################################################################
# HEREHEREHERE
import optparse

if __name__ == "__main__":
    opts = optparse.OptionParser(usage="%prog "+__doc__)

    opts.add_option("-v", "--verbose", action="store_true", dest="verboseflag",
                   default=False,
                   help="<bool>     be verbose about work.")

    (options, args) = opts.parse_args()
    print("List of Thorlabs names")
    for k,v in thorlabsmap.items():
        print(v.json())
        #print(str.strip(f'''"{k}"''')) # , v.debug()

    print("\n\nList of Edmund names")
    for k,v in edmundmap.items():
        print(v.json())
        #print(str.strip(f'''"{k}"''')) # , v.debug()
