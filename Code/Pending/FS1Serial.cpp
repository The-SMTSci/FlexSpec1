extern "C"
{
    #include <asm/termbits.h>
    #include <sys/ioctl.h>
    #include <unistd.h>
    #include <fcntl.h>
}

#include <iostream>
using namespace std;

#include "FS1Serial.h"

/*****************************************************************************
* FS1Serial::FS1Serial
*   "/dev/ttyAMA0" Example Device Name
*
*****************************************************************************/
FS1Serial::FS1Serial (string deviceName, int baud)
{
   handle = -1;
   Open (deviceName, baud);

} // FS1Serial::FS1Serial

/******************************************************************************
* FS1Serial::~FS1Serial
*   Clean up the instance.
******************************************************************************/
FS1Serial::~FS1Serial ()
{
   if(handle >= 0)
      Close ();                 // Resets handle to -1

} //  FS1Serial::FS1Serial::~FS1Serial

/******************************************************************************
* FS1Serial::Open
*   "/dev/ttyAMA0" Example Device Name
******************************************************************************/
bool FS1Serial::Open (string pdeviceName, int baud)
{
   struct termios tio;
   struct termios2 tio2;
   deviceName = pdeviceName;            // e.g. "/dev/ttyAMA0"
   baud       = baud;
   handle     = open (deviceName.c_str (), O_RDWR | O_NOCTTY /* | O_NONBLOCK */ );

   if(handle < 0)
      return false;
   tio.c_cflag     = CS8 | CLOCAL | CREAD;
   tio.c_oflag     = 0;
   tio.c_lflag     = 0;                 //ICANON;
   tio.c_cc[VMIN]  = 0;
   tio.c_cc[VTIME] = 1;                 // time out every .1 sec
   ioctl (handle, TCSETS, &tio);

   ioctl (handle, TCGETS2, &tio2);
   tio2.c_cflag &= ~CBAUD;
   tio2.c_cflag |= BOTHER;
   tio2.c_ispeed = baud;
   tio2.c_ospeed = baud;
   ioctl (handle, TCSETS2, &tio2);

   ioctl (handle, TCFLSH, TCIOFLUSH);   //   flush buffer

   return true;

} //  FS1Serial::Open

/******************************************************************************
* FS1Serial::IsOpen - Predicate to see if handle thinks it is open
*
******************************************************************************/
bool FS1Serial::IsOpen (void)
{
   return (handle >= 0);

} //  FS1Serial::IsOpen

/******************************************************************************
* FS1Serial::Close -- Close if handle is positive.
*
******************************************************************************/
void FS1Serial::Close (void)
{
   if(handle >= 0)
      close (handle);
   handle = -1;

} //  FS1Serial::Close

/******************************************************************************
* FS1Serial::Send   char * string of maxium length
*
******************************************************************************/
bool FS1Serial::Send (unsigned char *data, int len)
{
   if(!IsOpen ())
   {
      return false;
   }

   int rlen = write (handle, data, len);

   return (rlen == len);

} //  FS1Serial::Send

/******************************************************************************
* FS1Serial::Send  Plain character
*
******************************************************************************/
bool FS1Serial::Send (unsigned char value)
{
   if(!IsOpen ())
   {
      return false;
   }

   int rlen = write (handle, &value, 1);

   return (rlen == 1);

} //  FS1Serial::Send

/******************************************************************************
* FS1Serial::Send Send a std::string
*
******************************************************************************/
bool FS1Serial::Send (const string & value)
{
   if(!IsOpen ())
   {
      return false;
   }
   int rlen = write (handle, value.c_str (), value.size ());

   return (rlen == value.size ());

} //  FS1Serial::Send

/******************************************************************************
* FS1Serial::Receive - receive characters, put results in buffer
* up to size of buffer. Return count of bytes recieved.
*
******************************************************************************/
int FS1Serial::Receive (unsigned char *buffer, int bufsize)
{
   if(!IsOpen ())
   {
      return -1;
   }

   // this is a blocking receives
   int lenRCV = 0;
   while(lenRCV < bufsize)
   {
      int rlen = read (handle, &buffer[lenRCV], bufsize - lenRCV);
      lenRCV += rlen;
   }

   return lenRCV;

} //  FS1Serial::Receive

/******************************************************************************
*  FS1Serial::NumberByteRcv
*
******************************************************************************/
bool FS1Serial::NumberByteRcv (int &bytelen)
{
   if(!IsOpen ())
   {
      return false;
   }
   ioctl (handle, FIONREAD, &bytelen);

   return true;

} //  FS1Serial::NumberByteRcv
