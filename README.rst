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
   :widths: 10 25 25 50 50
   :header-rows: 1

   * - UART
     - RX Pin (Board)
     - Tx Pin (Board)
     - Comm Port
     - Conflicts
   * - uart0 
     - GPIO 14    8  
     - GPIO 15   10  
     - /dev/ttyAMA0 
     - Serial Console
   * - uart1 
     - GPIO 0    27  
     - GPIO 1    28  
     - /dev/ttyAMA1 
     -
   * - uart2 
     - GPIO 4     7  
     - GPIO 5    29  
     - /dev/ttyAMA2 
     - I2C
   * - uart3 
     - GPIO 8    24  
     - GPIO 9    21  
     - /dev/ttyAMA3 
     -
   * - uart4 
     - GPIO 12   32  
     - GPIO 13   33  
     - /dev/ttyAMA4 
     - SPI0
   * - uart5
     - GPIO 12   14
     - GPIO 13   15
     - /dev/ttyAMA5

Other Interfaces
----------------

# Enabling I2C3, with SDA on GPIO4 and SCL on GPIO5
dtoverlay=i2c3,pins_4_5

History:
--------

V0.0 - pre-release placeholder.

  
.. |Release| image:: https://img.shields.io/github/release/iraf-community/pyraf.svg
    :target: https://github.com/The-SMTSci/FlexSpec1/
    :alt: FlexSpec1 release

.. |Documentation| image:: https://readthedocs.org/projects/pyraf/badge/?version=latest
    :target: https://flexspec1.readthedocs.io/en/latest/
    :alt: FlexSpec1 Status

PuTTY Commands:
+++++++++++++++

.. list-table:: PuYTTY FlexSpec1 Serial Port Commands
   :widths: 10 25 90
   :header-rows: 0

   * - A<CR>
     - 
     - All functions list
   * - B<CR>
     - 
     - Blue LED
   * - C<CR>
     - 
     - Configuration to set the grating lines per mm
   * - F<CR>
     - 
     - Focus the collimating lens
   * - G<CR>
     - 
     - Green LED lights the Green
   * - H<CR>
     - 
     - Home The Grating
   * - I<CR>
     - <PWM>
     - Incandescent Grain of Wheat Flat lamps, PWM 0 - 100%.
   * - J<CR>
     - 
     - Used to center zero order to focus on slit
   * - L<CR>
     - <PWM>
     - Flat Lamp lights the LED Flat lamps, PWM 0 - 100%.
   * - M<CR>
     - 
     - Reset collimating Focuses to zero
   * - N<CR>
     - 
     - Neon / Calibration
   * - O<CR>
     - 
     - Off Turns all lamps off
   * - Q<CR>
     - 
     - Query status of the spectrometer
   * - R<CR>
     - <PWM>
     - Red LED Controls The Red LED With PWM 0 - 100%
   * - S<CR>
     - 
     - Shutter  (Open Close Toggle)
   * - U<CR>
     - <PWM>
     - UV Boost Lights the UV Boost, PWM 0 - 100%.
   * - V<CR>
     - 
     - Viewer for Slit. Backlight View the slit with backlight
   * - W<CR>
     - <Integer>
     - Wavelength rotate the grating to center desired wavelength
   * - Z<CR>
     - 
     - Zero Collimating lens to position = 0 (home)
   * - 
     - 
     - (This should only be done once on initialization of
   * - 
     - 
     - physical focus)
   * - 
     - 
     - 
   * - ?<CR>
     - 
     - Query the Defines the grating and collimating motor direction
   * - 
     - 
     - (This should only be done once on initialization or
   * - 
     - 
     - if a motor is changed depending on the manufacture
   * - 
     - 
     - some motors run in oposit direction)



