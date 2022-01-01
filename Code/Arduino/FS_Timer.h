/******************************************************************************
* FS_Timer.h -- hack to use a timer module as a tiny RTC
* 
* The idea is to have a RTC that runs through say every 100-200 ms.
* Each Patron implements a virtual function to be called from the
* Dispatcher that pledges to do what it needs to do.
* 
* 
* 
* 
* 
* 
* 
* 
* 
* 
* 
*
******************************************************************************/

#ifndef __FS_TIMER.H__h__
#define __FS_TIMER.H__h__#ifdef __REGRESSION__
   #include <iostream>
#endif
// INIT FIX THESE LINES
#include <string>  // INIT
#include <map>     // INIT
#include <vector>  // INIT
#include <deque>   // INIT
#include <ccytpe>  // INIT

# From https://content.arduino.cc/assets/Nano_BLE_MCU-nRF52840_PS_v1.1.pdf

#define  TIMER1 0x40009000 // TIMER1 timer instance has 4 CC registers (CC[0..3])
#define  TIMER2 0x4000A000 // TIMER2 timer instance has 4 CC registers (CC[0..3])
#define  TIMER3 0x4001A000 // TIMER3 timer instance has 6 CC registers (CC[0..5])
#define  TIMER4 0x4001B000 // TIMER4 timer instance has 6 CC registers (CC[0..5


#define TASKS_START      0x000     // Start Timer
#define TASKS_STOP       0x004     // Stop Timer
#define TASKS_COUNT      0x008     // Increment Timer (Counter mode only)
#define TASKS_CLEAR      0x00C     // Clear time
#define TASKS_SHUTDOWN   0x010     // Shut down timer Deprecated

#define TASKS_CAPTU_0    0x040     // Capture Timer value to CC[0] register
#define TASKS_CAPTU_1    0x044     // Capture Timer value to CC[1] register
#define TASKS_CAPTU_2    0x048     // Capture Timer value to CC[2] register
#define TASKS_CAPTU_3    0x04C     // Capture Timer value to CC[3] register
#define TASKS_CAPTU_4    0x050     // Capture Timer value to CC[4] register
#define TASKS_CAPTU_5    0x054     // Capture Timer value to CC[5] register

#define EVENTS_COMPA_0   0x140     // Compare event on CC[0] match
#define EVENTS_COMPA_1   0x144     // Compare event on CC[1] match
#define EVENTS_COMPA_2   0x148     // Compare event on CC[2] match
#define EVENTS_COMPA_3   0x14C     // Compare event on CC[3] match
#define EVENTS_COMPA_4   0x150     // Compare event on CC[4] match
#define EVENTS_COMPA_5   0x154     // Compare event on CC[5] match

#define SHORTS           0x200     // Shortcuts between local events and tasks
#define INTENSET         0x304     // Enable interrupt
#define INTENCLR         0x308     // Disable interrupt
#define MODE             0x504     // Timer mode selection
#define BITMODE          0x508     // Configure the number of bits used by the TIMER
#define PRESCALER        0x510     // Timer prescaler register
#define CC_0             0x540     // Capture/Compare register 0
#define CC_1             0x544     // Capture/Compare register 1
#define CC_2             0x548     // Capture/Compare register 2
#define CC_3             0x54C     // Capture/Compare register 3
#define CC_4             0x550     // Capture/Compare register 4
#define CC_5             0x554     // Capture/Compare register 5

#define TIMERWIDTH16         0     // 16 bits used by the TIMER
#define TIMERWIDTH08         1     // 08 bits used by the TIMER
#define TIMERWIDTH24         2     // 24 bits used by the TIMER
#define TIMERWIDTH32         3     // 32 bits used by the TIMER

// LFCLK = 32.768 Hz

#define DIV_1                0     //  Divide by 1 (16 MHz)  pg. 269
#define DIV_2                1     //  Divide by 2 (8 MHz)
#define DIV_4                2     //  Divide by 4 (4 MHz)
#define DIV_8                3     //  Divide by 8 (2 MHz)
#define DIV_16               4     //  Divide by 16 (1 MHz)
#define DIV_32               5     //  Divide by 32 (500 kHz)
#define DIV_64               6     //  Divide by 64 (250 kHz)
#define DIV_128              7     //  Divide by 128 (125 kHz)

// register offsets, not sure of base address TODO 
#define INTENSET         0x304     //  Enable interrupt
#define INTENCLR         0x308     //  Disable interrupt


using namespace std;

/******************************************************************************
* The FS_Timer, up to 4 timers may be specified by the template
* values of TIMER1, TIMER2, TIMER3, or TIMER4
******************************************************************************/

template <unsigned int TIMERID,            // Base address for this thingy in the machine
          unsigned int PRESCALERVALUE,     // A prescaler divide-by from clock DIV_n from above
          unsigned int MODESETTING>        // Mode  [0..3] per TIMERWIDTHnn above
class FS_Timer 
{
  int prescaler = PRESCALER;
  int mode;

  inline void Start()    { static_cast<int *>(TIMERID + TASKS_START)     = 1; }
  inline void Stop()     { static_cast<int *>(TIMERID + TASKS_STOP)      = 1; }   
  inline void Count()    { static_cast<int *>(TIMERID + TASKS_COUNT)     = 1; }   
  inline void Clear()    { static_cast<int *>(TIMERID + TASKS_CLEAR)     = 1; }   
  inline void Shutdown() { static_cast<int *>(TIMERID + TASKS_SHUTDOWN)  = 1; } 

};



#endif
//(class-insert)
/* *INDENT-OFF* */
#if 0

(Classdef FS_Timer
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
         (""  ""   "()"   "")
      )
   )



)
#endif
/*  *INDENT-ON*  */
