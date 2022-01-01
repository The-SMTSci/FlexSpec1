/******************************************************************************
* FS_Dispatcher
*
* (compile "g++ --std=c++11 -c FS_Dispatcher.h && rm FS_Dispatcher.h.gch")
*
******************************************************************************/

#ifndef __FS_DISPATCHER__h__
#define __FS_DISPATCHER__h__
#ifdef __REGRESSION__
   #include <iostream>
#endif
using namespace std;

#include <map>

/******************************************************************************
* FS_Dispatcher -- Keep it simple, only one dispatcher, set the timer
* to hit a static ISR/loop that knows where FS_Dispatcher is located and
* have it run the list of registered patrons.
*
* Keep a map, using the patron's instances' "this" pointer as the key
* and use the value as the current val to use.
*
* Let the patron store its requested interval as a variable, set the value
* on call and reset the value when it counts out.
* The patron   registers by dispatchtable TheDispatcher.register_cb(this);
*            unregisters by dispatchtable TheDispatcher.unregister_cb(this);
*
* Scheduable things of type "Patron *" register
* The map<> prevents dual registration
* Member function unregister_cb fails silently
* Only calls one function, here ThinkFast virtual member to Patron.
*
******************************************************************************/
template <class TTT, int TTTResetTime>
class FS_Dispatcher
{
 public:

   map< TTT*, int> dispatchtable; // key is patron 'this'; val is divideby

 public:
   FS_Dispatcher() {}

   void register_cb(TTT *fswidget, int interval)
   {
     dispatchtable[fswidget] = interval;  // find or insert a new key

   } // FS_Dispatcher::register_cb

   void unregister_cb(TTT *fswidget)
   {
     typename map<TTT *, int>::iterator itor = dispatchtable.find(fswidget);
     if(itor != dispatchtable.end())
       dispatchtable.erase(fswidget);    // remove the key if exists.

   } // FS_Dispatcher::unregister_cb

   /*******************************************************************
   *  dispatch called by the matching static ISR.
   *
   *******************************************************************/
   void dispatch(string &reportstr)
   {
      int                                resettime;
      int                                i = 0;
      typename map<TTT *, int>::iterator itor;

      for( itor = dispatchtable.begin();        // From the top of the container
           itor != dispatchtable.end();         // ... and not the end of the container
           ++itor)                              // ... move to the nest widgy
      {
         if( --itor->second == 0)               // the 'value part' is not empty
         {
            i++;                                // count fact we did think about something
            TTT *fswidget = itor->first;
            resettime = fswidget->getnext();    // get the fswidget dispatchinterval
            if(resettime == 0)                  // It its time! then report
            {
               resettime = TTTResetTime;
               fswidget->report(reportstr);     // Hit the widgy's report function
            }
            else
            {
               resettime -= 1;                  // Not now for this widgy
            }

            if((TTTResetTime == 0) && (resettime == 0))    // param TTTResetTime == 0 means disptch
                unregister_cb(itor->first);                // unregister before we...

            itor->second = fswidget->getnext(); // proceed, reset
            fswidget->ThinkFast(reportstr);     // Actually do something!
         }

      } // for

      if(i == 0)                                // we never thought of that!
         reportstr += " Nothing to report.";

   } // FS_Dispatcher::dispatch

}; // FS_Dispatcher

#endif

