/******************************************************************************
* FS_CharMask.h -- implement a valid character mask [0..255] for testing.
* Hack to allow making a mask and adding things later with low difficulty
******************************************************************************/
#ifndef __FS_CHARMASK_H__
#define __FS_CHARMASK_H__

#include <string>
using namespace std;

class FS_CharMask
{
  char    mask[255] = {0};    // space for this mask
  string  basis;              // The basis for this mask
public:

   FS_CharMask(const string &ref) :
     basis(ref)
   {
     int i = 0; ;
      //for(i = 0; i < sizeof(mask); ++i)
      //  mask[i] = 0;
      for(i = 0; i < ref.length(); ++i)
        mask[ref[i]] = 1;

   } // FS_CharMask

   bool validcharacter(char ch) const
   {
      return mask[ch] == 1;

   } // FS_CharMask::validcharacter

   bool validcharacter(const string &ref) const;
   string replace(const string &ref, char replace_ch) const; // replace_ch = ' '


}; // FS_CharMask

#endif

