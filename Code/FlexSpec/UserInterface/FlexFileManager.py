#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#############################################################################
#
#  /home/git/external/FlexSpec1/Code/FlexSpec/UserInterface/FlexFileManager.py
#
# (compile (format "python -m py_compile %s" (buffer-file-name)))
#
# 2022-10-28T07:48:27-0600 wlg
#############################################################################

import os                # TODO add some mode testing etc.
import sys

#############################################################################
#
# (wg-python-toc)
#
# __doc__ = """
# __author__  = 'Wayne Green'
# __version__ = '0.1'
# class BinaryFileManagerException(Exception):
#     def __init__(self,message,errors=None):
#     @staticmethod
#     def __format__(e):
# class BinaryFileManagerEOF(Exception):
#     def __init__(self,message,errors=None):
#     @staticmethod
#     def __format__(e):
# class BinaryFilemanager(object):
#        class provides both lookahead and infinite pushback opportunities.
#     def __init__(self,fh):                # BinaryFilemanager::__init__
#     def getch(self):                      # BinaryFilemanager::getch()
#     def peek(self):                       # BinaryFilemanager::peek()
#     def eof(self):                        # BinaryFilemanager::eof()
#     def pushback(self,ch):                # BinaryFilemanager::pushback()
# if __name__ == "__main__":
#
#############################################################################
__doc__ = """

/home/git/external/FlexSpec1/Code/FlexSpec/UserInterface/FlexFileManager.py
[options] files...

Under unit test, print out first 100 chars or less of given files.

This module provides a lookahead/pushback filemanager designed for
binary files.

"""

__author__  = 'Wayne Green'
__version__ = '0.1'
__all__     = ['BinaryFilemanager',
               'BinaryFileManagerException',
               'BinaryFileManagerEOF'
              ]   # list of quoted items to export

##############################################################################
# BinaryFileManagerException
#
##############################################################################
class BinaryFileManagerException(Exception):
    """Special exception to allow differentiated capture of exceptions"""
    def __init__(self,message,errors=None):
        super(BinaryFileManagerException,self).__init__("BinaryFileManager "+ message)
        self.errors = errors
    @staticmethod
    def __format__(e):
        return f" BinaryFileManager: {e.__str__()}\n"
# BinaryFileManagerException

##############################################################################
# BinaryFileManagerEOF -- an actual EOF condition for a file, how amazing.
#
##############################################################################
class BinaryFileManagerEOF(Exception):
    """Special exception to allow differentiated capture of exceptions"""
    def __init__(self,message,errors=None):
        super(BinaryFileManagerEOF,self).__init__("BinaryFileManager EOF"+ message)
        self.errors = errors
    @staticmethod
    def __format__(e):
        return f" BinaryFileManager EOF: {e.__str__()}\n"
# BinaryFileManagerEOF

##############################################################################
# BinaryFilemanager -- meat of the coconut. 
#
##############################################################################
class BinaryFilemanager(object):
    """class BinaryFilemanager(object)
       Given a filehandle opened 'rb', manage processing the file.  This
       class provides both lookahead and infinite pushback opportunities.
       For example while looking for <ETX> we find a <RS>; then pushback
       the <RS> and have another go later.
    """
    def __init__(self,fh):                                  # BinaryFilemanager::__init__
        self.fh     = fh                    # the file handle
        self.nextch = fh.read(1)            # may be EOF
        self.count  = 0                     # track the logical position
        self.stack  = b''                   # init to signal EOF

    ### BinaryFilemanager.()

    def getch(self):                                        # BinaryFilemanager::getch()
        ret = b''                           # be safe...
        if(len(self.stack) != 0):           # something pushed back
            print(f"stack is {len(self.stack)}")
            ret        = self.stack[0]      # get the char
            self.stack = self.stack[1:]     # manage pushback stack
            self.count += 1                 # (re) advance the logical position
        else:
            ret        = self.nextch        # OK pending next char
            if(ret == b''):                 # here is where we may hit EOF
                raise ValueError
            self.nextch = self.fh.read(1)
            self.count += 1
        return ret                          # single exit

    ### BinaryFilemanager.getch()

    def peek(self):                                         # BinaryFilemanager::peek()
        return self.nextch                   # allow look-ahead

    ### BinaryFilemanager.peek()

    def eof(self):                                          # BinaryFilemanager::eof()
        return self.nextch == b''

    ### BinaryFilemanager.eof()

    def pushback(self,ch):                                  # BinaryFilemanager::pushback()
        self.stack = ch + self.stack;        # push on to byte array
        self.count =- 1

        return self

    ### BinaryFilemanager.pushback()

# class BinaryFilemanager

##############################################################################
#                                    Main
#                               Regression Tests
##############################################################################
# HEREHEREHERE
if __name__ == "__main__":
    import optparse                       # delay use
    import sys

    opts = optparse.OptionParser(usage="%prog "+__doc__)

    opts.add_option("-v", "--verbose", action="store_true", dest="verboseflag",
                   default=False,
                   help="<bool>     be verbose about work.")

    (options, args) = opts.parse_args()

    # (wg-python-atfiles)
    for filename in args:
        try:
            with open(filename,'rb') as f:
                fm = BinaryFilemanager(f)
                while(not fm.eof() and fm.count < 10):
                    print(f"{fm.count:3d} {fm.getch()}")
                print(f"{fm.count} bytes from file {filename}")
            print(f"File {filename} complete.")
        except BinaryFileManagerEOF as eof:
            print(f"EOF found for file {filename}")
        except BinaryFileManagerException as ex:
            print(f"Exception with {filename}\n{ex.__str__()}")

