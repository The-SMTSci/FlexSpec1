/*  *INDENT-ON*  */
/*****************************************************************************
*
*  FS_Blinky.h -- Blinky Class
*
* $Revision$
*   $Log$
*
*
*   Sun Jul 11 14:01:20 2021
*
*****************************************************************************/
#ifndef __FS_Blinky_H__
#define __FS_Blinky_H__

#ifdef __REGRESSION__
   #include <iostream>
#endif
// INIT FIX THESE LINES
#include <string>
#include "Patron.h"
#include "Postmaster.h"

using namespace std;

/*****************************************************************************
*
*  FS_Blinky -- Blinky Class  NANO pin is 13u
*
*****************************************************************************/
class FS_Blinky : public Patron
{

private:

   int    pin                          ; // Pin assigned to the led
   int    ontime                       ; // The on time for the led
   int    offtime                      ; // The on time for the led
   int    pause                        ; // Time to delay between an on/off cycle
   int    count                        ; // Count of cycles to perform
   int    status                       ; // Maintain active/inactive 
   int    returnrequested              ; // What to do when Process finishes

public:

//******************************** FS_Blinky Constructors **********************

   FS_Blinky(const string &pname,                      // I have to have a unique name
             Postmaster   &ppostmaster,                // I have to know where the mailbox is
             unsigned int  ppin              =   13,   // Arduino Nano 33 BLE Sense LED pin no.
             int           pdispatchinterval =    0,   // I'm a blinky I will not fast release
             unsigned int  ppon              =  500,   // ms of on time
             unsigned int  poff              =  500,   // ms of off time
             unsigned int  ppause            = 1000    // pause between on,off cycles.
           :
         Patron(ppostmaster,pname,pdispatchinterval,string("0.0.1")),  // Version is HARDWIRED!
         pin             (ppin),
         ontime          (ppon),
         offtime         (poff),
         pause           (ppause),
         count           (0),
         status          (0),
         returnrequested (0)
      {
         mailbox.register(dynamic_cast<Patron *>(this), name);
      } // FS_Blinky memberwise X::X(): v(0) constructor

   // Copy constructor.
   FS_Blinky(const FS_Blinky &ref) :
     Patron(ref.name, ref.dispatchinterval, ref.version)
      {
         pin                           = ref.pin;
         ontime                        = ref.ontime;
         offtime                       = ref.offtime;
         pause                         = ref.pause;
         count                         = ref.count;
         status                        = ref.status;
         returnrequested               = ref.returnrequested;
         
         mailbox.register(dynamic_cast<Patron *>(this);
      
      } // FS_Blinky copy constructor X::X(const &X)

   //********************************FS_Blinky's Interface ***********************

public:

   void       ThinkFast();
   void       Report(string &ref);
   void       Process(string &ref);
   void       Inventory(string &ref);
   void       reset();
   inline int Validp() const { return 0;}   // INIT  validity predicate

}; // FS_Blinky

#endif

/* *INDENT-OFF* */
// The emacs class here is out of date. 2021-07-29T23:56:34-0600
#if 0

(Classdef "FS_Blinky"
  "Blinky Class"

   (variable (access private) (attributes dialog encapsulate persistent stream)
    ("string" (
       ("name"   "This instances name" )
    )))

   (variable (access private) (attributes dialog encapsulate persistent stream)
    ("int" (
       ("pin"   "Pin assigned to the led" )
       ("ontime"            "The on time for the led" )
       ("offtime"           "The on time for the led" )
       ("pause"             "Time to delay between an on/off cycle" )
       ("count"             "Count of cycles to perform" )
       ("status"            "Maintain the status condition")
       ("returnrequested"   "What to do when Process finishes")
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
   (cpp         FS_Blinky)   ; nil or name xxx of xxx.cpp. (cpp xxx).
   ;(html        nil)   ; Generate a documentation .html file if possible.

   ;(man         nil)   ; Generate a documentation .html file if possible.

   (interface (access public) ; (attributes virtual pure)
      (
         ("void"              "ThinkFast"   "()"                      "Get permission for fast interrupt check. FS_Dispatcher")
         ("void"              "Process"     "(string &ref)"           "Get permission for fast interrupt check. FS_Dispatcher")
         ("void"              "Report"      "(string &ref)"           "Get permission for fast interrupt check. FS_Dispatcher")
         ("void"              "Inventory"   "(string &ref)"           "Load string with the inventory info")
         ("void"              "reset"       "()"                      "Reset -- whatever that may mean.")
      )
   )


)
#endif
