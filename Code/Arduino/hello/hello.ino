/******************************************************************************
* gigo.ino -- 
* (compile "g++ -I../ -D__REGRESSION__ -g --std=c++11  -o gigo -x c++ gigo.ino && ./gigo")
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
*
******************************************************************************/
void loop()
{
   Serial.println("Hello USB\n");
   Serial1.println("Hello TTY\n");
   delay(1000);

} // gigo loop

/*****************************************************************************
*                                MAIN UNIT TEST
*****************************************************************************/
#ifdef __UNIT_TEST__
int main(int c, char **v)
{
    std::cout << "No regression tests for gigo." << std::endl;
    return 0;
} // main

#endif //__UNIT_TEST__


