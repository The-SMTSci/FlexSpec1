#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# SAS_NA1_3D_Spectrograph/py/FlexJSONCompiler.py
#
#
# (wg-python-toc)
#
#
# (compile (format "python -m py_compile %s" (buffer-file-name)))
# (compile (format "pydoc3 %s" (buffer-file-name)))
#
# (wg-astroconda3-pdb)
#
# (wg-python-fix-pdbrc)
#
# (compile "./FlexJSONCompiler.py GUI_Scenario_Display.txt")
#
# (compile "./FlexJSONCompiler.py --dumper fakemessage.bin")
#
# (wg-python-toc)
#
# __doc__ = """
# __author__  = 'Wayne Green'
# __version__ = '0.1'
# __all__     = ['FlexJSONCompilerException','FlexJSONCompiler']   # list of quoted items to export
# class FlexJSONCRCException(Exception):
#     def __init__(self,message,errors=None):
#     @staticmethod
#     def __format__(e):
# class FlexJSONCRC(object):
#     def __init__(self):                                     # FlexJSONCRC::__init__()
#     def encode(self,jsonstr : (bytes,str))->bytes:                        #  Flexjsonstr::encode()
#     def decode(self,jsoncrc : (str,bytes)) -> int:          # FlexJSONCRC::decode()
#     def debug(self,msg="",skip=[],os=sys.stderr):           # FlexJSONCRC::debug()
# class FlexJSONCompilerException(Exception):
#     def __init__(self,message,errors=None):
#     @staticmethod
#     def __format__(e):
# class FlexJSONCompiler(object):
#     def __init__(self,                                      # FlexJSONCompiler::__init__()
#     def setfilename(self,filename):                         # FlexJSONCompiler.setfilename()
#     def compilerecord(self,                                 # FlexJSONCompiler.compilerecord
#     def compile(self,                                       # FlexJSONCompiler.compile()
#     def writefile(self,filename=None):
#     def debug(self,msg="",skip=[],os=sys.stderr):           # FlexJSONCompiler::debug()
#     def uncompilerecord(self,                               # FlexJSONCompiler.uncompilerecord()
#     def uncompile(self,infile="",verboseflag = False):          # FlexJSONCompiler.uncompile()
#     @staticmethod
#     def encode(payload : str, addrs=False) -> bytes:
# if __name__ == "__main__":
#
#
#
# 2022-10-11T09:04:28-0600 wlg -- converted to a class, allows importing
# 2022-10-27T07:06:49-0600 wlg -- cleaned up (probably broke) file.
#                                 changed name, made more general in scope.
#
#############################################################################
### HEREHEREHERE

import os
import io
import sys
import re
import json
import zlib                                        # calculate the CRCs
from io import BytesIO                             # needed for byte manips.
from FlexFileManager import BinaryFileManager,  BinaryFileManagerException, BinaryFileManagerEOF
from RpiFlexCharmap import *
if(0):
    import traceback

__doc__ = """

/home/git/external/flexberry/code/py/FlexJSONCompiler.py

Generate test data for testing statetable and other dispatch related
activities.

-o --output       - the output file name
-r --recsep       - use a <RS> for linux testing.
-v --verboseflag  - be wordy about work as needed
--dumper          - generate a ASCII-string human output


write a binary file to serve as fake terminal input.
this will consist of the usual stream from the python dispatchserver:
each batch of chars have a very special record separator 0x30 character
that fakeserial read will filter. when fakeread sees one, it will
freeze for a specified time in that c++ code.

./FlexJSONCompiler.py gui_scenario_display.txt

The format of a FlexSpec1 record is presumed to be:

    <SOH>C1C2C3C4C5C6C7C8<STX>{valid json}<ETX>

where: SOH is start-of header the critical byte C1C2C3C4C5C6C7C8 are
       the ASCII letters with hex values for each nybble of a
       Bigendian 4-Byte CRC per zlib.crc32. <STX>{valid json
       payload}<ETX> is the sub-record within the record for the
       FlexSpec1 valid JSON. This relates to proper keywords (a check
       not performed here) and any numeric value is a "value" to be
       easy to parse with ArduinoJson package.

"""

__author__  = 'Wayne Green'
__version__ = '0.1'
__all__     = ['FlexJSONCompilerException','FlexJSONCompiler']   # list of quoted items to export

_charmap = RpiFlexCharmap()   # global scope, used for testing.
_crcfix  = re.compile(r' ')

