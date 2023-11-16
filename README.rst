FlexSpec1
=========

|Release| |Documentation|


Small telescope Flexible Spectrograph One.

Check out the documentation: 

`FlexSpec1 ReadTheDocs.io <https://flexspec1.readthedocs.io/en/latest/>`_

Serial Ports
------------

The later Rpi 4's are based on BCM2835 processor, and uses the
PL011 UARTs. 

.. list-table:: RPi 4 UART and Device Assignments
   :widths: 10 25 25 50
   :header-rows: 1

   *uart0 
     - GPIO 14    8  
     - GPIO 15   10  
     - /dev/ttyAMA0 
   *uart1 
     - GPIO 0    27  
     - GPIO 1    28  
     - /dev/ttyAMA1 
   *uart2 
     - GPIO 4     7  
     - GPIO 5    29  
     - /dev/ttyAMA2 
   *uart3 
     - GPIO 8    24  
     - GPIO 9    21  
     - /dev/ttyAMA3 
   *uart4 
     - GPIO 12   32  
     - GPIO 13   33  
     - /dev/ttyAMA4 

History:
--------

V0.0 - pre-release placeholder.

  
.. |Release| image:: https://img.shields.io/github/release/iraf-community/pyraf.svg
    :target: https://github.com/The-SMTSci/FlexSpec1/
    :alt: FlexSpec1 release

.. |Documentation| image:: https://readthedocs.org/projects/pyraf/badge/?version=latest
    :target: https://flexspec1.readthedocs.io/en/latest/
    :alt: FlexSpec1 Status


