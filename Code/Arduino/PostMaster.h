/*****************************************************************************
*
*  PostMaster.h -- Headermessage Put cursor on the ( of (Classdef... and M-x class-compile
* (compile "g++ -c PostMaster.h")
*
*****************************************************************************/
#ifndef __POSTMASTER_H__
#define __POSTMASTER_H__

#ifdef __REGRESSION__
   #include <iostream>
#endif
// INIT FIX THESE LINES
#include <string>  // INIT
#include <map>     // INIT

#include "Patron.h"

/*****************************************************************************
*
*  PostMaster -- Headermessage Put cursor on the ( of (Classdef... and M-x class-compile
*
*****************************************************************************/
class PostMaster
{

private:

   string                name   ; // The name of my postoffice (instrument's name exactly)
   map<Patron *, string> patrons; // Map the patron to the name
   map< string,Patron *> routes ; // Given the name, route the 


public:

//******************************** PostMaster Constructors **********************

   PostMaster(const string &ppname) :
         name(ppname)
            {} // PostMaster memberwise X::X(): v(0) constructor

   PostMaster(const PostMaster &ref)
      {
         name    = ref.name;                                           // INIT
         patrons = ref.patrons;                                        // INIT
         routes  = ref.routes;                                         // INIT
      } // PostMaster copy constructor X::X(const &X)

   //********************************PostMaster's Interface ***********************

public:

   void register(Patron *patron);
   void Open();
   void Mail(string jsonstr);
   inline int Validp() const { return 0;}   // INIT  validity predicate
}; // PostMaster

/* *INDENT-OFF* */
#if 0

(Classdef "PostMaster"
  "Headermessage Put cursor on the ( of (Classdef... and M-x class-compile"

   (variable (access private) (attributes dialog encapsulate persistent stream)
    ("string" (
       ("name"   "The name of my postoffice (instrument's name exactly)" )
    )))


   (variable (access private) (attributes dialog encapsulate persistent stream)
    ("map<Patron *, string>" (
       ("patrons"   "Map the patron to the name" )
    )))


   (variable (access private) (attributes dialog encapsulate persistent stream)
    ("map< string,Patron *>" (
       ("routes"   "Given the name, route the " )
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
         ("void"  "register"      "(Patron *patron)"  "Dig name etc from the patron.")
         ("void"  "Open"          "()"                "Infinite loop -- open for business.")
         ("void"  "Mail"          "(string jsonstr)"  "Send a message.")
      )
   )

)
#endif
/*  *INDENT-ON*  */
#endif