##############################################################################
# FlexJSONCRCException
#
##############################################################################
class FlexJSONCRCException(Exception):
    """Special exception to allow differentiated capture of exceptions"""
    def __init__(self,message,errors=None):
        super(FlexJSONCRCException,self).__init__("FlexJSONCRC "+ message)
        self.errors = errors
    @staticmethod
    def __format__(e):
        return f" FlexJSONCRC: {e.__str__()}\n"
# FlexJSONCRCException

##############################################################################
# FlexJSONCRC
#
##############################################################################
class FlexJSONCRC(object):
    """ A class to make/unmake crc's from JSON protocol. This is a CRC32
    BigEndian 8 bits returned as the ASCII-HEX representation.
    """

    def __init__(self):                                     # FlexJSONCRC::__init__()
        """Initialize this class."""
        #super().__init__()
        # (wg-python-property-variables)

    ### FlexJSONCRC.__init__()

    def encode(self,jsonstr : (bytes,str))->bytes:                        #  Flexjsonstr::encode()
        """Given a payload a json string , return a CRC bytes object with
        8 ASCII values of HEX characters for the nybbles of a 32-bit BigEndian
        CRC.

        """
        json     = jsonstr                           # grab input, assume its bytes
        bytescrc = b''
        if(isinstance(jsonstr, str)):
            json = jsonstr.encode()                  # turn into bytes
        if(isinstance(json,bytes)): # HEREHEREHERE
            bytescrc = bytes([f"{c:02x}" for c in json]) #  _crcfix.sub('0',"%08d" % zlib.crc32(json)).encode()
        else:
            raise FlexjsonstrException(f"FlexJSONCRC encode must be of type str or byte. Found {type(jsonstr)}")

        return bytescrc

    ###  FlexJSONCRC.encode()

    def decode(self,jsoncrc : (str,bytes)) -> int:          # FlexJSONCRC::decode()
        """With a 8 byte crc value of type byte (str), convert
        back into an int"""
        intcrc = None
        if(isinstance(jsoncrc,str)):
            json = str.encode()
        if(isinstance(json,bytes)):
            intcrc = json.decode()
        else:
            raise FlexJSONCRCException(f"FlexJSONCRC decode must be of type str or byte. Found {type(jsoncrc)}")

        return intcrc

    ### FlexJSONCRC.decode()

    def debug(self,msg="",skip=[],os=sys.stderr):           # FlexJSONCRC::debug()
        """Help with momentary debugging, file to fit.
           msg  -- special tag for this call
           skip -- the member variables to ignore
           os   -- output stream: may be IOStream etc.
        """
        import pprint
        print("FlexJSONCRC - %s " % msg, file=os)
        for key,value in self.__dict__.items():
            if(key in skip):
               continue
            print(f'{key:20s} =',file=os,end='')
            pprint.pprint(value,stream=os,indent=4)
        return self

    ### FlexJSONCRC.debug()

# class FlexJSONCRC

##############################################################################
# FlexJSONCompilerException
#
##############################################################################
class FlexJSONCompilerException(Exception):
    """Special exception to allow differentiated capture of exceptions"""
    def __init__(self,message,errors=None):
        super(FlexJSONCompilerException,self).__init__("FlexJSONCompiler "+ message)
        self.errors = errors
    @staticmethod
    def __format__(e):
        return f" FlexJSONCompiler: {e.__str__()}\n"
# FlexJSONCompilerException

