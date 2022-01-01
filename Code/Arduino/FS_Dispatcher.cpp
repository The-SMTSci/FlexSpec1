/*****************************************************************************
* FS_Dispatcher.cpp -- This should not be installed in the Arduino, it is a
*  linux test framework.
*
*****************************************************************************/
#include <iostream>
#include <string>
#include "FS_Dispatcher.h"

using namespace std;

#ifdef __REGRESSION__

/******************************************************************************
* Test Classes... Foo is 'Patron'; bar and baz two widgys
******************************************************************************/
class foo
{
public:
   int    dispatchinterval;
   string name;

   foo(const string &pname, int pdispatchinterval = 0):
       name(pname),
       dispatchinterval(pdispatchinterval)   {}

   virtual void say(int i)             = 0;     // Pure virtual functions
   virtual int  getnext() const        = 0;
   virtual void report(string &)       = 0;
   virtual void ThinkFast(string &ref) = 0;

}; //foo

/******************************************************************************
* class bar
*
******************************************************************************/
class bar : virtual public foo
{
public:

   bar(const std::string &pname,int pdispatchinterval=0) : 
     foo(pname,pdispatchinterval) {}
   void say(int i)             { cout << "just saying " << i << endl ; };
   int  getnext() const        { return dispatchinterval; }
   void report(string &ref)    { ref += name + "\n"; }
   void ThinkFast(string &ref) { ref += "thinking fast as I can " + name + "\n"; }
}; //bar

/******************************************************************************
* class baz
*
******************************************************************************/
class baz : virtual public foo
{
public:

   baz(const std::string &pname,int pdispatchinterval=0) : 
     foo(pname,pdispatchinterval) {}
   void say(int i)             { cout << "just saying " << i << endl ; };
   int  getnext() const        { return dispatchinterval; }
   void report(string &ref)    { ref += name + "\n"; }
   void ThinkFast(string &ref) { ref += "thinking fast as I can " + name + "\n"; }
}; //baz

/******************************************************************************
*                                 MAIN
*
******************************************************************************/
int main(int c, char **v)
{
  FS_Dispatcher<foo, 10> disp;                       // Dispatcher for foo's call ThinkFast member.
  
  // create a few widgy's for the test: two bars and one baz.
  bar *bar1     = new bar("bar1 instance"     , 0);  // Subclasses of 'foo's.
  bar *bar2     = new bar("bar2 fast instance", 1);
  baz *baz1     = new baz("baz1 instance"     , 0);

  string report = "starting...\n";                // start the report with a starting comment.

    disp.register_cb(dynamic_cast<foo*>(bar1), bar1->dispatchinterval);
    disp.register_cb(dynamic_cast<foo*>(bar2), bar2->dispatchinterval);
    disp.register_cb(dynamic_cast<foo*>(baz1), baz1->dispatchinterval);

    /******************************************************************
    *  Run over all the queued dispatch items ... and create a composit
    *  report. Remember the base report was initalized with 'starting...'
    ******************************************************************/
    disp.dispatch(report);                        // Access all the ThinkFast members.

    /******************************************************************
    *  TaDa! Issue the report, retire the side.
    ******************************************************************/
    cout << "The report is " << report << endl;

    return 0;

} // main

#else
int main(int c, char **v) { cout << "Non-regression" << endl; return 0;}

#endif // __REGRESSION__
