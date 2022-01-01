/******************************************************************************
* FS_Processor
*
******************************************************************************/

#ifndef __FS_PROCESSOR__h__
#define __FS_PROCESSOR__h__
#ifdef __REGRESSION__
   #include <iostream>
#endif

#include <map>

using namespace std;

/******************************************************************************
* FS_Processor -- Keep it simple, only one dispatcher, set the timer
* to hit a static ISR that knows where FS_Processor is located and
* have it run the list of registered patrons. 
* Keep a map, using the patron's instance this pointer as the key
* and use the value as the current val to use.
* Let the patron store its requested interval as a variable, set the value
* on call and reset the value when it counts out.
* The patron registers by dispatchtable TheProcessor.register(this);
*          unregisters by dispatchtable TheProcessor.unregister(this);
* ) Scheduable things of type Patron * register
* ) The map<> prevents dual registration
* ) Member function unregister fails silently
* ) Only calls one function, here Process virtual member to Patron.
* ) 
* ) 
* ) 
******************************************************************************/
class FS_Processor
{
 protected:

   map< void *(FS_Patron::)(), int> dispatchtable; // key is patron 'this'; val is divideby

 public:
   FS_Processor() {}

   void register(*(FS_Patron::)() patron, interval)
   {
     dispatchtable[patron] = interval;
   } // FS_Processor::register

   void unregister(*(FS_Patron::)() patron)
   {
     map< void *(FS_Patron::)(), int> itor = dispatchtable.find(patron);
     if(itor != dispatchtable.end())
       dispatchtable.erase(patron);
   } // FS_Processor::unregister


   /*******************************************************************
   *  dispatch called by the matching static ISR.
   *  
   *******************************************************************/
   void dispatch()
   {
      void *(FS_Patron::)() *patron;

      for(map< void *(FS_Patron::)(), int> itor = dispatchtable.begin(),
          itor != dispatchtable.end()
          ++itor )
      {
         if( -- itor->second == 0)
         {
            void *(FS_Patron::)() *patron = itor.first;
            itor->second = patron->dispatchinterval;
            *patron->Process();
         }
      }
   } // FS_Processor::dispatch

}; // FS_Processor


using namespace std;
#endif

