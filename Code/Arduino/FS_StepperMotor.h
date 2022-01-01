/******************************************************************************
* SAS_NA1_3D_Spectrograph/FS1Code-V1/tmp/FS_StepperMotor.h
*
******************************************************************************/
#ifndef __FS_STEPPERMOTOR_H__
#define __FS_STEPPERMOTOR_H__

using namespace std;

#ifndef __REGRESSION__
#define ARDUINO 101
#include <Arduino.h>
#include <Stepper.h>        // Arduino library for motors.
#endif

#include "PostMaster.h"     // support system inter-communication
#include "Patron.h"         // Classes responding to communiques.
#include "FS_Dispatcher.h"  // template function for dispatchers for various things.

#include <string>


/*****************************************************************************
* Stepper(steps, pin1, pin2)
* Stepper(steps, pin1, pin2, pin3, pin4)
* setSpeed(rpm)
* step(steps)
*****************************************************************************/
/*****************************************************************************
* Handle the steps per revolution to degrees conversion etc.
*****************************************************************************/
class StepperMotor // : virtual patron      string     name;
{
private:
  int   steps_Revolution;        // steps per revolution of the motor
  int   gear_ratio_numerator;
  int   gear_ratio_denominator;
  float step_angle;              // float from spec.

public:
  StepperMotor(int   psteps_Revolution         = 0,
               int   pgear_ratio_numerator     = 0,
               int   pgear_ratio_denominator   = 0,
               float pstep_angle               = 0.0) :
                  steps_Revolution(pgear_ratio_numerator),
                  gear_ratio_numerator(pgear_ratio_denominator),
                  gear_ratio_denominator(pgear_ratio_denominator),
                  step_angle(pstep_angle)
         {}

  // Pure virtual functions
  virtual void setSpeed(int)       = 0;
  virtual void reset()             = 0;
  virtual bool validp()            = 0;
  virtual void report(string &)    = 0;
  virtual void ThinkFast()         = 0;  // something to do on timer tick.

}; // StepperMotor

/******************************************************************************
* Motor28BYJ48 - Implement a stepper like FS1 testing has used.
*  It inherits a generic StepperMotor definition, has to add matching
*  functions.
*  Added some basics like min/max values to impose some limit tests
*  The pins are initialized to bad things.
*
* - A, B, C, D four-phase LED indicates the status of the stepper motor work.
* - Stepper motor with a standard interface, when used directly pluggable.
* - 5 line 4 phase can be used for ordinary ULN2003 chip driver, connect to the 2 phase ,
*       support the development board, with convenient use, direct docking.
*
* - Rated Voltage               : DC5V 4-phase
* - Step angle                  : 5.625 x 1/64
* - Reduction ratio             : 1/64
* - No-load Pull in Frequency   : >600Hz
* - No-load Pull out Frequency  : >1000Hz
* - Pull in Torque              : >34.3mN.m(120Hz)
* - Detent Torque               : >34.3mN.m
* - Temperature Rise            : < 40K(120Hz)
* - DC Resistance               : 200-ohm 7% (25C)
* - Insulation Resistance       : >10M-ohm (500V)
* - Dielectric Strength         : 600V AC / 1mA / 1s
* - Insulation Grade            : A
*
******************************************************************************/
class Motor28BYJ48 : virtual public StepperMotor
{
 public: // protected to save encapsulation code size, we go open-kimono!!
   int        pin1;                      // 4 pins, one each to the buffer.
   int        pin2;                      // 4 pins, one each to the buffer.
   int        pin3;                      // 4 pins, one each to the buffer.
   int        pin4;                      // 4 pins, one each to the buffer.

   int        minimum_position;          // Some idea of a minimum position
   int        maximum_position;          // The maximum position in microns (integer)
   int        currentPosition;           // minimum_position <=currentPosition   <= maximum_position
   int        newPosition;               // target position, set before a move

