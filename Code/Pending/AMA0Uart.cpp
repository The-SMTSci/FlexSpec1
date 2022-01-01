/******************************************************************************
* AMA0Uart3.cpp
* /home/git/external/FlexSpec1/Code/RPi/AMA0Uart.cpp
******************************************************************************/
#include "AMA0Uart.h"
#include <string>
using namespace std;

AMA0Uart *AMA0_handler;

/******************************************************************************
* C_UARTReader - this is a "C" function tied to the system during the instantiation
*  Current (or past) compilers had issues with typedefing this thing.
*  We use a separate class pointer ('AMA0_handler') that is initialized by
*  main to act as the "One and only" member for this routine.
******************************************************************************/
extern "C"
{
    void C_AMAReader (int status)
    {
         AMA0_handler->read();   // call the only member we should
    }
}

/******************************************************************************
* AMA0Uart -- Another interrupt dirven UART handler for Raspberry Pi.
*   https://stackoverflow.com/questions/15119412/setting-serial-port-interruption-in-linux
******************************************************************************/
AMA0Uart::AMA0Uart(const string pdevname,
            int pmode) :
     devname(pdevname),   // The name of the port
     devmode(pmode),      // Mode
     fd(-1)               // Unix file handle (-1 is closed/invalid)
{
  struct sigaction saio;
  struct termios   termAttr;

   fd = open("/dev/ttyUSB0", O_RDWR | O_NOCTTY | O_NDELAY);
   if (fd == -1)
   {
      perror("open_port: Unable to open /dev/ttyO1\n");
      exit(1);
   }
   else
   {
      saio.sa_handler  = C_AMAReader;  // this in turn calls an instance of this class
      saio.sa_flags    = 0;
      saio.sa_restorer = NULL;
      sigaction(SIGIO,&saio,NULL);

      fcntl(fd, F_SETFL, FNDELAY);
      fcntl(fd, F_SETOWN, getpid());
      fcntl(fd, F_SETFL,  O_ASYNC ); /**<<<<<<------This line made it work.**/

      tcgetattr(fd,&termAttr);
      //baudRate = B115200;          /* Not needed */
      cfsetispeed(&termAttr,B115200);
      cfsetospeed(&termAttr,B115200);
      termAttr.c_cflag &= ~PARENB;
      termAttr.c_cflag &= ~CSTOPB;
      termAttr.c_cflag &= ~CSIZE;
      termAttr.c_cflag |= CS8;
      termAttr.c_cflag |= (CLOCAL | CREAD);
      termAttr.c_lflag &= ~(ICANON | ECHO | ECHOE | ISIG);
      termAttr.c_iflag &= ~(IXON | IXOFF | IXANY);
      termAttr.c_oflag &= ~OPOST;
      tcsetattr(fd,TCSANOW,&termAttr);
   }

} // AMA0Uart::AMA0Uart


/******************************************************************************
*                                  MAIN
*
******************************************************************************/
int main(int argc, char *argv[])
{
   AMA0_handler = new AMA0Uart(string("/dev/AMA0",O_RDWR | O_NOCTTY | O_NDELAY ));
} // Main

