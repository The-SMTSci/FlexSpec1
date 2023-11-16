FlexSpec1 Arduino Directory
===========================

An Arduino program consists of a *.ino* file, that acts like the main program.

The Arduino IDE/Compilers require the .ino file to be in a directory with the
same name. For example:  demos/hello/hello.ini is inside a directory called hello.

Any other file in the directory that ends in *.c*, *.cpp*, *.h*" will also
be compiled and linked into the code. So if you have a file call extras.cpp
and you want to keep it around as a temporary backup call it extras.cpp.bak
and it will be ignored.

Arduino code ***IS*** "--std=c++11" and "-fno-exceptions". This means quite
a few interesting new code features are available, like auto, looping extensions
etc. However it also means that "try/throw/catch" exception mechanism is 
disabled. The exception mechanism uses quite a bit of code.

Avoid anything that refers to "iostream" This brings in quite a lot of code.

C is a proper subset of C++, so do not feel compelled to use lots of C++
features.

ARM Boards, BLE/IoT and Seeduino Xaio
------

Boards are made to be compilent with different vendors environments. One is Mbed
and the other is SAMD. In some cases, libraries are written to take advantage
of only one environment's features! Thus code that compiles on one will fail
on another.

In the main .ino file, please use the IDE to gather the version and author's
name for each library package used. This helps to avoid confusion later.

This Directory
++++++++++++++

1. Demos
   a. hello : Print the word hello to the serial ports.
   b. gigo: Characters that are read, are printed right back. Handy for testing the CR/LF and baud rates.
2. MainBoard
   a. FlexSpec
3. Kzin
   a. Kzin


Serial Communications
+++++++++++++++++++++

The USB hardware in Arduinos, may not work well with the USB hardeare
found in hubs and main motherboards. This does cause some issues.

The clock rates of Arduinos are not that precise. 9600 baud may be 
a tad bit slower/faster -- but the protocol usually does not trip
over small differences.



