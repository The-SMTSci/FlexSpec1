/******************************************************************************
* AMA0Uart.h
*
******************************************************************************/
#ifndef _AMA0UART_H__
#define _AMA0UART_H__

#include <stdio.h>
//#include <stdlib.h>
#include <unistd.h>
//#include <sys/types.h>
//#include <sys/socket.h>
//#include <netinet/in.h>
#include <fcntl.h>
#include <errno.h>
#include <sys/signal.h>
#include <termios.h>

#include <string>
using namespace std;

extern "C" {
void C_AMAReader (int status);   /* definition of signal handler */
}

class AMA0Uart
{
   string devname;
   int    devmode;
   long   baud;
   int    status;          // set to 1 if open
   int    fd;

 public:
   AMA0Uart(const string pdevname,
            int pmode = O_RDWR | O_NOCTTY | O_NDELAY);

   ~AMA0Uart()
   {
      if(status)
      {
         close(fd);
      }
   } // ~AMA0Uart

   int read()          {}
   int write(const string &ref)   {}

}; // AMA0Uart


#endif
