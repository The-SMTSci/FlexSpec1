/******************************************************************************
* FS_CircularBuffer.h -- manage a circular buffer for serial characters.
*  The template form allows fixing the max allocation of size.
# (compile "g++ -D__LINUX__ -c FS_CircularBuffer.h")
******************************************************************************/
#ifndef __FS_CIRCULARBUFFER_H__
#define __FS_CIRCULARBUFFER_H__
#ifdef __LINUX__
#include <iostream>
#endif
#include <cstddef>        // picks up size_t
#include <vector>
#include "FS_CharMask.h"

using namespace std;

/******************************************************************************
* FS_CircularBuffer<length> -- implement a vector of type char, where char
* is an acceptable JSON character [ _A-Za-zO-9[\]{}.+-"].
* If full, then return false and drop this last character.
* 
* Returns in general:
*   bool means a push was OK
*   a zero char NULL is illegal and indicates a bad pop.
*   other values as expected.
* 
******************************************************************************/

typedef enum _FS_CircularBuffer_Enum 
                 { EMPTY = 0x00, FULL = 0x01, OVERFLOW = 0x02, 
                   UNDERFLOW = 0x04, ILLEGAL_CHAR = 0x08,
                   INVALID = 0x10
                 } FS_CircularBuffer_Enum;

template <size_t TTT>
class FS_CircularBuffer
{
    //static const size_t EMPTY = ~ 0u;    // 0xffffffffffffffff  (64 bit on arm?)
    // We're now a template and have no .cpp module to finalize this value.
    // we hack the constant in by hand.

    std::vector<char>       data                 ; // type char is ASCII -- here JSON subset.
    size_t                  next  = 0            ; // index at which next insert will occur
    size_t                  head  = ~0u /*EMPTY*/; // index of next pop, or EMPTY marker
    FS_CircularBuffer_Enum  flags =  FS_CircularBuffer_Enum::EMPTY ; 
    FS_CharMask             mask                 ; // All are legal.

public:
    FS_CircularBuffer(FS_CharMask             &pmask = FS_CharMask()) :
        mask(pmask),
        data(TTT),                        // fill constructor set size.
        next(0),                            // Set our values.
        head(0)
    {}

    //virtual ~CircularBuffer() = default;

    FS_CircularBuffer<TTT> &reset()
    {
       head = ~0u /*EMPTY*/;
       next = 0;
       return *this;                        // allow chaining.
    } // FS_CircularBuffer::reset

    // FS_CircularBuffer::validcharp    validity predicate
    bool validcharp(char testchar) const
    {
       return mask.validcharacter(testchar);
    } // FS_CircularBuffer::validcharp

    // FS_CircularBuffer::emptyp        validity predicate
    bool emptyp() const
    {
        return head == ~ 0u /*EMPTY*/;
    } // FS_CircularBuffer::emptyp
                                        
    // FS_CircularBuffer::fullp         validity predicate
    bool fullp() const
    {
       return head == next && head == ~ 0u; /*EMPTY*/
    } // FS_CircularBuffer::fullp

    /******************************************************************
    *  size - return the amount of space used.
    ******************************************************************/
    size_t size() const
    {
      size_t  ret = 0;
        if (emptyp())
            ret = 0;
        if (next > head)
            ret = next - head;
        else
           ret = data.size() - head + next;
        return ret;

    } // FS_CircularBuffer::size

    /******************************************************************
    *  push - return true/false. False is a overrun situation.
    *  Uses a boolean as  Arduino has removed exceptions.
    ******************************************************************/
    bool push(char val)
    {
      bool ret = false;

        if (validcharp(val) && ! fullp())
        {
            data[next] = val;
            if (emptyp())
                head = next;
            else if (++next == data.size())  // wrap the buffer
                next = 0;
            ret = true;
        }
        return ret;

    } // FS_CircularBuffer::push

    /******************************************************************
    *  pop - return a zero (null) illegal in our use as Arduino
    *  has removed exceptions. or the character.
    ******************************************************************/                  
    char pop()
    {
     const char popVal = 0;       // illegal char as bad pop.
        if (! emptyp())
        {
            if (++head == data.size())
                head = 0;
            if (head == next)
                head = ~ 0u /*EMPTY*/;
        }

        return popVal;

    } // FS_CircularBuffer::pop

    FS_CircularBuffer<TTT> &debug()
    {
#ifdef __LINUX__
       cout << "FS_CircularBuffer capacity" << TTT << " size " << size() << endl;
       cout << "   next " << next << endl;
       cout << "   head " << head << endl;
       cout << "   full " << fullp() << endl;
#endif
       return *this;
    } // FS_CircularBuffer::debug

    friend ostream &operator << (ostream &os, FS_CircularBuffer<TTT> &ref)
    {
       ref.dump(os);
    } //  FS_CircularBuffer::friend ostream &operator << 

#ifdef __LINUX__
    void dump(ostream &os = cout)
    {
       char comma=' ';
       cout << "[";
       for(int i = 0; i < TTT; ++i)
       {
          if(validcharp(data[i]))
             cout << comma << data[i];
          else
             cout << comma << " ";
          comma = ',';
       }
       cout << "]" << "(size " << size() << ")" 
            << " head=" << head << ','
            << " next=" << next
            << endl;
    } //  FS_CircularBuffer::dump
#endif

}; // FS_CircularBuffer

#endif
