

/*****************************************************************************
*
*  FS_Switch.h -- Report on the status of a switch.
*
* (compile "g++ -c FS_Switch.h")
*
*   Fri Jul 30 15:09:15 2021
*
*****************************************************************************/
#ifndef __FS_Switch_H__
#define __FS_Switch_H__

#ifdef __REGRESSION__
   #include <iostream>
#endif
// INIT FIX THESE LINES
#include <string> 
#include "PostMaster.h"
#include "Patron.h"

using namespace std;

/*****************************************************************************
*
*  FS_Switch -- Report on the status of a switch.
*
*****************************************************************************/
class FS_Switch : public Patron
{

private:

   int pin   ; // Pin to use
   int state ; // Current state
   int status; // 


public:

//******************************** FS_Switch Constructors **********************

   FS_Switch( const string &pname,                      // I have to have a unique name
              PostMaster   &ppostmaster,                // I have to know where the mailbox is
              int           pdispatchinterval =    0    // I'm a switch I will not fast release
            ) :
         Patron(ppostmaster,pname,pdispatchinterval,string("0.0.1")),  // Version is HARDWIRED!
         pin(0),
         state(0),
         status(0)
      {
         mailbox.register(dynamic_cast<Patron *>(this);
      } // FS_Switch memberwise X::X(): v(0) constructor

   FS_Switch(const FS_Switch &ref)
      {
         pin    = ref.pin; 
         state  = ref.state;
         status = ref.status;
         mailbox.register(dynamic_cast<Patron *>(this);
      } // FS_Switch copy constructor X::X(const &X)

   //********************************FS_Switch's Interface ***********************

   FS_Switch &SetPin(int ppin) { pin = ppin; return *this; }

public:

   void ThinkFast()  {};                   // I'm a blinky I will not fast release
   void Report(string &ref);
   void Process(string &ref);
   void Inventory(string &ref);
   void Reset();
   int  Validp() const;
   inline int Validp() const { return 1;}  // Switch is always valid.
}; // FS_Switch

#endif


//(class-insert)
/* *INDENT-OFF* */
#if 0

(Classdef "FS_Switch"
  "Report on the status of a switch."

   (variable (access private) (attributes dialog encapsulate persistent stream)
    ("int" (
       ("pin"      "Pin to use" )
       ("state"    "Current state" )
       ("status"   "" )
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
   (cpp         nil)   ; nil or name xxx of xxx.cpp. (cpp xxx).
   ;(html        nil)   ; Generate a documentation .html file if possible.

   ;(man         nil)   ; Generate a documentation .html file if possible.



   (interface (access public) ; (attributes virtual pure)
      (
         ("void"  "ThinkFast"   "()"   "Get permission for fast interrupt check. FS_Dispatcher")
         ("void"  "Report"      "(string &ref)"   "Get permission for fast interrupt check. FS_Dispatcher")
         ("void"  "Process"     "(string &ref)"   "Get permission for fast interrupt check. FS_Dispatcher")
         ("void"  "Inventory"   "(string &ref)" "Load string with the inventory info")
         ("void"  "Reset"       "()"   "Reset -- whatever that may mean.")
         ("int"   "Validp"      "() const"   " class is in a valid state")
      )
   )



)
#endif
/*  *INDENT-ON*  */
