#ifndef __FS_TIMEDSWITCH.H__h__
#define __FS_TIMEDSWITCH.H__h__
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

(Classdef FS_TimedSwitch
  "Headermessage Put cursor on the ( of (Classdef... and M-x class-compile"


   (variable (access private) (attributes dialog encapsulate persistent stream) ; static
    ("" (
       ("duration"   "requested duration" )
       ("timeleft"   "amount time left fro ThinkFast" )
       ("status"     "on = 1, off = 0" )
    )))


   (variable (access private) (attributes dialog encapsulate persistent stream) ; static
    ("string" (
       ("name"   "" )
    )))


   (variable (access private) (attributes dialog encapsulate persistent stream) ; static
    ("" (
       (""   "" )
    )))


   ;(header      t)     ; nil for second/subsequent class insertions.
   ;(equality    t)     ; operator != ==
   ;(comparison  t)     ; operator > >= < <= 
   ;(arithmetic  t)     ; operators + - * /
   ;(destructor  t)     ; ~X 
   ;(freepool    t)     ; Manage used objects from a pool.
   ;(iterator    t)     ; Add X<TTT> conainer operations.
   (debug       t)     ; Stuff to assist with debuging.
   ;(dialog      t)     ; Will this class use a dialog to manage members?
   ;(assignment  t)     ; operator =
   (memberwise  t)     ; X::X() : v(), v() ...
   (encapsulate t)     ; Get/Set routines for variables
   (friendio    t)     ; friend [io]stream &operator [<<,>>]
   (persistence t)     ; (Un)Marshall routines.
   ;(cpp         nil)   ; nil or name xxx of xxx.cpp. (cpp xxx).
   ;(html        nil)   ; Generate a documentation .html file if possible.

   ;(man         nil)   ; Generate a documentation .html file if possible.



   (interface (access public) ; (attributes virtual pure)
      (
         (""  ""   "()"   "")
      )
   )



)
#endif
/*  *INDENT-ON*  */
