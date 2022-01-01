#ifndef __SERIAL__H_
#define __SERIAL__H_

#include <string>
using namespace std;

/******************************************************************************
* FS1Serial - A class for Serial Port Communication for RPI.
* Turn off the console on the RPi via the boot script.
* The GPIO pins are:
*
*
* 
******************************************************************************/
class  FS1Serial
{

public:

  int     handle;
  int     baud;
  string  deviceName;

  FS1Serial(std::string deviceName, int baud);
  ~FS1Serial();

  bool Send(unsigned char  *data,int len);
  bool Send(unsigned char value);
  bool Send(const string  &value);
  int  Receive(unsigned char  *data, int len);
  bool IsOpen(void);
  void Close(void);
  bool Open(string deviceName, int baud);
  bool NumberByteRcv(int &bytelen);

}; // class  FS1Serial

#endif // __SERIAL__H_
