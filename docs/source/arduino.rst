Arduino Chips
=============

Follow the instructions:

`Seeeduino XIAO <https://wiki.seeedstudio.com/Seeeduino-XIAO/>`_


Arduino chips come in several flavors. Here we are using Arm -Core :index:`Arm` processors.

Download the Arduino IDE (here 1.8.15)

Under **File -> Preferences**

Into the **Additional Boards Manager URLs** enter:

"https://files.seeedstudio.com/arduino/package_seeeduino_boards_index.json"

**Tools -> Board -> Boards Manager**

Search/select **Seeed SAMD Boards** (see that it includes
Seeeduino XAIO M0, and install it. (here 1.21.1) Takes a beat.

The real trick is to start with the raw IDE and add the **Blink**
program. This shows the 'loop' is closed with respect to development.


Pin Outs
--------

..  code-block:: none
    :linenos:

    Pin Funcion Type Description
    1  D13          Digital GPIO
    2  +3V3 Power Out Internally generated power output to external devices
    3  AREF         Analog           Analog Reference; can be used as GPIO
    4  A0/DAC0      Analog ADC in/DAC out; can be used as GPIO
    5  A1           Analog ADC in; can be used as GPIO
    6  A2           Analog ADC in; can be used as GPIO
    7  A3           Analog ADC in; can be used as GPIO
    8  A4/SDA       Analog ADC in; I2C SDA; Can be used as GPIO (*)
    9  A5/SCL       Analog ADC in; I2C SCL; Can be used as GPIO(*)
    10 A6           Analog ADC in; can be used as GPIO
    11 A7           Analog ADC in; can be used as GPIO
    12 VUSB Normally NC; 
    13 RST          Digital In Active low reset input (duplicate of pin 18)
    14 GND Power Power Ground
    15 VIN Power In Vin Power input
    16 TX           Digital USART TX; can be used as GPIO
    17 RX           Digital USART RX; can be used as GPIO
    18 RST          Digital Active low reset input (duplicate of pin 13)
    19 GND Power Power Ground
    20 D2           Digital GPIO
    21 D3/PWM       Digital GPIO; can be used as PWM
    22 D4           Digital GPIO
    23 D5/PWM       Digital GPIO; can be used as PWM
    24 D6/PWM       Digital GPIO; can be used as PWM
    25 D7           Digital GPIO
    26 D8           Digital GPIO
    27 D9/PWM       Digital GPIO; can be used as PWM
    28 D10/PWM      Digital GPIO; can be used as PWM
    29 D11/MOSI     Digital SPI MOSI; can be used as GPIO
    30 D12/MISO     Digital SPI MISO; can be used as GPIO

Note: (12)can be connected to VUSB pin of the USB connector by shorting 
          a jumper Power In/Out

Logical
-------

Pins are "overloaded" in their ability; Use of some pins
precludes blocks of use.


..  code-block:: none
    :linenos:

    1  D13          Digital GPIO
    3  AREF         Analog  GPIO  Analog Reference
    4  A0/DAC0      Analog  GPIO  ADC in/DAC out
    5  A1           Analog  GPIO  ADC in
    6  A2           Analog  GPIO  ADC in
    7  A3           Analog  GPIO  ADC in
    8  A4/SDA       Analog  GPIO  ADC in; I2C SDA
    9  A5/SCL       Analog  GPIO  ADC in; I2C SCL
    10 A6           Analog  GPIO  ADC in
    11 A7           Analog  GPIO  ADC in
    20 D2           Digital GPIO
    21 D3/PWM       Digital GPIO  ; can be used as PWM
    22 D4           Digital GPIO
    23 D5/PWM       Digital GPIO  ; can be used as PWM
    24 D6/PWM       Digital GPIO  ; can be used as PWM
    25 D7           Digital GPIO
    26 D8           Digital GPIO
    27 D9/PWM       Digital GPIO  ; can be used as PWM
    28 D10/PWM      Digital GPIO  ; can be used as PWM
    29 D11/MOSI     Digital GPIO  SPI MOSI
    30 D12/MISO     Digital GPIO  SPI MISO
    
    
    16 TX           Digital USART TX; can be used as GPIO
    17 RX           Digital USART RX; can be used as GPIO
    
    
    2  +3V3 Power Out Internally generated power output to external devices
    12 VUSB Normally NC; 
    15 VIN Power In Vin Power input
    
    14 GND Power Power Ground
    19 GND Power Power Ground
    
    13 RST          Digital In Active low reset input (duplicate of pin 18)
    18 RST          Digital Active low reset input (duplicate of pin 13)
    


..

Libraries
---------

   `ArduinoJson library <https://arduinojson.org/?utm_source=meta&utm_medium=library.properties>`_ 
