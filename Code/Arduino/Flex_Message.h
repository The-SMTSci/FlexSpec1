#ifndef __FLEX_MESSAGE__h__
#define __FLEX_MESSAGE__h__
/******************************************************************************
* Flex_Message.h
*
* (compile "g++ -c Flex_Message.h && rm Flex_Message.h.gch")
*
******************************************************************************/
#ifdef __REGRESSION__
   #include <iostream>
#endif

#include <string>


/******************************************************************************
* Flex_Message - An envelope of sorts. The postalAddress is the name
*  of the destination and the message is the content.
*
* With a JSON string; The postal address should be the key and the
* value should be the message. 
* map<string &name, Message *> where name -> postalAddress for the Message.
*
******************************************************************************/
class Message
{
public:
   std::string postalAddress;
   std::string message;

   Message() {clear(); }

   Message(const char *ppostalAddress, const char *pmessage) :
        postalAddress(ppostalAddress),
        message(pmessage)
   {
   } // message::message

   Message(const std::string ppostalAddress, const std::string pmessage) :
        postalAddress(std::string(ppostalAddress)),
        message(std::string(pmessage))
   {
   } // message::message

   ~Message()
   { // Strings are automatically deleted.
   }

   Message &send(const char *pmessage)
   {
     strncpy(&(message[0]) , pmessage, sizeof(message));
     message[messagelen-1] = 0;
#ifdef __REGRESSION__
     cout << "Message send |" << message << endl;
#endif
     return *this;
   }  // Message:: send

   Message &clear()
   {
      message.clear();
      return *this;
   } // Message::clear

   int length()
   {
     return message.length();
   } // Message::length

}; // Message

#endif
