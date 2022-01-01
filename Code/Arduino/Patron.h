/*****************************************************************************
*
*  Patron.h -- Headermessage Put cursor on the ( of (Classdef... and M-x class-compile

*
* $Revision$
*   $Log$
*
*
*   Thu Apr 29 12:42:29 2021
*
*****************************************************************************/
#ifndef __Patron_H__
#define __Patron_H__

#ifdef __REGRESSION__
   #include <iostream>
#endif

using namespace std;


#ifdef __REGRESSION__
   #include <iostream>
#endif
// INIT FIX THESE LINES
#include <string>  // INIT

#include "PostMaster.h"

/*****************************************************************************
*
*  Patron -- Headermessage Put cursor on the ( of (Classdef... and M-x class-compile
*  Virtual class with common details.
*  Mixed Metaphor
*****************************************************************************/
class Patron
{

protected:

   PostMaster  &mailbox        ; // Need to know where my 'Postmaster' is.
   string      name            ; // The name of the Patron
   string      version         ; // The version of this patron
   string      lineitem        ; // The line-item description this instance default=name+version
   int         dispatchinterval; // How often to let me ThinkFast default = 0


public:

//******************************** Patron Constructors **********************

   Patron(PostMaster   &postmaster,
          const string &pname, 
          const string &pversion = string("0.0.1"), 
          int          pdispatchinterval = 0) :
         mailbox(postmaster),
         name(pname),
         dispatchinterval(pdispatchinterval),
         version(pversion),
         lineitem(pname+" "+pversion)
            {} // Patron memberwise X::X(): v(0) constructor

   Patron(const Patron &ref)
      {
         name             = ref.name;
         version          = ref.version;
         lineitem         = ref.lineitem;
         dispatchinterval = ref.dispatchinterval;
      } // Patron copy constructor X::X(const &X)

   //********************************Patron's Interface ***********************


    virtual void ThinkFast()                  = 0;  // Something needed done fast
    virtual void Report(string &report)       = 0;  // Return the state
    virtual void Process(string &jsoncommand) = 0;  // given a state, match it
    virtual void Inventory(string &report)    = 0;  // return the details of the widget
    virtual void Reset()                      = 0;  // reset to initial state
    inline  int  Validp() const { return 0;}        // INIT  validity predicate

}; // Patron

#endif

//(class-insert)
/* *INDENT-OFF* */
#if 0

(Classdef "Patron"
  "Headermessage Put cursor on the ( of (Classdef... and M-x class-compile"

   (variable (access protected) (attributes dialog encapsulate persistent stream)
    ("string" (
       ("name"    "The name of the Patron" )
       ("version" "The version of this patron" )
    )))


   (variable (access private) (attributes dialog encapsulate persistent stream)
    ("int" (
       ("dispatchinterval"   "How often to let me ThinkFast default = 0" )
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
   ;(cpp         nil)   ; nil or name xxx of xxx.cpp. (cpp xxx).
   ;(html        nil)   ; Generate a documentation .html file if possible.

   ;(man         nil)   ; Generate a documentation .html file if possible.


   (interface (access public) (attributes virtual pure)
      (
         ("void"  "ThinkFast"   "()"                    "Get permission for fast interrupt check. FS_Dispatcher")
         ("void"  "Report"      "(string &report)"      "Add my stuff to the developing report in prose.")
         ("void"  "Process"     "(string &jsoncommand)" "Given a JSON string, act on the key:values")
         ("void"  "Inventory"   "(string &report)"      "Add my inventory info to developing report")
         ("void"  "reset"       "()"                    "Reset -- whatever that may mean.")
      )
   )

)
#endif
/*  *INDENT-ON*  */