   // HallSensor sensor;                 // has-a relatinoship unimplemented here.
   int        minimum_speed;             // Some idea of a minimum speed
   int        maximum_speed;             // The maximum speed in rpm
   int        speedlimit;                // rpm
   int        stepduration_us;           // duration of one steps in micro-seconds  (integer)
   int        overShoot;                 // backlash removal step count.
   FS_Dispatcher<StepperMotor *, 10> &TimeDispatcher;  // reference to a particular FS_Dispatcher
   int        dispatchinterval;          // The amount of time for millis bookkeeping update

   enum _mysteperstate { SteperStateIdle      = 0, // declare some prose for states.
                         SteperStateMoving    = 1,
                         SteperStateOvershoot = 2
                       };
   _mysteperstate mysteperstate;

 public:
    Motor28BYJ48 ( FS_Dispatcher<StepperMotor*, 10> &pTimeDispatcher,
                   int psteps_Revolution = 2048, // MUST HAVE
                   int ppin1             = -1,   //  MUST HAVE Pin = -1 is illegal.
                   int ppin2             = -1,   //  MUST HAVE Pin = -1 is illegal.
                   int ppin3             = -1,      //  MUST HAVE Pin = -1 is illegal.
                   int ppin4             = -1,      //  MUST HAVE Pin = -1 is illegal.
                   int pminimum_position =  0,      // Optional... counts
                   int pmaximum_position =  0,      // counts
                   int pminimum_speed    =  0,
                   int pmaximum_speed    =  0,
                   int pspeedlimit       =  0,
                   int pstepduration_ms  =  0,
                   int pnewPosition      =  0,
                   int pcurrentPosition  =  0,      // Optional: Define default values
                   int poverShoot        =  0   // (iv (setq tmp (* 64 64.0 )))    4096.0
                 ):
       currentPosition(pcurrentPosition),
       newPosition(pnewPosition),
       overShoot(poverShoot),
       pin1(ppin1),
       pin2(ppin2),
       pin3(ppin3),
       pin4(ppin4),
       mysteperstate(SteperStateIdle),
       dispatchinterval(0),                // don't bother me.
       StepperMotor(64*64, 1, 64, 5.625),   // details specific to this motor
       TimeDispatcher(pTimeDispatcher)
    {
        // TODO add some code to determine some things from initial conditions.
        // This motor is geared.
    } // Motor28BYJ48::Motor28BYJ48()

    void ThinkFast()
    {
       switch(mysteperstate)
       {
       case  SteperStateIdle:
//            setSpeed(speednlimit);
//            step(newPosition - currentPos + overShoot)  // number of steps to move
//            TimeDispatcher.register_cb(dynamic_cast<StepperMotor*>(this),1000);
//            mysteperstate = SteperStateMoving
//            dispatchinterval = 100;                     // time to allow for
            break;
       case  SteperStateMoving:
//            step(-overShoot);
//            TimeDispatcher.unregister_cb(dynamic_cast<StepperMotor*>(this));            // pull my ticket
            mysteperstate = SteperStateOvershoot;         // the next thing to wake up in.
            break;
       case  SteperStateOvershoot:
            // motors off?
            mysteperstate = SteperStateIdle;
            break;
       default:
            TimeDispatcher.unregister_cb(dynamic_cast<StepperMotor*>(this));
            mysteperstate = SteperStateIdle;
       }
    }

    void setSpeed(int pspeed) // RPM
    {
       speedlimit = pspeed;   // TODO something!
    } // Motor28BYJ48::setSpeed

    void reset()
    {
       currentPosition = newPosition = 0;
    } // Motor28BYJ48::reset

    bool validp()
    {
       bool ret = true;
       ret &= ((pin1 > 0) && (pin2 > 0) && (pin3 > 0) && (pin4 > 0)); // one test!
       return ret;
    } // Motor28BYJ48::validp

    void report(string &str)
    {
        str += string("Motor28BYJ48::report Motor28BYJ48\n");
    } // Motor28BYJ48::report

}; // Motor28BYJ48

#endif
