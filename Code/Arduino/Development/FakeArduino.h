/******************************************************************************
* FakeArduino.h  Fake up some forward references, to allow debugging on
* big hardware during editing sessions.
*
* (compile "g++ --std=c++11 -c FakeArduino.h")
*
* % (iv (setq tmp (/ (expt 2 32) 86400000.0) ))   49.71 days per millis roll over
* 2021-08-28T13:32:49-0600 wlg.
******************************************************************************/
#ifndef __FakeArduino_H__
#define __FakeArduino_H__

//#pragma message("Using FAKE ARDUINO TYPEDEFS. FOR COMPILE ONLY.")

   #include <iostream>
   #define HIGH   (1)
   #define LOW    (0)
   #define OUTPUT (1)
   #define INPUT  (2)
   #define DEC    (0)

   // Pin Support
   void          digitalWrite(int,int);
   unsigned int  digitalRead(int);
   void          analogWrite(int,int);
   unsigned int  analogRead(int);
   void          pinMode(int,int);

   // Timing support
   void          delay(int) {};              // 49ish days.
   unsigned long millis();

   // C++11 has hosed up varargs... pay attention to the new way.
   struct FakeSerial // This is not that hot!
   {
      int  decl;
      bool overflowflag;
      inline            FakeSerial() : overflowflag(false) {}
      inline void       FakeForceOverflow()                {overflowflag = true;}
      inline int        readBytes(char *buf, size_t len)   {buf[0] = 'a'; buf[1] = 0; return 1;}
      inline void       begin(int v)                       {}
      inline int        write(char ch)                     { return 1;}
      inline void       end()                              {}
      operator          int()                              { return 99;}
      inline bool       overflow()
         {
             bool ret =  overflowflag;  
             overflowflag = false; 
             return ret;
         }
      template<typename... VARNUM> inline void print(VARNUM... arg)   {}
      template<typename... VARNUM> inline void println(VARNUM... arg) {}
      inline bool       available()                        {return true;}
      inline char       read()                             {}

   };

   // Fake up hardware
   FakeSerial Serial  = FakeSerial();
   FakeSerial Serial1 = FakeSerial();

#define REPORT(ch,msg) (std::cout << ch << "" << msg << std::endl)

#ifdef __REGRESSION__
#define flexmain main
#endif



#endif