##############################################################################
# FlexJSONCompiler
#
##############################################################################
class FlexJSONCompiler(object):
    """FlexJSONCompiler: compile and uncompile stream-images with FlexSpec packets.
    The packet may have <RS> (record separators for linux development support) (or not)
    and consists mainly of:

       [<RS>]<SOH>C1C2C3C4C5C6C7C8<STX>...flex legal json...<ETX>

    images. Includes the ability is to make a .bin file for testing
    (with the <RS>, initial bootstrap code, and to decypher strings as
    they come in.

    The CRC is written as series of 8 characters, each a nybble of the 4 byte
    BIG endian crc sum.

    Python hates bytes.
    def __init__(self,infilename  : str,/, options     : dict = None)
    def compilerecord(self,payload : str)
    def compile(self,datastream : ...)
    def writefile(self,filename=None):
    def debug(self,msg="",skip=[],os=sys.stderr):
    def uncompilerecord(self,infilehandle : BinaryFileManager)
    def uncompile(self,infile="",verboseflag = False):

    def encode(payload : str, addrs=False) -> bytes:   @staticmethod

    """

    # class variables
    xlate = {ord('0') :  0, ord('1') :  1, ord('2') :  2, ord('3') :  3,
             ord('4') :  4, ord('5') :  5, ord('6') :  6, ord('7') :  7,
             ord('8') :  8, ord('9') :  9, ord('A') : 10, ord('B') : 11,
             ord('C') : 12, ord('D') : 13, ord('E') : 14, ord('F') : 15,
             ord('a') : 10, ord('b') : 11, ord('c') : 12, ord('d') : 13,
             ord('e') : 14, ord('f') : 15
            } # convert chars into integers

    ASCII_RS   = chr(0x1e).encode()  # FlexJSONCompiler.ASCII_RS
    ASCII_SOH  = chr(1)   .encode()  # FlexJSONCompiler.ASCII_SOH
    ASCII_STX  = chr(2)   .encode()  # FlexJSONCompiler.ASCII_STX
    ASCII_ETX  = chr(3)   .encode()  # FlexJSONCompiler.ASCII_ETX

    MAXSIZE    = 2048                                        # prevent runaway loop

    msgsplit = re.compile(r'[ ]*=[ ]*')                      # GII display's panel image splitter

    # Include the stream types we like.
    acceptabletypes = {io._io.BufferedReader, io._io.FileIO, io._io.BytesIO, io._io.TextIOWrapper}

    def __init__(self,                                      # FlexJSONCompiler::__init__()
                 instream  : BinaryFileManager,
                 /,                        # the input filename
                 options     : dict = None                   # callable without options
                ):
        """Create a usable instance.
        options.output       - as program, take good data; produce binary image
        options.recsep       - with a streamm, accept records return payloads
        options.uncompile    - given a file, roundtrip back to 'outputs' input sans comments.
        options.verboseflag  - be chatty
        """

        if(options is None):                                 # make into a dict, to easily
            self.options = {}                                # setup defaults with dict semantics.
        else:
            self.options     = vars(options)                 # convert to a usable dict structure
        self.infilestream    = instream                          # Bokeh display like commands.
        self.dumperrecno = 0                                 # try to he helpful
        self.binimage    = None                              # compiled image seek(0) to start from top
        self.crc         = None
        self.outfilename = self.options.get('output'     , "gencrc.out")
        self.verboseflag = self.options.get('verboseflag', False)
        self.recsep      = self.options.get('recsep'     , False)

    ### FlexJSONCompiler.__init__()

    def compilerecord(self,                                 # FlexJSONCompiler.compilerecord
                      payload : str                               # the 'json string'
                     ) -> bytes:
        """Given a simple json string;
        return <RS><SOH>CcCcCcCc<STX>bytes of string<ETX>
        """
        if(self.binimage is None):
            self.binimage = BytesIO()                             # create an BytesIO instance, use write semantics
        if(self.recsep):
            self.binimage.write(FlexJSONCompiler.ASCII_RS)        # write ASCII Record Separator
        self.binimage.write(FlexJSONCompiler.ASCII_SOH)           # write the SOH
        self.binimage.write(("%08X" % self.crc).encode())         # 8 bytes CRC zero padded
        self.binimage.write(FlexJSONCompiler.ASCII_STX)           # the STX char
        self.binimage.write(payload)                              # the payload as bytes
        self.binimage.write(FlexJSONCompiler.ASCII_ETX)           # the ETX

        return self.binimage

    ### FlexJSONCompiler.compilerecord

    def compile(self,                                       # FlexJSONCompiler.compile()
                datastream : (io._io.BufferedReader, # standare open(fname,'r')
                              io._io.FileIO,         # binary open open(fname,'rb')
                              io._io.BytesIO         # a bytes data struct as a stream.
                             ) = None
               ):
        """Given a stream (io.FileIO,io.BufferedReader), or bytes as BytesIO
        Compile the structure, return self.  indatastream is a regular
        string-like file with complete pythonic JSON structures,
        compatible with Python3's 'json' package. It is presumed to
        follow FlexSpec1' Scenario2 format.

        Blank lines are ignored, any line with a '#' is considered to be
        A '#' to end of line is considered a comment and dropped. (hacky)

        At the end, the self.binimage is loaded, but positioned at the
        end of the file. Additional calls may be made.

        """
        if(datastream is None):
            if(self.infilestream is None):
                raise FlexJSONCompilerException("FlexJSONCompiler.compile has no stream")
        elif(type(datastream) not in FlexJSONCompiler.acceptabletypes):
            raise FlexJSONCompilerException("FlexJSONCompiler.compile wrong type: {type(datastream)}")
        try:
            for l in self.infilestream:
                l = l.strip()                            # remove leading/trailing/newlines
                if(len(l) == 0):                         # skip blank lines
                    continue
                parts = l.split('#',1)                   # flens (any) trailing comments
                #parts = FlexJSONCompiler.msgsplit.split(l)[:1]  # Flense trailing comments...
                if(parts is None or parts[0] == ''):
                    continue                             # ...nothing left
                payload       = parts[0].encode()        # turn to raw bytes
                self.crc      = zlib.crc32(payload)      # calculate the CRC
                self.compilerecord(payload,self.binimage)# add this record to the image
        except Exception as e:
            print(f"Oops FlexJSONCompiler.py: file |{datastream}| not found\n{e.__str__()}",file=sys.stderr)
            print(f"{os.getcwd()}",file=sys.stderr)
        if(options.verboseflag):
            raise

        return self

    ### FlexJSONCompiler.compile()

    def writefile(self,filename=None):
        """Write the compiled BytesIO structure to a proper file.
        Routine rewinds the entire binary image, writes it to filename
        thus leaving the binary image at its end for contunuing.
        """
        if(filename is not None):
            self.outfilename = filename
        with open(self.outfilename,'wb') if(not isinstance(filename,io._io.TextIOWrapper)) else filename as bof: # a binary output file.
            self.binimage.seek(0)                                 # rewind now
            c = bof.write(self.binimage.read())                   # write this batch of bytes to special file.
        if(options.verboseflag):
            print(f"Wrote {c} bytes")                             # chat about it.

        return self

    ### FlexJSONCompiler.writefile

    def uncompilerecord(self,                             # FlexJSONCompiler.uncompilerecord()
                        infilestream : BinaryFileManager = None): # be chatty and raise on errors

        """\ Given an open 'file handle' or 'infilestream', to a bin file used
        for testing, transliterate bytes for an image of record(s).
        The format of FlexSpec1 testing records are presumed to be:

        <RS><SOH>C1C2C3C4C5C6C7C8<STX>{valid json}<ETX>[<RS>...<STX>]EOF

        where: <RS> is a record separator, to pace input for testing
               via Unix FakeSerial.

               <SOH> is Start-Of Header

               C1C2C3C4C5C6C7C8 is the checksum, an ASCII representation of a BIG ENDIAN 32bit unsigned
               integer per zlib.crc32

               <STX>{valid flexspec json}<ETX> is the sub-record...

               ...within the record for the FlexSpec1 valid JSON. This
               relates to proper keywords (a check not performed here)
               and any numeric value is a "ascii value" easily parsed
               with ArduinoJson package.  Newlines accumulate as
               warnings.

        A binary file with the <RS> will be used to test statemachines.

        """
        if(infilestream is None and self.instream is None):
            raise FlexJSONCompilerException("FlexJSONCompiler.uncompilerecord can not find input stream.")
        try:
            self.dumperrecno += 1                            # Update the count
            errors           = []                            # accumulate errors this record
