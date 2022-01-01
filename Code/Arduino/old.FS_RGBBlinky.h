#ifndef __FS_RGBLINKY.H__h__
#define __FS_RGBLINKY.H__h__
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

(Classdef FS_RGBlinky
  "Contol the RGB Diode (internal part)"


   (variable (access private) (attributes dialog encapsulate persistent stream)
    ("int" (
       ("ontime"    "Onetime for a blink" )
       ("offtime"   "Offtime for a blink, rate=0" )
       ("rate"      "additinoal gap between blinks" )
       ("count"     "how many, 0-> forever" )
       ("state"     "current state 1=0n, 0=off" )
       ("redval",   "The amount of red   0..255")
       ("blueval",  "The amount of blue  0..255")
       ("greenval", "The amount of green 0..255")
    )))

   (variable (access private) (attributes dialog encapsulate persistent stream)
    ("string" (
       ("name"   "The name of this instance" )
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
 (cpp         FS_RGBlinky)   ; nil or name xxx of xxx.cpp. (cpp xxx).
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
