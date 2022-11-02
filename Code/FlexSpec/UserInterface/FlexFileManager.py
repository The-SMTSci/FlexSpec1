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
# __all__     = ['BinaryFilemanager',
# class BinaryFileManagerException(Exception):
#     def __init__(self,message,errors=None):
#     @staticmethod
#     def __format__(e):
# class BinaryFileManagerEOF(Exception):
#     def __init__(self,message,errors=None):
#     @staticmethod
#     def __format__(e):
# class BinaryFilemanager(object):
#     def __init__(self,fh,/,maxstack=1024):                  # BinaryFilemanager::__init__
#     def push(self,ch) -> 'self':                            # BinaryFilemanager::push()
#     def getch(self,/,count=1) -> bytes:                     # BinaryFilemanager::getch()
#     def peek(self) -> bytes:                                # BinaryFilemanager::peek()
#     def eof(self) -> bool:                                  # BinaryFilemanager::eof()
#     def ischar(self,ch):                                    # BinaryFilemanager.ischar()
#     def find(self,ch,/,pushback=False) -> (bytes,bytes):    # BinaryFilemanager.find()
#     def pushback(self,ch : bytes) -> 'self':                # BinaryFilemanager::pushback()
# if __name__ == "__main__":
#
#
#
# 2022-10-29T09:25:25-0600 wlg
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
    """class BinaryFilemanager(object) Given a filehandle opened 'rb',
       manage processing the file.  This class provides both one char
       lookahead and infinite pushback opportunities.  For example
       while looking for <ETX> we find a <RS>; then pushback the <RS>
       and try another logic-path.
    push(ch)
    getch() getch(10)
    peek()
    ischar(ch)
    find(ch) find(ch,True)
    pushback(ch)
    """

    def __init__(self,fh,/,maxstack=1024):                  # BinaryFilemanager::__init__
        """Set up the file handle open 'rb', manage an infinite look
        back, with one char lookahead."""
        self.fh        = fh                    # the file handle
        self.nextch    = fh.read(1)            # may be EOF
        self.position  = 0                     # track the logical position
        self.stack     = b''                   # init to signal EOF
        self.maxstack  = maxstack              # upper limit on push backs

    ### BinaryFilemanager.__init__()

    def push(self,ch) -> 'self':                            # BinaryFilemanager::push()
        """If the length of the stack is sane, push length of ch
        characters back for later tries. Pevent find(ch) for a ch
        that is way way far away.
        """
        if((len(stack) + len(ch)) < self.maxstack):
            self.stack = self.stack + ch
        else:
            raise OverflowError("BinaryFilemanager: pushback overflowed {self.maxstack} bytes")

        return self

    ### BinaryFilemanager.push()

    def getch(self,/,count=1) -> bytes:                     # BinaryFilemanager::getch()
        """Get the the char (or more with count >= 1).
        Raises EOFError"""
        ret = b''                              # be safe...
        if(len(self.stack) != 0):              # something pushed back
            print(f"stack is {len(self.stack)}")
            ret            = self.stack[0]         # get the char
            self.stack     = self.stack[1:]        # manage pushback stack
            self.position += 1                 # (re) advance the logical position
        else:
            ret        = self.nextch           # OK pending next char
            if(ret == b''):                    # here is where we may hit EOF
                raise BinaryFileManagerEOF(f"fh at {fh.tell()} or {self.position} by our reckoning.")
            self.nextch    = self.fh.read(count)
            self.position += 1
        return ret                             # single exit

    ### BinaryFilemanager.getch()

    def peek(self) -> bytes:                                # BinaryFilemanager::peek()
        """Take a peek at the next available character.
        The peek is buffered 1 deep w.r.t. the file handle.
        """
        return self.nextch                     # allow look-ahead

    ### BinaryFilemanager.peek()

    def eof(self) -> bool:                                  # BinaryFilemanager::eof()
        """Duh -- Is the next char really the EOF"""
        return self.nextch == b''

    ### BinaryFilemanager.eof()

    def ischar(self,ch):                                    # BinaryFilemanager.ischar()
        """If not EOF then ask if the next char may be the one you are looking
        for. This saves peek() and test on your end.
        """
        return (isinstance(ch,b'') and ch == self.nextch())

    ### BinaryFilemanager.ischar()

    def find(self,ch,/,pushback=False) -> (bytes,bytes):    # BinaryFilemanager.find()
        """Find the character, return ch, skipped if(b'') is False.
        This function is here mainly to assist with error recovery
        with the main idea is that ch is nearby.
        """
        skipped = b''
        try:
            while((c := self.getch()) != ch):  # expect character nearby skipped is empty...
               skipped = skipped + ch          # ...if successful, or what we had to skip
        except BinaryFileManagerEOF as eof:
            if(pushback):
                self.pushback(skipped)
            c       = None                     # did not find it
            skipped = b''                      # put it all back.
        return skipped,c                       # return None and a ch  or [bads],ch

    ### BinaryFilemanager.find()

    def pushback(self,ch : bytes) -> 'self':                # BinaryFilemanager::pushback()
        """Pushback one or more characters such that getch gets the
        first (subsecent) one(s) from this action before picking up
        with the original reads from fh."""
        self.push(ch)                           # push one or more on to byte array if OK
        self.position =- len(ch)                # adjust the count.

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
                print(f"{fm.count} bytes from file {filename}",file=sys.stderr)
            print(f"File {filename} complete.")
        except BinaryFileManagerEOF as eof:
            print(f"EOF found for file {filename}",file=sys.stderr)
        except OverflowError as over:
            print(f"Overflow, pushed back too many things",file=sys.stderr)
        except BinaryFileManagerException as ex:
            print(f"Exception with {filename}\n{ex.__str__()}",file=sys.stderr)

