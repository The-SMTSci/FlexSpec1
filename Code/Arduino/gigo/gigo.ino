/******************************************************************************
* gigo.ino --
* (compile "g++ -I../../ -D__REGRESSION__ -g --std=c++11  -o gigo -x c++ gigo.ino && ./gigo")
*
* A simple program that listens on Serial and bounces its input back to
* both the Serial and Serail1 ports. Designed to test the loopback on ports.
*
* (insert (format "\n* %s" (buffer-file-name)))
* /home/git/external/FlexSpec1/Code/Arduino/gigo/gigo.ino
******************************************************************************/
#ifdef __REGRESSION__
#include "FakeArduino.h"
#define __UNIT_TEST__ 1
#endif

static char buf;

/******************************************************************************
* setup
*
******************************************************************************/
void setup()
{
   Serial.begin(9600);
   Serial1.begin(9600);
   delay(3000);                // Allow port turn around time

} // setup

/******************************************************************************
* gigo loop main loop
*
******************************************************************************/
void loop()
{
   while(Serial.available())                // bounce back to serial
   {
      buf = Serial.read();
      Serial.print(buf,DEC);
   }
   while(Serial1.available())               // bounce to Serial1 too.
   {
      buf = Serial1.read();
      Serial1.print(buf,DEC);
   }

} // gigo loop

/*****************************************************************************
*                                MAIN UNIT TEST
*****************************************************************************/
#if __UNIT_TEST__ == 1
int main(int c, char **v)
{
    std::cout << "No regression tests for gigo." << std::endl;
    return 0;
} // main

#endif //__UNIT_TEST__


