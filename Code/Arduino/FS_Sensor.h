#ifndef __FS_SENSOR.H__h__
#define __FS_SENSOR.H__h__
#ifdef __REGRESSION__
   #include <iostream>
#endif
// INIT FIX THESE LINES
#include <string>  // INIT
#include <map>     // INIT
#include <vector>  // INIT
#include <deque>   // INIT
#include <ccytpe>  // INIT


using namespace std;

//(class-insert)
/* *INDENT-OFF* */
#if 0

(Classdef FS_Sensor
  "Headermessage Put cursor on the ( of (Classdef... and M-x class-compile"




   (variable (access private) (attributes dialog encapsulate persistent stream)
    ("" (
       (""   "" )
    )))


   (variable (access private) (attributes dialog encapsulate persistent stream)
    ("" (
       (""   "" )
    )))


   (variable (access private) (attributes dialog encapsulate persistent stream)
    ("" (
       (""   "" )
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
