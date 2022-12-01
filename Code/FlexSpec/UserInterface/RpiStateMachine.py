#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# /home/git/external/SAS_NA1_3D_Spectrograph/py/RpiStateMachine.py
#
# (wg-python-fix-pdbrc)
#
#
# (compile (format "python -m py_compile %s" (buffer-file-name)))
# (compile (format "pydoc3 %s" (buffer-file-name)))
#############################################################################
### HEREHEREHERE
import os
import optparse
import sys
import re
from RpiFlexCharmap import   *   # RpiFlexCharmap
from FlexJSONCompiler import *   # FlexJSONCompiler



#############################################################################
#
#  /home/wayne/play/Wayne/RpiStateMachine.py
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
# __all__     = ['RpiStateMachine','RpiFlexStateMachineException']   # list of quoted items to export
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
#     def _teststatemachine():
#
#
#
#############################################################################



__doc__ = """

/home/wayne/play/Wayne/RpiStateMachine.py
[options] files...



"""


__author__  = 'Wayne Green'
__version__ = '0.1'
__all__     = ['RpiStateMachine','RpiFlexStateMachineException']   # list of quoted items to export


##############################################################################
# RpiFlexStateMachine.Exception
#
##############################################################################
class RpiFlexStateMachineException(Exception):
    """Special exception to allow differentiated capture of exceptions"""
    def __init__(self,message,errors=None):
        super(RpiFlexStateMachineException,self).__init__("RpiFlexStateMachine"+ message)
        self.errors = errors
    @staticmethod
    def __format__(e):
        return f" RpiFlexStateMachine: {e.__str__()}\n"
# RpiFlexCharmapException

