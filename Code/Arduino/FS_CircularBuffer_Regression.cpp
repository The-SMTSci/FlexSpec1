/******************************************************************************
* FS_CircularBuffer_Regression.cpp -- regression test the buffer.
* (compile "g++ -D__LINUX__ -o FS_CircularBuffer_Regression FS_CircularBuffer_Regression.cpp && ./FS_CircularBuffer_Regression")
******************************************************************************/
#include <iostream>
#include "FS_CircularBuffer.h"

using namespace std;

/******************************************************************************
* FS_CircularBuffer_Regression.cpp -- test under linux.
* TODO: Hack in a test under Arduino.
******************************************************************************/
int main(int argc, char **argv)
{
  FS_CharMask             jsonmask1(string(" ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_[]{}+-.:\"")); // BAD incomplete for testing.
  FS_CharMask             jsonmask2(string(" abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_[]{}+-.:\"")); // May be right!

  FS_CircularBuffer<10>   buf(jsonmask2);
  int                     i;
  char                    testchar = 'a';

   buf.reset();
   cout << "Char a valid? " << buf.validcharp('a') << endl;
   cout << "buffer full?  " << buf.fullp() << endl;
   for(i = 0; i < 12; ++i)   // push with two errors
   {
      buf.push(testchar++);
      cout << buf << endl;
   }

   cout << "Bye FS_CircularBuffer." << endl;
} // main
