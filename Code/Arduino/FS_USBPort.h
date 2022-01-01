"/etc/udev/rules.d" called "99-usb-serial.rules" and put a line in there like so:



//(class-insert)
/* *INDENT-OFF* */
#if 0

(Classdef "FS_USBPort"
  "A class to manage USBPorts"

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
         ("void"             "ThinkFast"   "()"                      "Get permission for fast interrupt check. FS_Dispatcher")
         ("void"             "Process"     "(string &ref)"           "Get permission for fast interrupt check. FS_Dispatcher")
         ("void"             "Report"      "(string &ref)"           "Get permission for fast interrupt check. FS_Dispatcher")
         ("void"             "Inventory"   "(string &ref)"           "Load string with the inventory info")
         ("void"             "reset"       "()"                      "Reset -- whatever that may mean.")
         ("FS_USBPort &"  "setname"     "(const string &newname)" "After copy operator set the new name")
         ("FS_USBPort &"  "setdevice"   "(const string &newdev)"  "After copy operator set the new device")
      )
   )

)


)
#endif
/*  *INDENT-ON*  */
