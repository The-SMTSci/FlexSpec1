/******************************************************************************
* FS_CharMask_Regression.cpp -- test the header-only include file.
*   g++ -o FS_CharMask -D__REGRESSION__ FS_CharMask.cpp && ./FS_CharMask
* 2021-07-28T21:39:06-0600 wlg
******************************************************************************/
#include <iostream>
#include <string>
#include "FS_CharMask.h"

using namespace std;

/******************************************************************************
* FS_CharMask::validcharacter -- enough need for a callable routine.
*
******************************************************************************/
bool FS_CharMask::validcharacter(const string &ref) const
{
 bool ret = true;
   for(int i = 0; i < ref.length(); ++i)
      if(mask[ref[i]] == 0)
      {
         ret = false;
         break;
      }

   return ret;

} // FS_CharMask::validcharacter

/******************************************************************************
* FS_CharMask::replace -- enough need for a callable routine.
*
******************************************************************************/
string FS_CharMask::replace(const string &ref, char replace_ch = ' ') const
{
 string ret(ref);                          // Copy all...
    for(int i = 0; i < ref.length(); ++i)
       if(mask[ref[i]] == 0)
          ret[i] = replace_ch;             // ... replace as needed
    return ret;
} // FS_CharMask::replace

#ifdef __REGRESSION__
/******************************************************************************
*                            Linxu  REGRESSION  MAIN
*
******************************************************************************/
int main(int c, char **v)
{
 FS_CharMask  jsonmask1(string(" ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_[]{}+-.:\""));
 FS_CharMask  jsonmask2(string(" abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_[]{}+-.:\""));

 string   test1("{\"fred\" : 12}");
 char     ch;

   cout << "fail check jsonmask1 " << test1 << " " << jsonmask1.validcharacter(test1) << endl;
   cout << "pass check jsonmask2 " << test1 << " " << jsonmask2.validcharacter(test1) << endl;

   for(int i = 0; i < test1.length() ; ++i)
   {
      ch = test1[i];
      cout << "char " << ch << " " << jsonmask2.validcharacter(ch) << endl;
   }

   string test2(jsonmask1.replace(test1));
   cout << "pass check jsonmask1 " << test2 << " " << jsonmask1.validcharacter(test2) << endl;

   return 0;

} // main

#endif
