/******************************************************************************
* FS1RingBuf
*
******************************************************************************/
#ifndef __FS1RINGBUF_H__
#definf __FS1RINGBUF_H__

/******************************************************************************
* FS1RingBuf A simple ringbuffer for integers 
*https://git.jeelabs.org/jcw/embello/src/branch/master/lib/arch-lpc8xx/uart_irq.h
******************************************************************************/
template < int SIZE >
class FS1RingBuf 
{
 volatile uint8_t in
 volatile uint8_t out
 volatile uint8_t buf [SIZE];

public:

   FS1RingBuf () : in (0), out (0) {}

   bool isEmpty () const { return in == out; }
   bool isFull () const { return (in + 1 - out) % SIZE == 0; }

   void put (uint8_t data)
   {
      if (in >= SIZE)
         in = 0;
      buf[in++] = data;
   } // put

   uint8_t get ()
   {
      if (out >= SIZE)
         out = 0;
      return buf[out++];
   } // get

}; // FS1RingBuf

#endif