# HEREHEREHERE
            try:
                working = True
                while(working):                              # assume the infilestream is aligned on <RS>
                    errmsg      = "Seeking RS (Record Separator)"
                    seeking     = FlexJSONCompiler.ASCII_RS
                    skipped, ch = self.infilestream.find(seeking)  # skipped of none is good

                    if(not skipped and ch is not None):      # found it right off
                        rawcrc = b''                         # prepare the CRC
                        for i in range(8):
                            rawcrc += self.getch()
                        for c in rawcrc:
                            crc = (crc << 4) | c
                    else:
                        errors.append(msg := f"Unable to find a record seeking {seeking} {infilestream.count}")
                        raise FlexJSONCompilerException(msg)

                    seeking     = FlexJSONCompiler.ASCII_SOH
                    skipped, ch = self.infilestream.find(seeking)

                    if(not skipped):
                        seeking = FlexJSONCompiler.ASCII_ETX
                        skipped, ch = self.infilestream.find(seeking)  # Ah HA! skipped is the json record
                        if(self.verboseflag):
                            print(skipped)
                        if(not _charmap.validjson(skipped)):
                            error.append(msg := f"Bad payload {skipped} {infilestream.count}")
                            raise FlexJSONCompilerException(msg)
                        json    = skipped.encode()           # Brew up the string version
                        #jsoncrc = zlib.crc32(json)           # get its crc
                        jsoncrc = _crcfix.sub('0',"%08s" % zlib.crc32(json).decode())
                        print(f"{crc} = {jsoncrc} ? {json}") # print TODO finish thought here.
                    else:
                        errors.append(msg:=f"Unable to find a record seeking {seeking} {infilestream.count}")
                        raise FlexJSONCompilerException(msg)
            except Exception as e:
                print(f"Caught\n{e.__str__()}")
        except Exception as e:
            print(f"Outer Caught\n{e.__str__()}")

        return self

    ### FlexJSONCompiler.uncompilerecord()

    def uncompile(self,infile="",verboseflag = False):          # FlexJSONCompiler.uncompile()
        """just pretty print the file. walk through the file structure.
           Call uncompilerecord for each 'record' in the file. Any proper
           non-printable values are stated in readable form. E.g.: 0x01
           is <SOH>; 0x02 is <STX> 0x03 is <ETX> others are debatable
        """
        if(outfile == ""):
            outfile = sys.stdout
        else:
            outfile = open(outfile,'w')                # ASCII file afterall

        try:
            fh = open(self.filename,'rb')    # filename = "FakeMessage.bin"
            for i in range(100):
                (eof,record) = self.uncompilerecord(fh,infile)
                if(eof):
                    break
                print(f"{record}",file=outfile)
            outfile.close()
        except Exception as e:
            errors.append(msg:=f"error in uncompile for file {filename}\n{e.__str__()}")
            print(msg,file=sys.stderr)
            print(f"   {e}", file=sys.stderr)
            #print(traceback.format.exc(),file=sys.stderr)
            sys.exit(1)

    ### FlexJSONCompiler.uncompile()

    @staticmethod
    def encode(payload : str, addrs=False) -> bytes:
        """Add the wrapper for the payload.
        <SOH>crc<STX>payload<ETX>
        """
        epayload  = payload.encode()                               # encode the payload
        crc       = zlib.crc32(epayload)                           # calculate the CRC
        record    = FlexJSONCompiler.ASCII_SOH                     # start with SOH
        if(addrs):                                                 # if RS wanted
            record    = FlexJSONCompiler.ASCII_RS + record         # prepend it.
        record   += bytes(_crcfix.sub('0',"%08s" % crc.decode()))  # short string might happen
        record   += epayload                                       # append bytes of payload
        record   += FlexJSONCompiler.ASCII_ETX                     # add the end of transmission

        return record                                              # return the string.

    ### staticmethod FlexJSONCompiler.encode()

    def debug(self,msg="",skip=[],os=sys.stderr):           # FlexJSONCompiler::debug()
        """Help with momentary debugging, file to fit.
           msg  -- special tag for this call
           skip -- the member variables to ignore
           os   -- output stream: may be IOStream etc.
        """
        import pprint
        print("FlexJSONCompiler - %s " % msg, file=os)
        for key,value in self.__dict__.items():
            if(key in skip):
               continue
            print(f'{key:20s} =',file=os,end='')
            pprint.pprint(value,stream=os,indent=4)
        return self

    ### FlexJSONCompiler.debug()