##############################################################################
# RpiStateMachine
#
##############################################################################
class RpiStateMachine:
    """Implement the same statemachine as the Arduino side. A few liberties
    were taken in Python.
    All states have the same signature of byte
    """

    class ASCIIControl:
        """\
        Special Control Characters (complete here), that are of type
        <class 'bytes'>
        """
        ASCIINULL =   bytes([0])      #  Null character
        SOH       =   bytes([1])      #  Start of Header
        STX       =   bytes([2])      #  Start of Text
        ETX       =   bytes([3])      #  End of Text, hearts card suit
        EOT       =   bytes([4])      #  End of Transmission, diamonds card suit
        ENQ       =   bytes([5])      #  Enquiry, clubs card suit
        ACK       =   bytes([6])      #  Acknowledgement, spade card suit
        BEL       =   bytes([7])      #  Bell
        BS        =   bytes([8])      #  Backspace
        HT        =   bytes([9])      #  Horizontal Tab
        LF        =   bytes([10])     #  Line feed
        VT        =   bytes([11])     #  Vertical Tab, male symbol, symbol for Mars
        FF        =   bytes([12])     #  Form feed, female symbol, symbol for Venus
        CR        =   bytes([13])     #  Carriage return
        SO        =   bytes([14])     #  Shift Out
        SI        =   bytes([15])     #  Shift In
        DLE       =   bytes([16])     #  Data link escape
        DC1       =   bytes([17])     #  Device control 1
        DC2       =   bytes([18])     #  Device control 2
        DC3       =   bytes([19])     #  Device control 3
        DC4       =   bytes([20])     #  Device control 4
        NAK       =   bytes([21])     #  NAK Negative-acknowledge
        SYN       =   bytes([22])     #  Synchronous idle
        ETB       =   bytes([23])     #  End of trans. block
        CAN       =   bytes([24])     #  Cancel
        EM        =   bytes([25])     #  End of medium
        SUB       =   bytes([26])     #  Substitute
        ESC       =   bytes([27])     #  Escape
        FS        =   bytes([28])     #  File separator
        GS        =   bytes([29])     #  Group separator
        RS        =   bytes([30])     #  Record separator
        US        =   bytes([31])     #  Unit separator
        DEL       =   bytes([127])    #  Delete

    # class RpiStateMachine.ASCIIControl

    class MessageStatus:                                    # RpiStateMachine.MessageStatus
        """\
        A few constants that match semantics in the C++ side of this mess.
        """
        IDLE    = 1
        GETCRC  = 2
        HAVECRC = 3
        ACTIVE  = 4
        FULL    = 5
        ERROR   = 6
        TIMEOUT = 7

        xlate = { 1 : "IDLE",                            # static member variable
                  2 : "GETCRC",
                  3 : "HAVECRC",
                  4 : "ACTIVE",
                  5 : "FULL",
                  6 : "ERROR",
                  7 : "TIMEOUT"
                }  # RpiStateMachine.MessageStatus

        @staticmethod
        def xlatestate(st : int):                           # RpiStateMachine.MessageStatus.xlatestate()
            """translate back into words"""
            return  RpiStateMachine.MessageStatus.get(st,f"UNKNOWN {st}")

        ### RpiStateMachine.MessageStatus.xlatestate()

    ### RpiStateMachine.class MessageStatus

    def __init__(self,maxcount : int = 512):
        """Set up the state machine, declare the variables here.
        Transliterated from the C++. OK Should have done the algorithm
        in Cython.

        """
        self.maxcount    =  maxcount             # const int       Set to some maximum
        self.buffer      =  ""                   # std::string   * Get() a message, and build incomming text here.
        self.errors      =  ""                   # std::string     maintain our own list of errors
        self.count       =  0                    # int             ciount chars appended to buffer. Anticipating a maxcount.
        self.crc         =  0                    # uint32_t        The actual crc
        self.crccount    =  0                    # unsigned int    The count of CRC chars exactly 4
        self.badprecount =  0                    # int             total illegal chars seen before STX
        self.timeout     =  1000                 # unsigned long   Max duration while active wait for message in milliseconds 1000 = 1sec.
        self.timerstart  =  0                    # unsigned long   current timer (when expecting it.) (updates on each write())
        self.timer       =  0                    # unsigned long   current timer (when expecting it.) (updates on each write())
        self.charmap     =  RpiFlexCharmap()     # Flex_Charmap  & The legal characters we'll tolerate.
        self.statecount  =  0                    # spot runaway states.
        self.charmap     =  RpiFlexCharmap()     # an instance of the map
        self.statepath   =  []                   # accumulate list of states as we go.
        self.state       =  RpiStateMachine.MessageStatus.IDLE   # current state.
        self.states      =  { RpiStateMachine.MessageStatus.IDLE    : lambda ch : self.idlestate(ch)   , # -> GETCRC
                              RpiStateMachine.MessageStatus.GETCRC  : lambda ch : self.getcrc(ch)      , # -> HAVECRC
                              RpiStateMachine.MessageStatus.HAVECRC : lambda ch : self.havecrc(ch)     , # -> ACTIVE
                              RpiStateMachine.MessageStatus.ACTIVE  : lambda ch : self.active(ch)      , # -> IDLE (FULL) (ERROR)
                              RpiStateMachine.MessageStatus.FULL    : lambda ch : self.full(ch)        , # -> on <ETX> -> IDLE
                              RpiStateMachine.MessageStatus.ERROR   : lambda ch : self.error(ch)       , # -> on <ETX> -> IDLE
                              RpiStateMachine.MessageStatus.TIMEOUT : lambda ch : self.error(ch)         # -> on <ETX> -> IDLE
                            } # the states, self.states has to be assigned inside of self.xxx functions.

    def reset(self):
        """Assume fubar, set up the machine"""
        state = RpiStateMachine.MessageStatus.IDLE
        self.statepath=[]

        return self

    ### RpiStateMachine.reset()

    def trackstate(self,newstate):                          # RpiStateMachine.trackstate()
        """Aappend the state to the list."""
        curstate,count = self.statepath[:-1]             # pick up the last state
        if(curstate == newstate):
            self.statepath[:-1] = (curstate, ++count)    # add one as a repeat
        else:
            self.statepath.append(newstate, 1)           # initialize to 1
        if(newstate == RpiStateMachine.MessageStatus.ERROR ):
            raise RpiFlexStatemachineException(f"State wound up in error{self.reportstate}")

        return self

    ### RpiStateMachine.trackstate()

    def reportstate(self):                                  # RpiStateMachine.reportstate()
        """Draw ASCII primitive art, and reset the state"""
        arrow = ""
        for k,v in self.statepath:
            print(f"{arrow} {k}({v})",end=None)
            arrow = "->"
        self.statepath=[]

        return self

    ### RpiStateMachine.reportstate()

    ##################################################################
    #                        The State Machine
    #
    ##################################################################
    def idlestate(rawch : bytes) -> MessageStatus:
        """Hang here until <STX> is seen. <ETX><ETX><STX> does recover. """
        self.statepath.append(RpiStateMachine.MessageStatus.IDLE)       # PDB-DEBUG
        ch = self.charmap[rawch]
        if(ch == ASCIIControl.ETX):
             ret = RpiStateMachine.MessageStatus.IDLE    # Stay in IDLE
        elif(ch == ASCIIControl.SOH):                    # Eat this char,
            crc      = 0                                 # clear the crc
            crccount = 0
            crcgen.Start()                               # (re)start the crc
            ret = RpiStateMachine.MessageStatus.GETCRC   # move to next state
        elif(ch is None):
            ret = RpiStateMachine.MessageStatus.ERROR
        else:
            self.buffer += ch
        ret     =  RpiStateMachine.MessageStatus.ERROR

        state = ret                                      # have to do this here in Python

        return ret

    ### RpiStateMachine.idlestate(ch : bytes)

    def getcrc(ch : bytes) ->MessageStatus:
        """Start to accumulate 8 nybble images of hex values
        for the CRC.
        """
        self.statepath.append(RpiStateMachine.MessageStatus.GETCRC)
        ret    =  RpiStateMachine.MessageStatus.ERROR    # Assume fail...
        val    = 0
        status = 1

        if(self.crccount != 0):
            ret = RpiStateMachine.MessageStatus.GETCRC   # expecting and got crc ch
            crc = crc << 4 | ch                          # accumulate as hex nybble
            if(--crccount == 0) :                        # If we go to zero assume we're done
                ret = RpiStateMachine.MessageStatus.HAVECRC

        state = ret                                      # have to do this here in Python

        return ret                                       # same or next state {GETCRC,HAVECRC,ERROR}

    ### RpiStateMachine.getcrc(ch : bytes)

    def havecrc(ch : bytes) ->MessageStatus:
        """Finished the CRC, expecting the <STX>"""
        self.statepath.append(RpiStateMachine.MessageStatus.HAVECRC)
        ret =  RpiStateMachine.MessageStatus.ERROR        # Assume fail
        if(ch == ASCIIControl.STX):                       # Expecting and ...
            ret = RpiStateMachine.MessageStatus.ACTIVE    # got token to move to next state

        self.state = ret                                  # have to do this here in Python

        return ret                                        # must move to state {Active,ERROR}

    ### RpiStateMachine.havecrc(ch : bytes)

    def active(ch : bytes) ->MessageStatus:
        """Found the <STX> at end of CRC, starting to process first and
        subsequent bytes of payload while the characters are legal,
        the <ETX> not found and the buffer is still reasonable in
        length; accumulate the characters.
        """
        self.statepath.append(RpiStateMachine.MessageStatus.ACTIVE)
        ret =  RpiStateMachine.MessageStatus.ERROR        # Assume fail

        if(buffer == nullptr):                           # need buffer?
            buffer = queue.Acquire()                     # Acquire from the shared queue
            if(buffer == nullptr):                       # didn't get one, queue full
                return ret                               # PREMATURE RETURN to ERROR state
        if(len(buffer) < maxcount):                      # Haven't flooded into too many chars
            if(ch == ASCIIControl.ETX):                  # We may be at end
                # get the crc
                # compare the crc
                # if crc good pass buffer off to the dispatch queue
                # else error out.
                ret = RpiStateMachine.MessageStatus.IDLE
            elif(charmap[ch]):
                buffer += ch                              # Add to the buffer
                ret    =  RpiStateMachine.MessageStatus.ACTIVE
            else:
                queue.Return(buffer)                      # Return the buffer to the queue, unused.
                ret     = RpiStateMachine.MessageStatus.ERROR             # Bad character
        else:
            queue.Return(buffer)                         #  Return the buffer to the queue, unused.
            ret =  RpiStateMachine.MessageStatus.FULL

        self.state = ret                                 # have to do this here in Python

        return ret

    ### RpiStateMachine.active(ch : bytes)

    def full(ch : bytes) ->MessageStatus:
        """Oops, buffer went FULL, put us in the full state. Stay here until
        an ETX is seen.

        """
        self.statepath.append(RpiStateMachine.MessageStatus.FULL)
        ret =  RpiStateMachine.MessageStatus.FULL                         # Kinda like ERROR
        if(ch == ASCIIControl.ETX):                # OK we,re good to go
            ret    =  RpiStateMachine.MessageStatus.IDLE
            errors += "Buffer is bad."
            errors += buffer
            errors += "\n"

        state = ret                                       # have to do this here in Python

        return ret

    ### RpiStateMachine.full(ch : bytes)

    def error(ch : bytes) ->MessageStatus:
        """We got into some ERROR state, illegal char etc. Stay here until we
        see <ETX>

        """
        self.statepath.append(RpiStateMachine.MessageStatus.ERROR)
        ret =  RpiStateMachine.MessageStatus.ERROR                        # hang around until ETX
        if(ch == ASCIIControl.ETX):
            errors += "Buffer is bad."
            errors += buffer
            errors += "\n"
            queue.Return(buffer)                          # drop the buffer
            ret = RpiStateMachine.MessageStatus.IDLE                      # found redemption

        state = ret                                       # have to do this here in Python

        return ret

    ### error(ch : bytes)

    def validjson(self,txt : str):
        """See if string is valid"""
        return self.charmap.validjson(txt.encode())

# class RpiStateMachine

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

    def _teststatemachine():
        """Test the state machine"""
        goodjson = """{"kzin" : {"process"  : {"halpha" : "1", "hbeta" : "1"}}}"""
        badjson  = """{"kzin" : {"process<" : {"halpha" : "1", "hbeta" : "1"}}}"""

        sm = RpiStateMachine()
        try:
            for i,s in enumerate([goodjson,badjson]):
                print(f"{i} {sm.validjson(s)} {s}")
        except Exception as e:
            print(f"_teststatemachine: {s}\n{e.__str__()}")
            #raise

    ### _teststatemachine()

    fc = FlexJSONCompiler(goodjson)
