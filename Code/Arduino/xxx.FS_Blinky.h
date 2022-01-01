/*****************************************************************************
*
*  FlexBlinky.h -- Blinky Class

*
* $Revision$
*   $Log$
*
*
*   Tue Apr 20 21:45:37 2021
*
*****************************************************************************/
#ifndef __FS_BLINKY__h__
#define __FS_BLINKY__h__
#ifdef __REGRESSION__
   #include <iostream>
#endif
// INIT FIX THESE LINES
#include <string>
#include "Patron.h"

using namespace std;

/******************************************************************************
* FS_Blinky Control the Nano 33 BLE RGB Diode.
*
******************************************************************************/
class FS_Blinky : public Patron
{

private:

   string name            ; // This instances name
   int    pin             ; // Pin assigned to the led
   int    ontime          ; // The on time for the led
   int    offtime         ; // The on time for the led
   int    pause           ; // time to delay between an on/off cycle
   int    count           ; // count of cycles to perform
   int    status          ; // the state default 
   int    returnrequested ; // What to do when Process finishes


public:

//******************************** FS_Blinky Constructors **********************

   FS_Blinky() :
         name("Unknown"),
         pin(0),
         ontime(0),
         offtime(0),
         pause(0),
         count(0)
            {} // FS_Blinky memberwise X::X(): v(0) constructor

   /*******************************************************************
   *  FS_Blinky::FS_Blinky Instantiate fully from main or elsewhere
   *  
   *******************************************************************/
   FS_Blinky( string pname, int ppin, int pontime, int pofftime,
      int ppause, int pcount ) :
         pin(ppin),
         ontime(pontime),
         offtime(pofftime),
         pause(ppause),
         count(pcount)
      {
         name    = "Unknown";
         pin     = ppin;     
         ontime  = pontime;  
         offtime = pofftime; 
         pause   = ppause;   
         count   = pcount;   
      } // FS_Blinky parameterized memberwise constructor X::X(...) : ... { ... }

   /*******************************************************************
   *  FS_Blinky::FS_Blinky Instantiate as a copy of ref
   *  
   *******************************************************************/
   FS_Blinky(const FS_Blinky &ref)
      {
         name    = ref.name;                                           // INIT
         pin     = ref.pin;                                            // INIT
         ontime  = ref.ontime;                                         // INIT
         offtime = ref.offtime;                                        // INIT
         pause   = ref.pause;                                          // INIT
         count   = ref.count;                                          // INIT
      } // FS_Blinky copy constructor X::X(const &X)

   //********************************FS_Blinky's Interface ***********************

public:

   void Process(const string &);
   void report(string &);
   void reset();
   inline int Validp() const { return 0;}   // INIT  validity predicate
}; // FS_Blinky

#endif


/* *INDENT-OFF* */
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
       ("status")           "Maintain the status condition"
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
         ("void"  "ThinkFast"   "()"   "Get permission for fast interrupt check. FS_Dispatcher")
         ("void"  "Report"      "(string &ref)"   "Get permission for fast interrupt check. FS_Dispatcher")
         ("void"  "Process"     "(string &ref)"   "Get permission for fast interrupt check. FS_Dispatcher")
         ("void"  "Inventory"   "(string &ref)" "Load string with the inventory info")
         ("void"  "reset"       "()"   "Reset -- whatever that may mean.")
      )
   )


)
#endif
/*  *INDENT-ON*  */