# class FlexJSONCompiler

##############################################################################
#                                    main
#                               regression tests
##############################################################################
# hereherehere
if __name__ == "__main__":
    import optparse

    opts = optparse.OptionParser(usage="%prog"+__doc__)

    opts.add_option("-o", "--output", action="store", dest="output",
                   default="gencrc.out",
                   help="<filename>     binary file to create.")

    opts.add_option("-r", "--recsep", action="store_true", dest="recsep",
                   default=False,
                   help="<bool>     add a record separator for Linux testing.")

    opts.add_option("--uncompile", action="store_true", dest="uncompile",
                   default=False,
                   help="<bool>     pretty-print the bin file [fakemessage.bin]")

    opts.add_option("-v", "--verbose", action="store_true", dest="verboseflag",
                   default=False,
                   help="<bool>     be verbose about work.")

    (options, args) = opts.parse_args()

# Open a file and transliterate the ASCII image into 'binary' <RS>.. records
# Given a stream connection, take regular text as payload in create packets
# and accept packets and return the payload
# For testing, given a 'file' of regular payloads produce a bin file of packets


    for filename in args:                           # PDB-DEBUG
        bf   = open(filename,'r')
        jc   = FlexJSONCompiler(bf,options=options) # PDB -DEBUG
        jc.compile()                                # PDB-DEBUG
