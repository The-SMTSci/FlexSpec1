#ifndef __FS_SERIALPORT__h__
#define __FS_SERIALPORT__h__

#ifdef __REGRESSION__
   #include <iostream>
#endif

#include <string>

using namespace std;

/*****************************************************************************
*
*  FS_SerialPort -- A class to manage SerialPorts
*
*****************************************************************************/
class FS_SerialPort
{

private:

   string name  ; // Internal logical name of the port
   string device; // Hardware Device 'name' of the port
   int    baud  ; // serial port rate
   int    start ; // count start bits
   int    bits  ; // word size in bits
   int    stop  ; // count stop bits
   int    parity; // parity bits if used


public:

//******************************** FS_SerialPort Constructors **********************

   FS_SerialPort(const string &pname,
                 const string &pdevice = string("/dev/tty0"),
                 int pbaud = 115800,
                 int pstart = 1,
                 int pbits  = 8,
                 int stop   = 0,
                 int parity = 0) :
         name(pname),
         device(pdevice),
         baud(pbaud),
         start(pstart),
         bits(pbits),
         stop(stop),
         parity(parity)
            {} // FS_SerialPort memberwise X::X(): v(0) constructor

   FS_SerialPort(const FS_SerialPort &ref)
      {
         name   = ref.name;
         device = ref.device;
         baud   = ref.baud;
         start  = ref.start;
         bits   = ref.bits;
         stop   = ref.stop;
         parity = ref.parity;
      } // FS_SerialPort copy constructor X::X(const &X)

   //********************************FS_SerialPort's Interface ***********************

public:

   void ThinkFast();
   void Process(string &ref);
   void Report(string &ref);
   void Inventory(string &ref);
   void reset();
   FS_SerialPort &setname   (const string &newname) { name = newname;  return *this;}
   FS_SerialPort &setdevice (const string &newdev)  { device = newdev; return *this;}

   inline int Validp() const { return 0;}   // INIT  validity predicate
}; // FS_SerialPort

#endif

/*  *INDENT-OFF*  */

#if 0

(Classdef "FS_SerialPort"
  "A class to manage SerialPorts"

   (variable (access private) (attributes dialog encapsulate persistent stream)
    ("string" (
       ("name"     "Internal logical name of the port" )
       ("device"   "Hardware Device 'name' of the port" )
    )))

   (variable (access private) (attributes dialog encapsulate persistent stream)
    ("int" (
       ("baud"    "serial port rate" )
       ("start"   "count start bits" )
       ("bits"    "word size in bits" )
       ("stop"    "count stop bits" )
       ("parity"  "parity bits if used" )
    )))


   (header      t)     ; nil for second/subsequent class insertions.
   ;(equality    t)     ; operator != ==
   ;(comparison  t)     ; operator > >= < <=
   ;(arithmetic  t)     ; operators + - * /
   ;(destructor  t)     ; ~X
   ;(freepool    t)     ; Manage used objects from a pool.
   ;(iterator    t)     ; Add X<TTT> conainer operations.
   ;(debug       t)     ; Stuff to assist with debuging.
   ;(dialog      t)     ; Will this class use a dialog to manage members?
   ;(assignment  t)     ; operator =
   ;(memberwise  t)     ; X::X() : v(), v() ...
   ;(encapsulate t)     ; Get/Set routines for variables
   ;(friendio    t)     ; friend [io]stream &operator [<<,>>]
   ;(persistence t)     ; (Un)Marshall routines.
   (cpp         FS_SeriaoPort)   ; nil or name xxx of xxx.cpp. (cpp xxx).
   ;(html        nil)   ; Generate a documentation .html file if possible.

   ;(man         nil)   ; Generate a documentation .html file if possible.

   (interface (access public) ; (attributes virtual pure)
      (
         ("void"             "ThinkFast"   "()"                                        "Get permission for fast interrupt check. FS_Dispatcher")
         ("void"             "Process"     "(string &ref)"                             "Get permission for fast interrupt check. FS_Dispatcher")
         ("void"             "Report"      "(string &ref)"                             "Get permission for fast interrupt check. FS_Dispatcher")
         ("void"             "Inventory"   "(string &ref)"                             "Load string with the inventory info")
         ("void"             "reset"       "()"                                        "Reset -- whatever that may mean.")
         ("FS_SerialPort &"  "setname"     "(const string &newname)"                   "After copy operator set the new name")
         ("FS_SerialPort &"  "setdevice"   "(const string &newdev)"                    "After copy operator set the new device")
         ("int"              "open"        "(const string &pathname, int flags, mode_t mode = 0x444)"  "level 2 io")
         ("int"              "close"       "(int fd)"                                  "level 2 io")
         ("ssize_t"          "read"        "(int fd, string &buf, size_t count)"       "level 2 io")
         ("ssize_t"          "write"       "(int fd, const string &buf, size_t count)" "level 2 io")
         ("int"              "ioctl"       "(int fd, unsigned long request, ...)"      "level 2 io")
      )
   )

)
#endif
/*  *INDENT-ON*  */

/******************************************************************************
* 
* https://datasheets.raspberrypi.org/bcm2835/bcm2835-peripherals.pdf
* 
* Raspberry PI
* NAME    Type
* UART0   PL011        /dev/ttyAMA0
* UART1   mini UART    /dev/ttyS0 
* UART2   PL011      
* UART3   PL011      
* UART4   PL011      
* UART5   PL011      
* 
* Linux device    Description               
* /dev/ttyS0      mini UART                     
* /dev/ttyAMA0    first PL011 (UART0)       
* /dev/serial0    primary UART              
* /dev/serial1    secondary UART            
* 
* Note: /dev/serial0 and /dev/serial1 are symbolic links which point 
* to either /dev/ttyS0 or /dev/ttyAMA0.
* 
* 
* ---------------------------------
* 
* https://scribles.net/setting-up-uart-serial-communication-between-raspberry-pis/
*
* /boot/config.tx
* add
* # Enable UART
* enable_uart=1
* Remove “console=serial0,115200”, then save the file.
* --------------------------------------------------
* Rx 14    Tx 15
* 
* We are starved for pins, so in-band flow delivery it is.
* 
* 
* GPIO#     2nd Function PIN         PIN  2nd     Function    GPIO#
*             +3.3 V      1           2           +5 V        
* 2           SDA1 (I2C)  3           4           +5 V        
* 3           SCL1 (I2C)  5           6           GND         
* 4           GCLK        7           8           TXD0 (UART) 14
*             GND         9           10          RXD0 (UART) 15
* 17          GEN0        11          12          GEN1        18
* 27          GEN2        13          14          GND         
* 22          GEN3        15          16          GEN4        23
*             +3.3 V      17          18          GEN5        24
* 10          MOSI (SPI)  19          20          GND         
* 9           MISO (SPI)  21          22          GEN6        25
* 11          SCLK (SPI)  23          24          CE0_N (SPI) 8
*             GND         25          26          CE1_N (SPI) 7
* -----------------------------------------------------------------------------
*                (Pi 1 Models A and B stop here)
* -----------------------------------------------------------------------------
* 0           ID_SD (I2C) 27                      28          ID_SC (I2C) 1
* 5           N/A         29          30          GND         
* 6           N/A         31          32          N/A         12
* 13          N/A         33          34          GND         
* 19          N/A         35          36          N/A         16
* 26          N/A         37          38          Digital IN  20
*             GND         39          40          Digital OUT 21
*  
* 
* 
* 
* 
* 
*
******************************************************************************/
