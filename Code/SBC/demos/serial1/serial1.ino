/******************************************************************************
* Serial1.ino
*
******************************************************************************/
#include <string>

void setup()
{

   Serial.begin(9600);
   delay(100);

} // setup


/******************************************************************************
* loop
*
******************************************************************************/
void loop()
{
 int         i    = 1;
 int         ch   = 0;
 std::string buffer("Hello world ");
 
   for(;/* EVER */;)
   {
      
      //delay(1000);
      if(Serial.available())
      {
        ch = Serial.read();

        if(ch == 0x0a)
        {
          Serial.print(i++); Serial.print(" : "); Serial.println(buffer.c_str());
          buffer.clear();
        }
        else
        {
          buffer += (char)ch;
        }
      } // char is available
   } // for

} // loop
