/******************************************************************************
* gigo.ino -- 
* (compile "g++ -I../ -D__REGRESSION__ -g --std=c++11  -o gigo -x c++ hello.ino && ./gigo")
*
* A simple Arduino sketch to tell each port "Hello" on 1 second intervals.
*
*
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
*  Send a message to the serial port with a count. Delay is 1 second.
******************************************************************************/
void loop()
{
 int i;

   Serial .print("Hello USB  ") ; Serial.println(i++);
   Serial1.print("Hello TTY  ") ; Serial.println(i);
   delay(1000);

} // gigo loop

/*****************************************************************************
*                                MAIN UNIT TEST
*****************************************************************************/
#ifdef __UNIT_TEST__
#include <iostream>
int main(int c, char **v)
{
    std::cout << "No regression tests for hello." << std::endl;
    loop();
    return 0;
} // main

#endif //__UNIT_TEST__


