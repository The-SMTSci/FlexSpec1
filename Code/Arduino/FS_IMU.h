#ifndef __FS_IMU.H__h__
#define __FS_IMU.H__h__
#ifdef __REGRESSION__
   #include <iostream>
#else   
   #include <Arduino_LSM9DS1.h>
#endif

/*****************************************************************************
*
*  FS_IMU -- Headermessage Put cursor on the ( of (Classdef... and M-x class-compile
*
*****************************************************************************/
class FS_IMU : Patron
{

private:

   float xval; // X axis -1. .. 1.0
   float yval; // Y axis -1. .. 1.0
   float zval; // Z axis -1. .. 1.0


public:

//******************************** FS_IMU Constructors **********************

   FS_IMU(const string &pname,                        // I have to have a unique name
          Postmaster   &ppostmaster,                  // I have to know where the mailbox is
          int           pdispatchinterval = 0, 
      :
         Patron(ppostmaster,pname,pdispatchinterval,string("0.0.1")),  // Version is HARDWIRED!
         xval(0),                                     // Will be filled in on Process
         yval(0),                                     // Will be filled in on Process
         zval(0)                                      // Will be filled in on Process
      {
         mailbox.register(dynamic_cast<Patron *>(this);
      } // FS_IMU memberwise X::X(): v(0) constructor

   FS_IMU(const FS_IMU &ref)
      {
         xval = ref.xval;
         yval = ref.yval;
         zval = ref.zval;
      } // FS_IMU copy constructor X::X(const &X)

   //********************************FS_IMU's Interface ***********************

   void read();
public:

   void Process(const string &ref);
   void Report(const string &ref);
   inline int Validp() const { return 0;}   // INIT  validity predicate

}; // FS_IMU


using namespace std;

//(class-insert)
/* *INDENT-OFF* */
#if 0

(Classdef "FS_IMU"
  "Headermessage Put cursor on the ( of (Classdef... and M-x class-compile"


   (variable (access private) (attributes dialog encapsulate persistent stream)
    ("float" (
       ("xval"   "X axis -1. .. 1.0" )
       ("yval"   "Y axis -1. .. 1.0" )
       ("zval"   "Z axis -1. .. 1.0" )
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
   (cpp         FS_Imu)   ; nil or name xxx of xxx.cpp. (cpp xxx).
   ;(html        nil)   ; Generate a documentation .html file if possible.

   ;(man         nil)   ; Generate a documentation .html file if possible.


   (interface (access private) ; (attributes virtual pure)
      (
         ("void"  "read"   "()"   "IMU.readAcceleration(x, y, z)")
      )
   )

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
