#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# (wg-astroconda-pdb)
# (wg-python-fix-pdbrc)
#
#
# (compile (format "python -m py_compile %s" (buffer-file-name)))
# (compile (format "pydoc3 %s" (buffer-file-name)))
#
### HEREHEREHERE

import os
import optparse
import sys
import re
import logging

# (wg-python-types)
#############################################################################
#
#
#  /home/git/external/FlexSpec1/Code/FlexSpec/UserInterface/Flex_Log.py
# (wg-python-emacs-help)
# (wg-python-toc)
#
# __doc__ = """
# __author__  = 'Wayne Green'
# __version__ = '0.1'
# __all__     = ['Flex_Log','Flex_LogException']   # list of quoted items to export
# class Flex_LogException(Exception):
#     def __init__(self,message,errors=None):
#     @staticmethod
#     def __format__(e):
# class Flex_Log(object):
#     def __init__(self):                                      # Flex_Log::__init__()
#     def test(self):                                          # Flex_Log.test()
#     def debug(self, msg : str = "debug") -> 'self':          # Flex_Log.debug()
#     def info(self, msg : str = "debug") -> 'self':           # Flex_Log.info()
#     def warning(self, msg : str = "debug") -> 'self':        # Flex_Log.warning()
#     def error(self, msg : str = "debug") -> 'self':          # Flex_Log.error()
#     def critical(self, msg : str = "debug") -> 'self':       # Flex_Log.critical()
#     def _debug(self,msg="",skip=[],os=sys.stderr):           # Flex_Log::_debug()
#     def verbose(tf=False):                                   # Flex_Log.verbose()
# if __name__ == "__main__":
#
#
#
# 2022-11-16T05:14:54-0700 wlg
#############################################################################

__doc__ = """

/home/git/external/FlexSpec1/Code/FlexSpec/UserInterface/Flex_Log.py
[options] files...

sudo mkdir -p /var/log/flexspec1
sudo chgrp dialout /var/log/flexspec1  # or adm

In your code:
   logger = Flex_Log(verbose=True) #   or Flex_Log() verbose=False default
   logger.error(f"Oops it was my bad")
   # force one info message.
   logger.verbose(True).info('let this one into the log).verbose()


"""


__author__  = 'Wayne Green'
__version__ = '0.1'
__all__     = ['Flex_Log','Flex_LogException']   # list of quoted items to export


##############################################################################
# Flex_LogException
#
##############################################################################
class Flex_LogException(Exception):
    """Special exception to allow differentiated capture of exceptions"""
    def __init__(self,message,errors=None):
        super(Flex_LogException,self).__init__("Flex_Log "+ message)
        self.errors = errors
    @staticmethod
    def __format__(e):
        return f" Flex_Log: {e.__str__()}\n"
# Flex_LogException

##############################################################################
# Flex_Log
#
##############################################################################
class Flex_Log(object):
    """ Provide logging to main system: /var/log/flexspec_<name>
    """
    def __init__(self):                                      # Flex_Log::__init__()
        """Initialize this class."""
        # create self.logger
        logging.basicConfig(filename='/var/log/flexspec', encoding='utf-8',
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            level=logging.DEBUG,
                            verbose = False)


        self.logger  = logging.getLogger('FlexSpec1')
        self.verbose = verbose
        self.logger.setLevel(logging.DEBUG)

    ### Flex_Log.__init__()

    def test(self):                                          # Flex_Log.test()
        """Send a few test messages"""
        self.logger.debug('debug message')
        self.logger.info('info message')
        self.logger.warning('warn message')
        self.logger.error('error message')
        self.logger.critical('critical message')

        return self

    ### Flex_Log.test()

    def debug(self, msg : str = "debug") -> 'self':          # Flex_Log.debug()
        """debug log message"""
        self.logger.debug(f"FlexSpec {msg}")

        return self

    ### Flex_Log.debug()

    def info(self, msg : str = "debug") -> 'self':           # Flex_Log.info()
        """Write message if self.verbose is True.
        Allows lots of bread crumbs, but blocked in production
        """
        if(self.verbose):
            self.logger.info(f"FlexSpec {msg}")

        return self

    ### Flex_Log.info()

    def warning(self, msg : str = "debug") -> 'self':        # Flex_Log.warning()
        """Warning message"""
        self.logger.warning(f"FlexSpec {msg}")
        return self
    ### Flex_Log.warning()

    def error(self, msg : str = "debug") -> 'self':          # Flex_Log.error()
        """Error message"""
        self.logger.error(f"FlexSpec {msg}")

        return self

    ### Flex_Log.error()

    def critical(self, msg : str = "debug") -> 'self':       # Flex_Log.critical()
        """Critical message"""
        self.logger.critical(f"FlexSpec {msg}")

        return self

    ### Flex_Log.critical()

    def _debug(self,msg="",skip=[],os=sys.stderr):           # Flex_Log::_debug()
        """Help with momentary debugging, file to fit.
           msg  -- special tag for this call
           skip -- the member variables to ignore
           os   -- output stream: may be IOStream etc.
        """
        import pprint
        print("Flex_Log - %s " % msg, file=os)
        for key,value in self.__dict__.items():
            if(key in skip):
               continue
            print(f'{key:20s} =',file=os,end='')
            pprint.pprint(value,stream=os,indent=4)

        return self

    ### Flex_Log._debug()

    def verbose(tf=False):                                   # Flex_Log.verbose()
        """Set Verbose, return self"""
        if(isinstance(tf,bool)):
            self.verbose = tf
        else:
            msg = f"Flex_log.verbose() expects type bool, got {type(tf)}"
            self.critical(msg)
            raise Flex_LogException(msg);

        return self

    ###  Flex_Log.verbose()

# class Flex_Log

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
    log = Flex_Log()
    loggers = dict([("debug"    , log.debug    ),
                    ("info"     , log.info     ),
                    ("warning"  , log.warning  ),
                    ("error"    , log.error    ),
                    ("critical" , log.critical )
                   ])

    with open(filename,'r') if filename else sys.stdin as f:
        for l in f:
            if('#' in l):
                continue
            parts = l.strip().split()
            lpg = loggers.get(parts[0].strip(),log.critical)

