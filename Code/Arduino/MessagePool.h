#ifndef __MESSAGEPOOL.H__h__
#define __MESSAGEPOOL.H__h__
#ifdef __REGRESSION__
   #include <iostream>
#endif
// INIT FIX THESE LINES
#include "Message.h"
#include <string>  // INIT


using namespace std;

/******************************************************************************
* Implement as a non-pointer complicated class. If too many allocated
* then return a pointer to an overflow message.
******************************************************************************/
// Example: MessagePool<8,8,16>   smallfreepool;
// Example: MessagePool<2,8,64>   largefreepool;

template <int poolsize, int pstaddrlen, int messagelen>
class MessagePool
{
public:
   int                             freecells[poolsize];
   Message<pstaddrlen, messagelen> messagepool[poolsize];
   Message<pstaddrlen, messagelen> overflow;
   bool   status;

   MessagePool() : status(true) { clean();}

   Message< pstaddrlen,  messagelen>  *alloc()
   {
     Message< pstaddrlen,  messagelen> *ret = nullptr;

     for(int i = 0; i < poolsize; ++i)
     {
        if(freecells[i] == 1)
        {
           freecells[i] = 0;
           ret = &(messagepool[i]);
#ifdef __REGRESSION__
           cout << "allocated " << i << endl;
#endif
           break;
        }
     }

     if(ret == nullptr)
     {
        status = false;
        ret    = &overflow;
#ifdef __REGRESSION__
        // cout << "Message overflow" << endl;  TODO add log message
#endif
     }
     return ret;   // returns pointer to a "Message"

   } // Message::alloc

   Message< pstaddrlen,  messagelen>  *alloc(const char* pmsg)
   {
      Message< pstaddrlen,  messagelen>  *ret = alloc();
      alloc->send(pmsg);
      return ret;
   } // Message::alloc( msg )

   void recycle(Message< pstaddrlen,  messagelen> *pmsg)
   {
     for(int i = 0; i < poolsize; ++i)
     {
       if(&(messagepool[i]) == pmsg)
       {
          freecells[i] = 1;
          status = true;
#ifdef __REGRESSION__
          cout << "recycled " << i << endl;
#endif
          break;
       }
     }
   } //Message::recycle

#ifdef __REGRESSION__
   inline void dump()               // essentially __REGRESSION__'ed out.
   {
      cout << "Messagepool" << endl;
      for(int i = 0; i < poolsize; ++i)
      {
         cout  << freecells[i];
         if(freecells[1] == 1)
            cout << " " << " <free>";
         else
            cout << messagepool[i].message;
         cout << endl;
      }
   } //Message::dump
#endif

   MessagePool &clean()
   {
     for(int i = 0; i < poolsize; ++i)
       freecells[i] = 1;
     status = true;
     return *this;
   } //Message::clean

   bool statusp()
   {
     return status;
   } //Message::statusp

}; // MessagePool


#endif
