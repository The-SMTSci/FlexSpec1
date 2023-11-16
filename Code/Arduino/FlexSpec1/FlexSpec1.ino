
String CodeVersion = "4.1.2";
String CodeDate = "9/27/2023";
String CodeLocation = "SAS_NA1_3D_Spectrograph/V2-FS1Code/demos/My-FS1_Arduino_control_code_V4.1.2";

//                    This code is for Gregs board V4
//    This added the "A" routine to display all of the functions on request.

//&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
// IF RUNING WITH USB MAKE SURE THAT THE SERIAL MONITOR HAS "NO LINE ENDING" SELECTED
//&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

/*This Sketch takes my_serial inputs as controls for moving 28BYJ-48 stepper motors
   controlling collimating lens and grating position, Calibration and Flat lamps
   and location LEDs.

   Inputs are: integers and specific command letters entered through the my_serial Read
   function, the command notation being: NNNN <CR> for CCW rotation or -NNNN<CR> for
   CW rotation.
   Alpha inputs are:

  A<CR> Routine to display all functions
  B<CR> lights the Blue
  C<CR> Configuration to set the grating lines per mm
  F<CR> MOVES collimating lens focus
  G<CR> lights the Green
  H<CR> Home The Grating
  I<CR> lights the incandescent Grain of Wheat Flat lamps, PWM 0 - 100%.
  J<CR> Used to center zero order to focus on slit
  L<CR> lights the LED Flat lamps, PWM 0 - 100%.
  M<CR> Reset collimating Focuses to zero
  N<CR> lights the Neon bulb(s)
  O<CR> Turns all lamps off
  Q<CR> Query status of the spectrometer
  R<CR> Controls The Red LED With PWM 0 - 100%
  S<CR> This Opens And Closes The Shutter
  U<CR> Lights the UV Boost, PWM 0 - 100%.
  V<CR> View the slit with backlight
  W<CR> rotate the grating to center desired wavelength

  Z<CR> This sets the collimating lens position = 0 (home)
         (This should only be done once on initialization of physical focus)

  ?<CR> Defines the grating and collimating motor direction
        (This should only be done once on initialization or if a motor is changed
        depending on the manufacture some motors run in oposit direction)

   ALL COMMANDS WORK HIGH AND LOWER CASE

   All movement is ended with the motor rotating in the CW direction'
   and coils de-energized.

   Author: Clarke Yeager
   Version 4.1.2
   27 October 2023
*/

#include <Servo.h>  // loads the Servo.h library
#include "Wire.h"
#include "I2C_eeprom.h"

I2C_eeprom ee(0x57, I2C_DEVICESIZE_24LC256);  //establishes the I2C address for the 24LC256 EEPROM


//                               SPECTROGRAPH PROFILE
//              &&&& These are parameters that may need to be adjusted! &&&&
//  ===============================================================================================
#define my_serial Serial    // Serial1 is used with Putty, change this to Serial to use USB
int minimum = 3500;         // minimum selectable wavelength to be centered
int maximum = 7800;         // maximum selectable wavelength to be centered
int zeroOrderOffset;        // This is an offset number needed to center the slit after homing
int BkLashCount = 120;      // This is how many steps backlash goes
int minSteps = -700;        // The minimum negative steps are allowed in jog mode
int maxSteps = 450;         // The maximum positive steps are allowed in jog mode
float scaleFactor = .0540;  //gain to calibrate wavelength per motor step
float enterTime = 1500;     // This determines how long you have to enter a value after start of entry
int shutterOpen = 10;       //This is the value that determines the position of the open shutter
int shutterClosed = 140;    //This is the value that determines the position of the closed shutter
//  ---------------------------------------------------------------------------------------------------

//                      &&&& EEPROM address allocation &&&&
//  ===============================================================================================
int zeroOrderOffsetAddress = 12;  // Each address uses two bytes
int focusAddress = 14;            // focus location store two bytes
int focusPositionAddress = 16;    // focus location store two bytes
int negativeAddress = 18;         // focus location store two bytes
int inputAddress = 20;            // focus input offset;
int motorAddress = 22;            // Motor direction value
int gratingDirAddress = 24;       // grating motor direction value
int focusDirAddress = 26;         // focus motor direction value
int motorInitFlagAddress = 28;    // Motor initialization Flag
int posAddress = 30;              // Shutter position vlaue
int configurationAddress = 32;    // This is FS1 configuration

//  ---------------------------------------------------------------------------------------------------

int calLamp = 7;           // calibration lamp neon or Relco
int incandescentLamp = 4;  // this is the pin assignment for the Grain of wheat lamps
int UVBoostLED = 5;        // this boost the UV
int blueLED = 2;           // this is a blue marker
int greenLED = 9;          // this is a green marker
int slitLED = 10;          // this is the pin to backlight the slit
int flatLED = 3;           // this is a broad flat light
int redLED = 6;            // this is a red marker
int shutterPin = A1;       // this pin drives the shutter
int dly = 2;               //used to set the delay to control motor speed
int steps = 0;             //used to keep track of how many steps the stepper motor takes
int term = 8;              //this will be set to 0 when the desired number of motor sequence has been reached
int gsteps = 0;            // used to count the number of grating motor steps
int Position = 0;          // used to keep track of the grating position
int gratPosition = 0;      // used to keep track of the grating position
int gratStatus = 0;        // keeps track of the grating status
int colSteps = 997;        // collimating step count
int gratSteps = 997;       // grating step count
int zeroOrderSteps = 0;    // Zero order step count to center the slit in zero order
int zOrderSteps = 0;
int RequestedSteps = 0;  // The number of steps requested in jog mode
int zeroPosition = 0;    // used to keep track of the grating position
int PhaseHist;           // this is used to keep track of the last motor phase that was used
int orderPhaseHist;
int stepperPhase;
int zeroOrderPhase;
int zPhase = 0;
int phase;
int data = 20;
char savedFlag;      // Flag to show the homing has been done
int homed = 0;       // set to 1 when the grating has been homed
int colStepHist;     // keeps track of the collimating history if needed
int colPhaseHist;    // keeps track of the collimating motor history if needed
int gratStepHist;    // keeps track of the grating history if needed
int gratPhaseHist;   // keeps track of the grating motor history if needed
int magnetNew = 0;   //used to sense what magnetic polarity the Hall polarity sees for homing
int magnetOld = 0;   //remember the previous state so a transition can be recognized for homing
int magnetPin = A2;  //used for the homing Hall sensor
int CW = 0;          //keeps track if the rotation is CW or CCW
float wavelength;    //wavelength in Angstroms
int cal = -1;        // Relco calibration lamp starts off, LED will toggle between on and off
int UVBoost = -1;    // UV Boost LED starts off, LED will toggle between on and off
int incandescent;    // incandescent grain of wheat lamps start off
float GowPWM = 0;    // grain of wheat duty cycle (0 - 255)
float GowPWMnew;     // entered grain of wheat duty cycle
int blue = -1;       // Blue marker start off, LED will toggle between on and off (4700 angstroms)
int green = -1;      // green marker start off, LED will toggle between on and off, (5000 angstroms)
int slit = -1;       // slit illuminator to backlight the slit
int flat;            // Flat LED start off
float flatPWM = 0;   // Flat LED duty cycle (0-255)
float flatPWMnew;    // Entered flat LED duty cycle
int red;             // Red LED start off, (6590 angstroms)
float redPWM = 0;    // Red LED duty cycle (0-255)
float redPWMnew;     // Entered Red LED duty cycle
float UVPWM = 0;  // UV LED duty cycle (0-255)
float UVPWMnew;   // Entered UV LED duty cycle

int shutterStatus = 1;  // shutter starts open, it will toggle from open to closed
int servoPin = A1;      // Pin used for the shutter
int servoPos;           // Keeps track if the shutter is open or closed

int pos;               // The current position of the shutter servo
int posHist;           // Keeps track of where the shutter servo has been
int servo_delay = 25;  // Settle time for shutter moves
Servo shutterServo;    // Connect to the servo
int output;

int motorFlag;
int motorDir;
int gratingDir;
int focusDir;
int stepHist;

int colLocation;
float colPos;
float inputSteps;
int lastPosition;
int negativeFlag;
int negFlagHist;
int focusDirCode;
int focus;
int focusPosition;
int gratingDirCode;
int input;
int tempNegativeFlag;
int grating_mm;
int POR = 0;
int test;

float result;

// This void deals with the 2's compliment for negative numbers and large numbers < 32,768
//  ===============================================================================================

void write2BytesIntIntoEEPROM(int focusAddress, int number) {
  ee.writeByte(focusAddress, (number >> 8) & 0xFF);  //This writes two bytes to EEPROM, byte1 and byte2
  ee.writeByte(focusAddress + 1, number & 0xFF);     // byte1 is shifted and then byte2 is added to the result of the shift
}

int read2BytesFromEEPROM(int focusAddress)  //This reads two bytes to EEPROM, byte1 and byte2
{
  return (ee.readByte(focusAddress) << 8) + ee.readByte(focusAddress + 1);
}


// Patterns for collimator motor drive, 8 drive patterns,
//  ===============================================================================================
int dataArray1[8] = { 0b00000001, 0b00000011, 0b00000010, 0b00000110, 0b00000100, 0b00001100, 0b00001000, 0b00001001 };  //motor 1 CW
int dataArray2[8] = { 0b00001001, 0b00001000, 0b00001100, 0b00000100, 0b00000110, 0b00000010, 0b00000011, 0b00000001 };  //motor 1 CCW

// Patterns for grating motor drive, 8 drive patterns,
//  ===============================================================================================
int dataArray4[8] = { 0b00010000, 0b00110000, 0b00100000, 0b01100000, 0b01000000, 0b11000000, 0b10000000, 0b10010000 };  //motor 2 grating CW
int dataArray3[8] = { 0b10010000, 0b10000000, 0b11000000, 0b01000000, 0b01100000, 0b00100000, 0b00110000, 0b00010000 };  //motor 2 grating CCW

void displayFunctionList();
void functionList();
void enterFunction();
void resetFocus();
void homing();
void backlash();

//&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

void setup() {
  my_serial.begin(9600);
  delay(1000);

  ee.begin();
  int eeOutput = read2BytesFromEEPROM(zeroOrderOffsetAddress);
  if (eeOutput > 32768)  //if this is true the number is negative
  {
    zeroOrderOffset = -1 * (65536 - eeOutput);  //this converts a large number representing a negative number to a -value
  }

  delay(10);

  my_serial.println(" ");
  my_serial.print("zeroOrderOffset = ");
  my_serial.println(zeroOrderOffset);
  my_serial.println(" ");

  int eeOutput1 = read2BytesFromEEPROM(focusAddress);
  if (eeOutput1 > 32768)  //if this is true the number is negative
  {
    focus = -1 * (65536 - eeOutput);  //this converts a large number representing a negative number to a -value
  }

  pinMode(calLamp, OUTPUT);
  pinMode(UVBoostLED, OUTPUT);
  pinMode(blueLED, OUTPUT);
  pinMode(greenLED, OUTPUT);
  pinMode(redLED, OUTPUT);
  pinMode(shutterPin, OUTPUT);
  analogWrite(incandescentLamp, 0);

  // The motor drive is turned off to prevent the motors from heating up.
  // This will initialize both motors to prevent motors from heating up.

  // setup motor driver
  Wire.beginTransmission(0x21);  // transmit to device #44 (0x2c)
  Wire.write(byte(0x02));        // set to output port 0
  Wire.write(0x00);              // set to outputs low port 0
  Wire.write(0x00);              // set to outputs low port 1
  Wire.endTransmission();

  Wire.beginTransmission(0x21);  // transmit to device #44 (0x2c)
  Wire.write(byte(0x06));        // set to config port 0
  Wire.write(0x00);              // set to outputs
  Wire.write(0x00);              // set port 0 to outputs
  Wire.endTransmission();

  motorFlag = read2BytesFromEEPROM(motorInitFlagAddress);

  if (motorFlag != 1) {
    gratingDir = 1;
    focusDir = 1;
    my_serial.println("=============== This will occur only during the initial build ==========================");
    my_serial.println("              ----------------------------------------------------");
    my_serial.println("The motor direction control is stored in EEPROM. For first build EEPROM has no value stored.");
    my_serial.println("The motor control in EEPROM is automatically initialized before function can be established ");
    my_serial.println("Both the grating and focus motor direction have been set to the default direction. ");
    my_serial.println("The motor directions should be checked. A positive jog command J<CR> should rotate the grating holder CW.");
    my_serial.println("If it rotates CCW the ?<CR> command needs to be executed to correct it.");
    my_serial.println("To check the focus motor direction execute the F<CR> and specify a value between +/- 0% and 100%.");
    my_serial.println("The collimating lens should move toward the grating for a positive value and away for a negative value.");
    my_serial.println("If it moves in the wrong direction the ?<CR> command needs to be executed to correct it.");
    my_serial.println(" ");
    my_serial.println(" ");
    my_serial.println("=============== If a motor has been changed the direction needs to be checked ==========================");
    my_serial.println("              -----------------------------------------------------------------");
    my_serial.println("The motor directions needs to be checked. A positive jog command J<CR> should rotate the grating holder CW.");
    my_serial.println("If it rotates CCW the ?<CR> command needs to be executed to correct it.");
    my_serial.println("To check the focus motor direction execute the F<CR> and specify a value between +/- 0% and 100%.");
    my_serial.println("The collimating lens should move toward the grating for a positive value and away for a negative value.");
    my_serial.println("If it moves in the wrong direction the ?<CR> command needs to be executed to correct it.");
    my_serial.println(" ");
    my_serial.println(" ");
    my_serial.println(" ");

    write2BytesIntIntoEEPROM(gratingDirAddress, 1);  //Initialize grating motor direction to default
    gratingDir = read2BytesFromEEPROM(gratingDirAddress);

    write2BytesIntIntoEEPROM(focusDirAddress, 1);  //Initialize collimating Focus motor direction to default
    focusDir = read2BytesFromEEPROM(focusDirAddress);

    my_serial.print("grating motor direction = Default ");
    write2BytesIntIntoEEPROM(motorAddress, 5);
    my_serial.println(gratingDir);
    my_serial.println("focus motor direction = Default");
    write2BytesIntIntoEEPROM(motorInitFlagAddress, 1);
    my_serial.println(" ");
    my_serial.println("motor initialization = complete");
    write2BytesIntIntoEEPROM(motorInitFlagAddress, 1);
    my_serial.println(" ");
  }

  // --------Always starts with the shutter open ----------

  shutterServo.attach(servoPin);  // This activates the shutter servo
  posHist = read2BytesFromEEPROM(posAddress);

  for (pos = posHist; pos >= shutterOpen; pos -= 3)  // moves in 1 degree steps to control speed
    // moves shutter to the open position
  {
    shutterServo.write(pos);  // tell servo to go to position in variable 'pos'
    delay(servo_delay);       // waits for the servo to reach the position
  }
  shutterServo.detach();  // This turns off the shutter servo after opening the shutter
  my_serial.print("Shutter Is Open");
  write2BytesIntIntoEEPROM(posAddress, pos);  //Initialize grating motor direction to default
  posHist = read2BytesFromEEPROM(posAddress);

  shutterStatus = 1;

  focusDir = read2BytesFromEEPROM(focusDirAddress);
  gratingDir = read2BytesFromEEPROM(gratingDirAddress);
  displayFunctionList();
}

//  ===============================================================================================
void loop() {

  displayFunctionList();
  enterFunction();
}

//  ===============================================================================================
void displayFunctionList() {

  my_serial.println(" ");
  my_serial.println(" ");
  my_serial.println("               A<CR> To Display all functions");
  my_serial.println(" ");     
}

//  ===============================================================================================
void functionList() {

  my_serial.println(" ");
  my_serial.println(" ");
  my_serial.println("===================================");
  my_serial.println("A<CR> Display all functions");
  my_serial.println("B<CR> Toggles The Blue Marker On and Off");
  my_serial.println("C<CR> Configuration to set the grating lines per mm ");
  my_serial.println("F<CR> Focuses The Collimating lens ");
  my_serial.println("G<CR> Toggles The Green Marker On and Off");
  my_serial.println("H<CR> Home The Grating");
  my_serial.println("I<CR> Controls The Incandescent Grain of Wheat Bulb(s) With PWM 0 - 100%");
  my_serial.println("J<CR> Offset jog steps requested");
  my_serial.println("L<CR> Controls The Flat LED With PWM 0 - 100%");
  my_serial.println("M<CR> Reset Collimating Focuses to zero ");
  my_serial.println("N<CR> Toggles The Neon Bulb(s)- Relco Lamps On and Off");
  my_serial.println("O<CR> This Turns Off All Lamps");
  my_serial.println("Q<CR> Query status of the spectrometer ");
  my_serial.println("R<CR> Controls The Red LED With PWM 0 - 100%");
  my_serial.println("S<CR> This Opens And Closes The Shutter");
  my_serial.println("U<CR> Controls UV-Boost with PWM 0 - 100%");
  my_serial.println("V<CR> View the slit with backlight");
  my_serial.println("W<CR> rotates Grating to desired wavelength ");
  my_serial.println("Z<CR> Set Collimation Focus Position = 0 (Home position");
  my_serial.println("?<CR> Defines the grating and collimating motor direction");
  my_serial.println("===================================");
  my_serial.println(" ");
  my_serial.println(" ");
}

//  ===============================================================================================
void enterFunction() {
  
  my_serial.println("Enter The Desired Function Code ");
  my_serial.println("  ");
  while (my_serial.available() == 0) {
    steps = 0;
    gsteps = 0;
  }

  char ch = my_serial.read();
  my_serial.print("Option Entered = ");
  my_serial.print(ch);
  my_serial.println("  ");

  switch (ch) {
    //  ===============================================================================================
    case 'A':
    case 'a':

  functionList();

  break;

  //===================================================================================
case '?':  //A question mark is used so this function is not likely to be accidentally executed.

  my_serial.println("  ");
  my_serial.println("This function will set the direction of rotation for the grating motor and collimating motor ");
  my_serial.println("This function will only need to be run at the initial setup or when a motor is replaced ");
  my_serial.println("  ");
  my_serial.println("=============== If a motor has been changed the direction needs to be checked ==========================");
  my_serial.println("              -----------------------------------------------------------------");
  my_serial.println("A positive jog command J<CR> should rotate the grating holder CW.");
  my_serial.println("If it rotates CCW this ?<CR> command is used to correct it.");
  my_serial.println("To check the focus motor direction execute the F<CR> and specify a value between +/- 0% and 100%.");
  my_serial.println("The collimating lens should move toward the grating for a positive value and away for a negative value.");
  my_serial.println("If it moves in the wrong direction this ?<CR> command is used to correct it.");
  my_serial.println("The collimating lens should move toward the grating for a positive value and away for a negative value.");
  my_serial.println("If it moves in the wrong direction this ?<CR> command is used to correct it.");
  my_serial.println(" ");
  my_serial.println(" ");
  my_serial.println("Enter the desired motor direction ");

  my_serial.println("     1 = Grating motor default");
  my_serial.println("     2 = Grating motor reverse");
  my_serial.println("     3 = Focus motor default");
  my_serial.println("     4 = Focus motor reverse");
  my_serial.println("     5 = Both motors default");
  my_serial.println("     6 = both motor reverse");
  my_serial.println(" ");
  while (my_serial.available() == 0) { /*do nothing*/
  }
  motorDir = my_serial.parseInt();
  if (motorDir < 1 || motorDir > 6) {
    my_serial.println("  ");
    my_serial.print("              ******* Invalid Input, ");
    my_serial.println(" *******");
    my_serial.println("          ******* Choose Desired Operation *******");
    my_serial.println("  ");
  }

  else if (motorDir == 1) {  // Grating will rotate CW for a positive input
    my_serial.println(" ");
    my_serial.println("     Grating will rotate CW for a positive input (default)");
    my_serial.println(" ");
    gratingDirCode = 1;
  } else if (motorDir == 2) {  // Grating will rotate CCW for a negative input
    my_serial.println(" ");
    my_serial.println("     Grating will rotate CCW for a positive input (reverse)");
    my_serial.println(" ");
    gratingDirCode = 0;
  }

  else if (motorDir == 3) {  // Collimating lens moves CW for a positive input
    my_serial.println(" ");
    my_serial.println("     Collimating lens moves closer to the grating for a positive input (default)");
    my_serial.println(" ");
    focusDirCode = 1;
  } else if (motorDir == 4) {  // Grating will rotate CCW for a negative input
    my_serial.println(" ");
    my_serial.println("     Collimating lens moves away from the grating for a negative input (reverse)");
    my_serial.println(" ");
    focusDirCode = 0;
  }

  else if (motorDir == 5) {  // Both collimating lens and grating holder set to default
    my_serial.println(" ");
    my_serial.println("     Grating will rotate CW for a positive input (default)");
    my_serial.println("     Collimating lens moves closer to the grating for a positive input (default)");
    my_serial.println(" ");
    gratingDirCode = 1;
    focusDirCode = 1;
  } else if (motorDir == 6) {  // Both collimating lens and graing holder set to reverse
    my_serial.println(" ");
    my_serial.println("     Grating will rotate CCW for a positive input (reverse)");
    my_serial.println("     Collimating lens moves closer to the grating for a negative input (reverse)");
    my_serial.println(" ");
    gratingDirCode = 0;
    focusDirCode = 0;
  }

  write2BytesIntIntoEEPROM(gratingDirAddress, gratingDirCode);
  gratingDir = read2BytesFromEEPROM(gratingDirAddress);

  write2BytesIntIntoEEPROM(focusDirAddress, focusDirCode);
  focusDir = read2BytesFromEEPROM(focusDirAddress);

  break;

  //  ===============================================================================================
case 'W':
case 'w':

  POR = 1;

  grating_mm = read2BytesFromEEPROM(configurationAddress);

  my_serial.println(" ");
  my_serial.print("grating lines / mm  = ");
  my_serial.println(grating_mm);

  my_serial.println(" ");
  my_serial.println("Enter The Desired Central Wavelength in Angstroms");
  my_serial.println(" ");

  if (homed == 0) {
    my_serial.println("Not Homed Yet");
    my_serial.println("This Will Home The Unit Before You Enter Wavelength");
    my_serial.println(" ");
    my_serial.println("Go Ahead And Enter The Desired Wavelength In Angstroms");
    homing();
  }
  while (my_serial.available() == 0) { /*do nothing*/
  }

  wavelength = my_serial.parseInt();

  my_serial.print("Wavelength entered in Angstroms = ");
  my_serial.println(int(wavelength));

  if (wavelength < minimum || wavelength > maximum) {
    my_serial.print("******* Invalid Input, Choose Desired Operation *******");

    break;
  } else {

    //$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    //                                             Motor gear ration + printed gear ratio = .03515625 / degree
    //                                                 (28BYJ-48 5.625 deg / 64 printed gear ratio 2.5:1)
    //                                                            for 300line/mm  .0093x-22.508
    //                                                            for 600line/mm  .0189x-22.621
    //                                                            for 900line/mm  .0291x-22.92

    //    Example for 600 line grating
    // The grating incident angle is -22.5 degrees at home position. If the desired wavelength is set to 4000 angstroms the incident angle is -15.06 degrees
    // The angle of the grating needs to be -22.5 - (-15.06) = -7.44 degrees less than the angle at home.
    //-22.5/.03515625 steps/degree = 640 steps
    //-15.06/.03515625 steps/degree = 428 steps
    // The motor needs to move 640 - 428 = 212 steps to get to the desired incedince angle
    // It can also be calculated as 7.44/.03515625/degree which also = 212 steps

    my_serial.print("wavelength = ");
    my_serial.print(int(wavelength));
    my_serial.print("   ---  with ");
    my_serial.print(read2BytesFromEEPROM(configurationAddress));
    my_serial.println(" line grating");

    int stepsToMove;
    int numberSteps;
    float gearRatio = .03515625;

    if (grating_mm == 300) {
      result = ((.0093 * (wavelength / 10)) - 22.508);  // Calculate number of steps required to set desired central wavelength with 300 l/mm

    } else if (grating_mm == 600) {
      result = ((.0189 * (wavelength / 10)) - 22.621);  // Calculate number of steps required to set desired central wavelength with 600 l/mm

    } else {
      if (grating_mm == 900) {
        result = ((.0291 * (wavelength / 10)) - 22.92);  // Calculate number of steps required to set desired central wavelength with 900 l/mm
      }
    }

    numberSteps = (result / gearRatio);

    if (stepHist == 0) {

      stepsToMove = (640 - abs(numberSteps));  //-22.5 degrees = -640 steps at home

      stepHist = numberSteps;

    } else {
      stepsToMove = (int(result / gearRatio - stepHist));

      stepHist = numberSteps;
    }

    gratSteps = stepsToMove;

    if (gratSteps > 0) {
      CW = 1;
    }

    else {
      CW = 0;
    }

    while (gsteps < abs(gratSteps)) {
      term = 8;  // This is used to terminate the following for loop
      // when the number of required steps has been reached

      for (int phase = 0; phase < term; phase++) {

        if (CW > 0) {
          if (gratingDir == 1) {
            // Shift output the bits for CW rotation
            Wire.beginTransmission(0x21);  // transmit to device #44 (0x2c)
            // device address is specified in datasheet
            Wire.write(byte(0x02));         // sends instruction byte
            Wire.write(dataArray3[phase]);  // sends phase value byte
            Wire.write(dataArray3[phase]);  // sends phase value byte
            Wire.endTransmission();

          } else {
            // Shift output the bits for CCW rotation
            Wire.beginTransmission(0x21);  // transmit to device #44 (0x2c)
            // device address is specified in datasheet
            Wire.write(byte(0x02));         // sends instruction byte
            Wire.write(dataArray4[phase]);  // sends phase value byte
            Wire.write(dataArray4[phase]);  // sends phase value byte
            Wire.endTransmission();
          }
        }

        else {
          if (gratingDir == 1) {
            // Shift output the bits for CCW rotation
            Wire.beginTransmission(0x21);  // transmit to device #44 (0x2c)
            // device address is specified in datasheet
            Wire.write(byte(0x02));         // sends instruction byte
            Wire.write(dataArray4[phase]);  // sends phase value byte
            Wire.write(dataArray4[phase]);  // sends phase value byte
            Wire.endTransmission();

          } else {
            // Shift output the bits for CW rotation
            Wire.beginTransmission(0x21);  // transmit to device #44 (0x2c)
            // device address is specified in datasheet
            Wire.write(byte(0x02));         // sends instruction byte
            Wire.write(dataArray3[phase]);  // sends phase value byte
            Wire.write(dataArray3[phase]);  // sends phase value byte
            Wire.endTransmission();
          }
        }

        delay(dly);

        gsteps++;

        if (CW == 1) {
          gratPosition = gratPosition + 1;  //increase the position if motor is running CW
        } else {
          gratPosition = gratPosition - 1;  //decrease the position if motor is running CCW
        }

        if (gsteps >= abs(gratSteps)) {
          term = 0;  // This breaks us out of the for loop when done with requested steps

          gratStepHist = gratStepHist + gsteps;
          gratPhaseHist = phase;

          Wire.beginTransmission(0x21);  // transmit to device #44 (0x2c)
          // device address is specified in datasheet
          Wire.write(byte(0x02));  // sends instruction byte
          Wire.write(0x00);        // turns off motors to prevent heating
          Wire.write(0x00);        // turns off motors to prevent heating
          Wire.endTransmission();

          Wire.beginTransmission(0x21);  // transmit to device #44 (0x2c)
          // device address is specified in datasheet
          Wire.write(byte(0x06));  // sends instruction byte
          Wire.write(0x00);        // turns off motors to prevent heating
          Wire.write(0x00);        // turns off motors to prevent heating
          Wire.endTransmission();

          my_serial.println(" ");

          if (grating_mm == 300) {
            my_serial.print("Current wavelength setting      ");
            my_serial.print(int(10 * (result + 22.508) / .0093));
            my_serial.println(" Angstroms");
          }

          else if (grating_mm == 600) {
            my_serial.print("Current wavelength setting      ");
            my_serial.print(int(10 * (result + 22.621) / .0189));
            my_serial.println(" Angstroms");
          }

          else if (grating_mm == 900) {
            my_serial.print("Current wavelength setting      ");
            my_serial.print(int(10 * (result + 22.92) / .0291));
            my_serial.println(" Angstroms");
          }
        }
      }
    }
  }

  if (CW == 1)  // If CW motion the break will be executed
  {
    break;
  } else {
    steps = 0;
  }

  //=========================================================
  // This routine will be used to eliminate backlash
  // it will continue driving in the CCW and then turn CW back to starting Position
  // this will always drive in a CW direction to the desired Position
  //=========================================================
  gratSteps = 200;  // each directions will go 1/2 this many steps

  CW = 0;
  gratStatus = 0;
  gsteps = 0;
  while (gsteps < abs(gratSteps)) {
    for (int phase = 0; phase < 8; phase++) {

      if (CW == 1) {
        if (gratingDir == 1) {
          // Shift output the bits for CW rotation
          Wire.beginTransmission(0x21);  // transmit to device #44 (0x2c)
          // device address is specified in datasheet
          Wire.write(byte(0x02));         // sends instruction byte
          Wire.write(dataArray3[phase]);  // sends phase value byte
          Wire.write(dataArray3[phase]);  // sends phase value byte
          Wire.endTransmission();

        } else {
          // Shift output the bits for CCW rotation
          Wire.beginTransmission(0x21);  // transmit to device #44 (0x2c)
          // device address is specified in datasheet
          Wire.write(byte(0x02));         // sends instruction byte
          Wire.write(dataArray4[phase]);  // sends phase value byte
          Wire.write(dataArray4[phase]);  // sends phase value byte
          Wire.endTransmission();
        }
      } else {
        if (gratingDir == 1) {
          // Shift output the bits for CCW rotation
          Wire.beginTransmission(0x21);  // transmit to device #44 (0x2c)
          // device address is specified in datasheet
          Wire.write(byte(0x02));         // sends instruction byte
          Wire.write(dataArray4[phase]);  // sends phase value byte
          Wire.write(dataArray4[phase]);  // sends phase value byte
          Wire.endTransmission();

        } else {
          // Shift output the bits for CW rotation
          Wire.beginTransmission(0x21);  // transmit to device #44 (0x2c)
          // device address is specified in datasheet
          Wire.write(byte(0x02));         // sends instruction byte
          Wire.write(dataArray3[phase]);  // sends phase value byte
          Wire.write(dataArray3[phase]);  // sends phase value byte
          Wire.endTransmission();
        }
      }

      delay(dly);

      gsteps = gsteps + 1;

      if (CW == 1) {
        gratPosition = gratPosition + 1;
        gratStatus = gratStatus + 1;
      } else {
        gratPosition = gratPosition - 1;
        gratStatus = gratStatus - 1;
      }

      if (gsteps > (abs(gratSteps) / 2) - 1) {
        CW = 1;
      }
      delay(dly);

      if (gsteps >= abs(gratSteps)) {
        gratStepHist = gratStepHist + gsteps;
        gratPhaseHist = phase;

        Wire.beginTransmission(0x21);  // transmit to device #44 (0x2c)
        // device address is specified in datasheet
        Wire.write(byte(0x02));  // sends instruction byte
        Wire.write(0x00);        // turns off motors to prevent heating
        Wire.write(0x00);        // turns off motors to prevent heating
        Wire.endTransmission();

        Wire.beginTransmission(0x21);  // transmit to device #44 (0x2c)
        // device address is specified in datasheet
        Wire.write(byte(0x06));  // sends instruction byte
        Wire.write(0x00);        // turns off motors to prevent heating
        Wire.write(0x00);        // turns off motors to prevent heating
        Wire.endTransmission();
      }
    }
  }
  break;
  //===================================================================================
case 'H':
case 'h':

  homing();

  break;
  //===================================================================================
case 'M':
case 'm':

  resetFocus();

  break;

  //===================================================================================
case 'F':
case 'f':

  my_serial.println(" ");

  my_serial.print("enter the % of collimating lens travel from +/- 0 to 100% ");
  my_serial.println(" ");

  // This will move the collimation lens in equal linear steps from +/- 0 to 100%
  // of the lens travel. Full travel of 1.5 mm total and 0.75 mm in each direction.
  // This will move the lens to an absolute location, not incremental movements.
  // each time an adjustment is made it will be recorded in EEPROM so the desired
  // location can be entered after a power on reset.

  // If the large part of the cam lobe is away from the science camera at location "0"
  // a positive % input value will move the collimating lens closer to the grating.

  focusPosition = read2BytesFromEEPROM(focusAddress);

  if (negativeFlag == 1) {
    focusPosition = -1 * focusPosition;
  }

  while (my_serial.available() == 0) {
    /*do nothing*/
  }
  colLocation = my_serial.parseInt();

  my_serial.println(" ");
  my_serial.print("Collimating lens location Requested = ");
  my_serial.print(colLocation);
  my_serial.println("%");
  write2BytesIntIntoEEPROM(inputAddress, colLocation);

  if (colLocation > -101 && colLocation < 101) {
    if (colLocation < 0) {
      write2BytesIntIntoEEPROM(negativeAddress, 1);
      delay(5);
      negativeFlag = read2BytesFromEEPROM(negativeAddress);
    } else {
      write2BytesIntIntoEEPROM(negativeAddress, 0);
      delay(5);

      negativeFlag = read2BytesFromEEPROM(negativeAddress);
      tempNegativeFlag = negativeFlag;  //capture the old flag before negativeFlag gets reset
    }

    colPos = (90 - colLocation * .9);  // this converts input of +/- 100 to 0 to 90 degrees of rotation

    inputSteps = int(1024 - (1024 * cos(radians(90 - colPos))));  // calculates number of steps to achieve desired distance to move

    if (negativeFlag == 1) {
      inputSteps = (inputSteps * -1);
    }

    lastPosition = read2BytesFromEEPROM(focusAddress);  // read last focus position from EEPROM

    if (negFlagHist == 1) {
      lastPosition = (-1 * lastPosition);
    }

    negFlagHist = negativeFlag;

    write2BytesIntIntoEEPROM(negativeAddress, negativeFlag);
    delay(5);

    write2BytesIntIntoEEPROM(focusAddress, (abs(inputSteps)));
    delay(5);

    colSteps = inputSteps - lastPosition;

    if (colSteps > 0) {
      CW = 1;

    } else {
      CW = 0;
    }

    while (steps < abs(colSteps)) {
      term = 8;  // This is used to terminate the following for loop
      // when the number of required steps has been reached

      for (int phase = 0; phase < term; phase++) {

        if (CW > 0) {
          if (focusDir == 1) {
            // Shift output the bits for CW rotation
            Wire.beginTransmission(0x21);  // transmit to device #44 (0x2c)
            // device address is specified in datasheet
            Wire.write(byte(0x02));         // sends instruction byte
            Wire.write(dataArray1[phase]);  // sends phase value byte
            Wire.write(dataArray1[phase]);  // sends phase value byte
            Wire.endTransmission();

          } else {
            // Shift output the bits for CCW rotation
            Wire.beginTransmission(0x21);  // transmit to device #44 (0x2c)
            // device address is specified in datasheet
            Wire.write(byte(0x02));         // sends instruction byte
            Wire.write(dataArray2[phase]);  // sends phase value byte
            Wire.write(dataArray2[phase]);  // sends phase value byte
            Wire.endTransmission();
           }
        } else {
          if (focusDir == 1) {
            // Shift output the bits for CCW rotation
            Wire.beginTransmission(0x21);  // transmit to device #44 (0x2c)
            // device address is specified in datasheet
            Wire.write(byte(0x02));         // sends instruction byte
            Wire.write(dataArray2[phase]);  // sends phase value byte
            Wire.write(dataArray2[phase]);  // sends phase value byte
            Wire.endTransmission();
          } else {
            // Shift output the bits for CW rotation
            Wire.beginTransmission(0x21);  // transmit to device #44 (0x2c)
            // device address is specified in datasheet
            Wire.write(byte(0x02));         // sends instruction byte
            Wire.write(dataArray1[phase]);  // sends phase value byte
            Wire.write(dataArray1[phase]);  // sends phase value byte
            Wire.endTransmission();
          }
        }

        delay(dly);

        steps = steps + 1;

        if (CW == 1) {
          focusPosition = focusPosition + 1;  //increase the position if motor is running CW
        } else {
          focusPosition = focusPosition - 1;  //decrease the position if motor is running CCW
        }

        if (steps >= abs(colSteps)) {
          term = 0;  // This breaks us out of the for loop when done with requested steps

          colPhaseHist = phase;

          Wire.beginTransmission(0x21);  // transmit to device #44 (0x2c)
          // device address is specified in datasheet
          Wire.write(byte(0x02));  // sends instruction byte
          Wire.write(0x00);        // turns off motors to prevent heating
          Wire.write(0x00);        // turns off motors to prevent heating
          Wire.endTransmission();

          Wire.beginTransmission(0x21);  // transmit to device #44 (0x2c)
          // device address is specified in datasheet
          Wire.write(byte(0x06));  // sends instruction byte
          Wire.write(0x00);        // turns off motors to prevent heating
          Wire.write(0x00);        // turns off motors to prevent heating
          Wire.endTransmission();
        }
      }
    }

    if (CW == 1)  // If CW motion the break will be executed
    {
      break;
    } else {
      steps = 0;
    }

    //=========================================================
    // This routine will be used to eliminate backlash
    // it will continue driving in the CCW and then turn CW back to starting Position
    // this will always drive in a CW direction to the desired Position
    //=========================================================

    colSteps = 400;  // each directions will go 1/2 this many steps

    CW = 0;

    while (steps < abs(colSteps)) {
      for (int phase = 0; phase < 8; phase++) {

        if (CW == 1) {
          if (focusDir == 1) {

            // Shift output the bits for CW rotation
            Wire.beginTransmission(0x21);  // transmit to device #44 (0x2c)
            // device address is specified in datasheet
            Wire.write(byte(0x02));         // sends instruction byte
            Wire.write(dataArray1[phase]);  // sends phase value byte
            Wire.write(dataArray1[phase]);  // sends phase value byte
            Wire.endTransmission();
          } else {
            // Shift output the bits for CCW rotation
            Wire.beginTransmission(0x21);  // transmit to device #44 (0x2c)
            // device address is specified in datasheet
            Wire.write(byte(0x02));         // sends instruction byte
            Wire.write(dataArray2[phase]);  // sends phase value byte
            Wire.write(dataArray2[phase]);  // sends phase value byte
            Wire.endTransmission();
          }
        } else {
          if (focusDir == 1) {
            // Shift output the bits for CCW rotation
            Wire.beginTransmission(0x21);  // transmit to device #44 (0x2c)
            // device address is specified in datasheet
            Wire.write(byte(0x02));         // sends instruction byte
            Wire.write(dataArray2[phase]);  // sends phase value byte
            Wire.write(dataArray2[phase]);  // sends phase value byte
            Wire.endTransmission();

          } else {
            // Shift output the bits for CW rotation
            Wire.beginTransmission(0x21);  // transmit to device #44 (0x2c)
            // device address is specified in datasheet
            Wire.write(byte(0x02));         // sends instruction byte
            Wire.write(dataArray1[phase]);  // sends phase value byte
            Wire.write(dataArray1[phase]);  // sends phase value byte
            Wire.endTransmission();
          }
        }

        delay(dly);

        steps++;
        if (CW == 1) {
          focusPosition = focusPosition + 1;
        } else {
          focusPosition = focusPosition - 1;
        }

        if (steps > (abs(colSteps) / 2) - 1) {
          CW = 1;
        }
        delay(dly);

        if (steps >= abs(colSteps)) {
          colPhaseHist = phase;

          Wire.beginTransmission(0x21);  // transmit to device #44 (0x2c)
          // device address is specified in datasheet
          Wire.write(byte(0x02));  // sends instruction byte
          Wire.write(0x00);        // turns off motors to prevent heating
          Wire.write(0x00);        // turns off motors to prevent heating
          Wire.endTransmission();

          Wire.beginTransmission(0x21);  // transmit to device #44 (0x2c)
          // device address is specified in datasheet
          Wire.write(byte(0x06));  // sends instruction byte
          Wire.write(0x00);        // turns off motors to prevent heating
          Wire.write(0x00);        // turns off motors to prevent heating
          Wire.endTransmission();
        }
      }
    }
  } else {
    my_serial.println(" ");
    my_serial.print(" --- invalid entry, please enter a valid command --- ");
  }

  break;

  //===================================================================================
case 'Q':
case 'q':  // This gives current status of the spectrometer

  my_serial.println(" ");
  my_serial.print("    Arduino Code version V");
  my_serial.println(CodeVersion);

  my_serial.print("       Code Date ");
  my_serial.println(CodeDate);

  my_serial.println("      GitHub Code Location ");
  my_serial.println(CodeLocation);

  my_serial.println(" ");
  my_serial.println("      Spectrometer status ");
  my_serial.println("    ====================== ");

  grating_mm = read2BytesFromEEPROM(configurationAddress);
  my_serial.print("grating lines per mm               ");
  my_serial.println(grating_mm);

  my_serial.print("zeroOrderOffset ------------------ ");
  my_serial.println(zeroOrderOffset);

  if (POR == 1)
  {
    if (grating_mm == 300) {
      my_serial.print("Current wavelength setting         ");
      my_serial.print(int(10 * (result + 22.508) / .0093));
      my_serial.println(" Angstroms");
    }

    else if (grating_mm == 600) {
      my_serial.print("Current wavelength setting         ");
      my_serial.print(int(10 * (result + 22.621) / .0189));
      my_serial.println(" Angstroms");
    }

    else if (grating_mm == 900) {
      my_serial.print("Current wavelength setting         ");
      my_serial.print(int(10 * (result + 22.92) / .0291));
      my_serial.println(" Angstroms");
    }
  }
  else
  {
    my_serial.print("Current wavelength setting         ");
    my_serial.print(" ? ");
    my_serial.println(" Angstroms");
  }

  my_serial.print("Grating motor direction ");
  if (read2BytesFromEEPROM(gratingDirAddress) == 1) {
    my_serial.println(" --------- Default ");
  } else {
    my_serial.println(" --------- Reverse");
  }

  my_serial.print("Focus motor direction ");
  if (read2BytesFromEEPROM(focusDirAddress) == 1) {
    my_serial.println("             Default ");
  } else {
    my_serial.println("             Reverse");
  }


  my_serial.print("Current Focus Position from 0 ---- ");
  input = read2BytesFromEEPROM(inputAddress);
  tempNegativeFlag = read2BytesFromEEPROM(negativeAddress);

  if (tempNegativeFlag == 1) {
    my_serial.print("-");
    my_serial.print(65536 - input);
    my_serial.println(" %");
  } else {
    my_serial.print(input);
    my_serial.println(" %");
  }

  my_serial.print("current jog position               ");
  my_serial.print(zeroPosition);
  my_serial.println("  steps");

  if (shutterStatus == 1)
    my_serial.println("Shutter Is ----------------------- Open");

  else {
    my_serial.println("Shutter Is ----------------------- Closed");
  }

  if (cal == 1) {
    my_serial.println("Calibration Lamp                   On");
  } else {
    my_serial.println("Calibration Lamp                   Off");
  }

  if (int(100 * redPWM / 255) > 0) {
    my_serial.print("Red LED -------------------------- ");
    my_serial.print(int(100 * redPWM / 255));
    my_serial.println(" %");
  } else {
    my_serial.println("Red LED -------------------------- Off");
  }

  if (green == 1) {
    my_serial.println("green LED                          On");
  } else {
    my_serial.println("green LED                          Off");
  }


  if (blue == 1) {
    my_serial.println("Blue LED ------------------------- On");
  } else {
    my_serial.println("Blue LED ------------------------- Off");
  }

  if (int(100 * UVPWM / 255) > 0) {
    my_serial.print("UV boost LED                       ");
    my_serial.print(int(100 * UVPWM / 255));
    my_serial.println(" %");
  } else {
    my_serial.println("UV boost LED                       Off");
  }

  if (int(100 * flatPWM / 255) > 0) {
    my_serial.print("flat LED ------------------------- ");
    my_serial.print(int(100 * flatPWM / 255));
    my_serial.println(" %");
  } else {
    my_serial.println("flat LED ------------------------- Off");
  }

  if (int(100 * GowPWM / 255) > 0) {
    my_serial.print("Incandescent lamp                  ");
    my_serial.print(int(100 * GowPWM / 255));
    my_serial.println(" %");
  } else {
    my_serial.println("Incandescent lamp                  Off");
  }

  if (slit == 1) {
    my_serial.println("slit backlight illuminator ------- On");
  } else {
    my_serial.println("slit backlight illuminator ------- Off");
  }


  break;

  //===================================================================================
case 'N':
case 'n':

  cal = cal * -1;
  if (cal == 1) {
    digitalWrite(calLamp, HIGH);
    my_serial.print("Calibration Lamp Is On");
  } else {
    digitalWrite(calLamp, LOW);
    my_serial.print("Calibration Lamp Is Off");
  }
  break;
  //===================================================================================
case 'I':
case 'i':

  my_serial.println(" ");
  my_serial.print(" Enter Requested incandescent Intensity 0-100%");
  my_serial.println(" ");
  while (my_serial.available() == 0) {
    /*do nothing*/
  }
  GowPWMnew = (my_serial.parseInt());
  if (GowPWMnew >= 0 && GowPWMnew < 101) {
    GowPWM = GowPWMnew / 100 * 255;
    my_serial.println(" ");
    my_serial.print(" Requested Intensity = ");
    my_serial.print(GowPWMnew);
    my_serial.println(" % ");

    if (GowPWM > 0) {
      analogWrite(incandescentLamp, GowPWM);
      my_serial.println(" ");
      my_serial.print("Incandescent Lamp Is on at Intensity = ");
      my_serial.print(100 * GowPWM / 255);
      my_serial.println(" %");
    } else {
      analogWrite(incandescentLamp, 0);
      my_serial.println(" ");
      my_serial.print("Incandescent Lamp Is Off");
    }
  } else {
    my_serial.println(" ");
    my_serial.println("******* Invalid PWM Value Entered *******");
    my_serial.println("*******  Select a valid function  *******");

    break;
  }

  break;

  //===================================================================================
case 'L':
case 'l':

  my_serial.println(" ");
  my_serial.print(" Enter Requested Flat LED Intensity 0-100%");
  my_serial.println(" ");
  while (my_serial.available() == 0) {
    /*do nothing*/
  }
  flatPWMnew = my_serial.parseInt();
  if (flatPWMnew >= 0 && flatPWMnew < 101) {
    flatPWM = flatPWMnew / 100 * 255;
    my_serial.println(" ");
    my_serial.print(" Requested Flat LED Intensity = ");
    my_serial.print(flatPWMnew);
    my_serial.println(" ");

    if (flatPWM > 0) {
      analogWrite(flatLED, flatPWM);
      my_serial.println(" ");
      my_serial.print("flat LED Intensity = ");
      my_serial.print(100 * flatPWM / 255);
      my_serial.println("%");
    } else {
      analogWrite(flatLED, 0);
      my_serial.println(" ");
      my_serial.print("Flat LED Is Off");
    }
  } else {
    my_serial.println(" ");
    my_serial.println("******* Invalid PWM Value Entered *******");
    my_serial.println("*******  Select a valid function  *******");

    break;
  }

  break;

  //===================================================================================
case 'R':
case 'r':

  my_serial.println(" ");
  my_serial.print(" Enter Requested Red LED Intensity 0-100%");
  my_serial.println(" ");
  while (my_serial.available() == 0) {
    /*do nothing*/
  }
  redPWMnew = my_serial.parseInt();
  if (redPWMnew >= 0 && redPWMnew < 101) {
    redPWM = redPWMnew / 100 * 255;
    my_serial.println(" ");
    my_serial.print(" Requested Red LED Intensity = ");
    my_serial.print(redPWMnew);
    my_serial.println("%");

    if (redPWM > 0) {
      analogWrite(redLED, redPWM);
      my_serial.println(" ");
      my_serial.print("Red LED Is On At Intensity = ");
      my_serial.print(100 * redPWM / 255);
      my_serial.print("%");
    } else {
      analogWrite(redLED, 0);
      my_serial.println(" ");
      my_serial.print("Red LED Is Off");
    }
  } else {
    my_serial.println(" ");
    my_serial.println("******* Invalid PWM Value Entered *******");
    my_serial.println("*******  Select a valid function  *******");

    break;
  }

  break;

  //===================================================================================
case 'U':
case 'u':

  my_serial.println(" ");
  my_serial.print(" Enter Requested UV-boost LED Intensity 0-100%");
  my_serial.println(" ");
  while (my_serial.available() == 0) {
    /*do nothing*/
  }
  UVPWMnew = my_serial.parseInt();
  if (UVPWMnew >= 0 && UVPWMnew < 101) {
    UVPWM = UVPWMnew / 100 * 255;
    my_serial.println(" ");
    my_serial.print(" Requested UV-boost LED Intensity = ");
    my_serial.print(UVPWMnew);
    my_serial.println("%");

    if (UVPWM > 0) {
      analogWrite(UVBoostLED, UVPWM);
      my_serial.println(" ");
      my_serial.print("UV-boost LED Is On At Intensity = ");
      my_serial.print(100 * UVPWM / 255);
      my_serial.print("%");
    } else {
      analogWrite(UVBoostLED, 0);
      my_serial.println(" ");
      my_serial.print("UV-boost LED Is Off");
    }
  } else {
    my_serial.println(" ");
    my_serial.println("******* Invalid PWM Value Entered *******");
    my_serial.println("*******  Select a valid function  *******");

    break;
  }

  break;

  //===================================================================================
case 'B':
case 'b':

  blue = blue * -1;
  if (blue == 1) {
    digitalWrite(blueLED, HIGH);
    my_serial.println(" ");
    my_serial.print("Blue Marker Is On");
  } else {
    digitalWrite(blueLED, LOW);
    my_serial.println(" ");
    my_serial.print("Blue Marker Is Off");
  }
  break;

  //===================================================================================
case 'V':
case 'v':

  slit = slit * -1;
  if (slit == 1) {
    digitalWrite(slitLED, HIGH);
    my_serial.println(" ");
    my_serial.print("slit illuminator Is On");
  } else {
    digitalWrite(slitLED, LOW);
    my_serial.println(" ");
    my_serial.print("slit illuminator Is Off");
  }
  break;

  //===================================================================================
case 'G':
case 'g':

  green = green * -1;
  if (green == 1) {
    digitalWrite(greenLED, HIGH);
    my_serial.println(" ");
    my_serial.print("green Market Is On");
  } else {
    digitalWrite(greenLED, LOW);
    my_serial.println(" ");
    my_serial.print("green Marker Is Off");
  }
  break;

  //===================================================================================
case 'O':
case 'o':

  my_serial.println(" ");
  my_serial.println("All Lamps Have Been Turned Off");

  digitalWrite(calLamp, LOW);        // turn off the calibration lamp
  cal = -1;                          // setup to toggle next on command
  analogWrite(incandescentLamp, 0);  // turn off the incandescent grain of wheat lamp
  GowPWM = 0;
  analogWrite(slitLED, 0);          // turn off slit illuminator
  slit = -1;                        // setup to toggle next on command
  digitalWrite(blueLED, LOW);      // turn off the blue marker
  blue = -1;                       // setup to toggle next on command
  digitalWrite(greenLED, LOW);     // turn off the green marker
  green = -1;                      // setup to toggle next on command
  analogWrite(UVBoostLED, 0);      // turn off the UV boost LEDs
  UVPWM = 0;
  analogWrite(flatLED, 0);  // turn off the flat LEDs
  flatPWM = 0;
  analogWrite(redLED, 0);  // turn off the red marker
  redPWM = 0;

  break;

  //===================================================================================
case 'S':
case 's':

  shutterServo.attach(servoPin);  // This activates the shutter servo
  posHist = read2BytesFromEEPROM(posAddress);

  if (shutterStatus == -1) {
    for (pos = posHist; pos >= shutterOpen; pos -= 3)  // moves in 1 degree steps to control speed
      // moves shutter to the open position
    {
      shutterServo.write(pos);  // tell servo to go to position in variable 'pos'
      delay(servo_delay);       // waits for the servo to reach the position
    }
    shutterServo.detach();  // This turns off the shutter servo after opening the shutter
    my_serial.print("Shutter Is Open");
    shutterStatus = 1;
  }

  else {
    for (pos = posHist; pos <= shutterClosed; pos += 3)  // moves in 1 degree steps to control speed
      // moves shutter to the open position
    {
      shutterServo.write(pos);  // tell servo to go to position in variable 'pos'
      delay(servo_delay);       // waits for the servo to reach the position
    }
    shutterServo.detach();  // This turns off the shutter servo after closing the shutter
    my_serial.print("Shutter Is Closed ");
    shutterStatus = -1;
  }
  write2BytesIntIntoEEPROM(posAddress, pos);  //Initialize grating motor direction to default
  posHist = read2BytesFromEEPROM(posAddress);

  break;

  //===================================================================================
case 'J':
case 'j':

  my_serial.println("  ");
  my_serial.println("enter the number of desired offset steps");
  my_serial.println("  ");

  while (my_serial.available() == 0) {
    /*do nothing*/
  }
  delay(enterTime);
  RequestedSteps = my_serial.parseInt();

  zOrderSteps = 0;

  if (RequestedSteps < minSteps || RequestedSteps > maxSteps) {
    my_serial.print("RequestedSteps = ");
    my_serial.println(RequestedSteps);
    my_serial.println("  ");
    my_serial.println("  ");
    my_serial.print("******* Invalid Input, Total Position Exceeds");
    my_serial.print(minSteps);
    my_serial.print(" or ");
    my_serial.print(maxSteps);
    my_serial.println(" *******");
    my_serial.print("                  Current Position = ");
    my_serial.println(zeroPosition);
    my_serial.println("          ******* Choose Desired Operation *******");
    my_serial.println("  ");
    my_serial.println("  ");
    break;
  }
  my_serial.print("Number of Steps Requested = ");
  my_serial.println(RequestedSteps);
  my_serial.println(" ");
  my_serial.print("Number of Steps Taken = ");
  my_serial.print(RequestedSteps);
  my_serial.println("  ");
  my_serial.println("  ");

  zPhase = PhaseHist;

  if (RequestedSteps > 0) {
    CW = 1;
  } else {
    CW = 0;
    RequestedSteps = RequestedSteps - BkLashCount;
  }

  //*****This turns on the motor to the last know motor drive phase so X number of steps can be taken from there *****

  if (gratingDir == 1) {
    // Shift output the bits for CW rotation
    Wire.beginTransmission(0x21);  // transmit to device #44 (0x2c)
    // device address is specified in datasheet
    Wire.write(byte(0x02));             // sends instruction byte
    Wire.write(dataArray3[PhaseHist]);  // sends PhaseHist value byte
    Wire.write(dataArray3[PhaseHist]);  // sends PhaseHist value byte
    Wire.endTransmission();


  } else {
    // Shift output the bits for CCW rotation
    Wire.beginTransmission(0x21);  // transmit to device #44 (0x2c)
    // device address is specified in datasheet
    Wire.write(byte(0x02));             // sends instruction byte
    Wire.write(dataArray4[PhaseHist]);  // sends PhaseHist value byte
    Wire.write(dataArray4[PhaseHist]);  // sends PhaseHist value byte
    Wire.endTransmission();
  }

  delay(dly);

  //*****This will start the desired number of steps from the last know motor phase *****

  if (CW == 0) {
    zPhase = zPhase - 1;  //this will start desired CW steps from one phase after the last know phase
    if (zPhase < 0) {
      zPhase = 7;
    }
  } else {
    zPhase = zPhase + 1;
    if (zPhase >= 8) {
      zPhase = 0;
    }
  }

  while (zOrderSteps < abs(RequestedSteps)) {
    if (CW == 0) {
      term = -1;  // This is used to terminate the following for loop
      // when the number of required steps has been reached
    } else {
      term = 8;
    }

    if (CW == 0) {
      for (stepperPhase = zPhase; stepperPhase > term; stepperPhase--) {

        if (CW == 0) {
          if (gratingDir == 1) {

            // Shift output the bits for CW rotation
            Wire.beginTransmission(0x21);  // transmit to device #44 (0x2c)
            // device address is specified in datasheet
            Wire.write(byte(0x02));                // sends instruction byte
            Wire.write(dataArray3[stepperPhase]);  // sends stepper Phase value byte
            Wire.write(dataArray3[stepperPhase]);  // sends stepper Phase value byte
            Wire.endTransmission();

          } else {
            // Shift output the bits for CCW rotation
            Wire.beginTransmission(0x21);  // transmit to device #44 (0x2c)
            // device address is specified in datasheet
            Wire.write(byte(0x02));                // sends instruction byte
            Wire.write(dataArray4[stepperPhase]);  // sends stepper Phase value byte
            Wire.write(dataArray4[stepperPhase]);  // sends stepper Phase value byte
            Wire.endTransmission();
          }
        }

        delay(dly);

        zOrderSteps++;

        zeroPosition--;  //increase the position if motor is running CW

        zPhase = 7;

        if (zOrderSteps >= abs(RequestedSteps)) {
          term = 8;  // This breaks us out of the for loop when done with requested steps

          PhaseHist = stepperPhase;

          delay(dly);

          Wire.beginTransmission(0x21);  // transmit to device #44 (0x2c)
          // device address is specified in datasheet
          Wire.write(byte(0x02));  // sends instruction byte
          Wire.write(0x00);        // turns off motors to prevent heating
          Wire.write(0x00);        // turns off motors to prevent heating
          Wire.endTransmission();

          Wire.beginTransmission(0x21);  // transmit to device #44 (0x2c)
          // device address is specified in datasheet
          Wire.write(byte(0x06));  // sends instruction byte
          Wire.write(0x00);        // turns off motors to prevent heating
          Wire.write(0x00);        // turns off motors to prevent heating
          Wire.endTransmission();
        }
      }
    }

    // below is for CW = 1

    else {
      for (stepperPhase = zPhase; stepperPhase < term; stepperPhase++) {

        if (gratingDir == 1) {
          // Shift output the bits for CW rotation
          Wire.beginTransmission(0x21);  // transmit to device #44 (0x2c)
          // device address is specified in datasheet
          Wire.write(byte(0x02));                // sends instruction byte
          Wire.write(dataArray3[stepperPhase]);  // sends stepper Phase value byte
          Wire.write(dataArray3[stepperPhase]);  // sends stepper Phase value byte
          Wire.endTransmission();

        } else {
          // Shift output the bits for CCW rotation
          Wire.beginTransmission(0x21);  // transmit to device #44 (0x2c)
          // device address is specified in datasheet
          Wire.write(byte(0x02));                // sends instruction byte
          Wire.write(dataArray4[stepperPhase]);  // sends stepper Phase value byte
          Wire.write(dataArray4[stepperPhase]);  // sends stepper Phase value byte
          Wire.endTransmission();
        }

        delay(dly);

        zOrderSteps++;

        zeroPosition++;  //increase the position if motor is running CW

        zPhase = 0;

        if (zOrderSteps >= abs(RequestedSteps)) {
          term = 0;  // This breaks us out of the for loop when done with requested steps

          PhaseHist = stepperPhase;

          delay(dly);

          Wire.beginTransmission(0x21);  // transmit to device #44 (0x2c)
          // device address is specified in datasheet
          Wire.write(byte(0x02));  // sends instruction byte
          Wire.write(0x00);        // turns off motors to prevent heating
          Wire.write(0x00);        // turns off motors to prevent heating
          Wire.endTransmission();

          Wire.beginTransmission(0x21);  // transmit to device #44 (0x2c)
          // device address is specified in datasheet
          Wire.write(byte(0x06));  // sends instruction byte
          Wire.write(0x00);        // turns off motors to prevent heating
          Wire.write(0x00);        // turns off motors to prevent heating
          Wire.endTransmission();
        }
      }
    }
  }

  if (CW == 1)  // If CW motion the break will be executed
  {

    my_serial.print("Current Position = ");
    my_serial.println(zeroPosition);
    my_serial.println(" ");
    my_serial.println("Do you want to save this as homing position ?");
    my_serial.println("");

    while (my_serial.available() == 0) {
      /*do nothing*/
    }
    savedFlag = my_serial.read();
    if (savedFlag == 'y') {
      my_serial.println("  ");
      my_serial.println("  ");
      my_serial.print("homing offset has been updated to ");
      zeroOrderOffset = zeroPosition + zeroOrderOffset;
      my_serial.println(zeroOrderOffset);
      my_serial.println("This value will be stored in EEPROM");

      write2BytesIntIntoEEPROM(zeroOrderOffsetAddress, zeroOrderOffset);
      delay(5);
      my_serial.println(" ");
      my_serial.print(zeroOrderOffset);
      my_serial.println("  was written to EEPROM");
      my_serial.println(" ");

    } else {
      my_serial.println("homing offset has NOT been updated");
      my_serial.println(" ");
      my_serial.print("Homing offset = ");
      my_serial.print(zeroOrderOffset);
      my_serial.println(" ");
    }

    break;
  } else {
    zOrderSteps = 0;
  }

  RequestedSteps = abs(BkLashCount);

  CW = 1;
  zPhase = PhaseHist;

  delay(dly);
  zPhase = zPhase + 1;
  if (zPhase >= 8) {
    zPhase = 0;
  }

  while (zOrderSteps < abs(RequestedSteps)) {
    term = 8;

    for (stepperPhase = zPhase; stepperPhase < term; stepperPhase++) {

      if (gratingDir == 1) {
        // Shift output the bits for CW rotation
        Wire.beginTransmission(0x21);  // transmit to device #44 (0x2c)
        // device address is specified in datasheet
        Wire.write(byte(0x02));                // sends instruction byte
        Wire.write(dataArray3[stepperPhase]);  // sends stepper Phase value byte
        Wire.write(dataArray3[stepperPhase]);  // sends stepper Phase value byte
        Wire.endTransmission();

      } else {
        // Shift output the bits for CCW rotation
        Wire.beginTransmission(0x21);  // transmit to device #44 (0x2c)
        // device address is specified in datasheet
        Wire.write(byte(0x02));                // sends instruction byte
        Wire.write(dataArray4[stepperPhase]);  // sends stepper Phase value byte
        Wire.write(dataArray4[stepperPhase]);  // sends stepper Phase value byte
        Wire.endTransmission();
      }

      delay(dly);

      zOrderSteps++;

      zeroPosition++;  //increase the position if motor is running CW

      zPhase = 0;

      if (zOrderSteps >= abs(RequestedSteps)) {
        term = 0;  // This breaks us out of the for loop when done with requested steps

        PhaseHist = stepperPhase;

        my_serial.println("  ");
        my_serial.println("  ");
        my_serial.print("Current Position = ");
        my_serial.println(zeroPosition);
        my_serial.println("  ");
        my_serial.println("  ");

        delay(dly);

        Wire.beginTransmission(0x21);  // transmit to device #44 (0x2c)
        // device address is specified in datasheet
        Wire.write(byte(0x02));  // sends instruction byte
        Wire.write(0x00);        // turns off motors to prevent heating
        Wire.write(0x00);        // turns off motors to prevent heating
        Wire.endTransmission();

        Wire.beginTransmission(0x21);  // transmit to device #44 (0x2c)
        // device address is specified in datasheet
        Wire.write(byte(0x06));  // sends instruction byte
        Wire.write(0x00);        // turns off motors to prevent heating
        Wire.write(0x00);        // turns off motors to prevent heating
        Wire.endTransmission();
      }
    }
  }

  if (CW == 1)  // If CW motion the break will be executed
  {
    my_serial.println("Do you want to save this as homing position ?");
    my_serial.println("Enter y to save -- n not to save?");

    while (my_serial.available() == 0) {
      /*do nothing*/
    }
    savedFlag = my_serial.read();
    if (savedFlag == 'y') {
      my_serial.println("  ");
      my_serial.println("  ");
      my_serial.print("homing offset has been updated to ");
      zeroOrderOffset = zeroPosition + zeroOrderOffset;
      my_serial.println(zeroOrderOffset);

      write2BytesIntIntoEEPROM(zeroOrderOffsetAddress, zeroOrderOffset);
      delay(5);
      my_serial.println(" ");
      my_serial.print(zeroOrderOffset);
      my_serial.println("  was written to EEPROM");
      my_serial.println(" ");

      //------------------------------------------------------
      output = read2BytesFromEEPROM(zeroOrderOffsetAddress);

      if (output > 32768)  //if this is true the number is negative
      {
        output = -1 * (65536 - output);  //this converts a large number representing a negative number to a -value
      }
      //------------------------------------------------------
    } else {
      my_serial.println("homing offset has NOT been updated");

      my_serial.println(" ");
      my_serial.print("Homing offset = ");
      my_serial.print(zeroOrderOffset);
      my_serial.println(" ");
    }

    break;
  } else {
    zOrderSteps = 0;
  }
  break;

  //===================================================================================
case 'Z':
case 'z':
  // This routine will set the collimating lens position to 0 (home position)
  // This should only be done once on initialization of physical focus

  write2BytesIntIntoEEPROM(focusAddress, 0);
  delay(5);
  my_serial.println(" ");
  my_serial.println("to establish a Home location");
  my_serial.println("0 was written to EEPROM");
  my_serial.println(" ");
  break;

  //===================================================================================
case 'C':
case 'c':
  // This configuration routine will store the grating values of 300, 600, or 900
  // lines per mm

  my_serial.println(" ");
  my_serial.print("Enter the grating lines per mm - 300, 600, or 900");
  my_serial.println(" ");
  while (my_serial.available() == 0) {
  }
  grating_mm = my_serial.parseInt();

  if (grating_mm == 300 || grating_mm == 600 || grating_mm == 900) {

    write2BytesIntIntoEEPROM(configurationAddress, grating_mm);
    delay(5);
    grating_mm = read2BytesFromEEPROM(configurationAddress);
    my_serial.println(" ");
    my_serial.print("grating L/mm was written to EEPROM = ");
    my_serial.println(grating_mm);
    my_serial.println(" ");

  } else {
    my_serial.print("the value entered was ");
    my_serial.println(grating_mm);
    my_serial.println(" ");
    my_serial.print("invalid input, select desired function");
  }

  break;

  //===================================================================================
default:
  my_serial.println(" ");
  my_serial.println("******* No Valid Entry Has Been Entered, Please Try Again *******");
  break;
}
}

//===================================================================================

void resetFocus() {
  my_serial.println(" ");
  my_serial.println("Are you sure you want to reset the collimation focus? Y/N");
  my_serial.println(" ");
  my_serial.println("Enter a Y To Reset The Focus Position to 0");
  my_serial.println(" ");

  while (my_serial.available() == 0) {
    /*do nothing*/
  }

  char chr = my_serial.read();

  if (chr == 'Y' || chr == 'y') {

    my_serial.print("******* collimation focus has been reset == to ");
    lastPosition = 0;
    my_serial.print(lastPosition);
    my_serial.println(" *******");

    my_serial.println(" ");
    my_serial.print("reset position = ");
    focusPosition = 0;
    my_serial.print(focusPosition);
    my_serial.println(" ");

    write2BytesIntIntoEEPROM(focusAddress, 0);
    delay(5);
    my_serial.println(" ");

    my_serial.print(lastPosition);
    my_serial.println("  was written to EEPROM");
    my_serial.println(" ");
  } else {
    my_serial.println("  something other than Y was entered");
    my_serial.println(" ");
    my_serial.println("******* the focus Position has not been changed *******");
    my_serial.println(" ");
  }
}

//====================================================================

void homing() {
  homed = 0;
  int magnetNew = digitalRead(magnetPin);
  int magnetOld = magnetNew;

  while (homed == 0) {
    magnetNew = (digitalRead(magnetPin));

    term = 8;  // This is used to terminate the following for loop
    // when the number of required steps has been reached

    for (int phase = 0; phase < term; phase++) {

      if (magnetNew == 1) {

        if (gratingDir == 1) {
          // Shift output the bits for CW rotation
          Wire.beginTransmission(0x21);  // transmit to device #44 (0x2c)
          // device address is specified in datasheet
          Wire.write(byte(0x02));         // sends instruction byte
          Wire.write(dataArray3[phase]);  // sends phase value byte
          Wire.write(dataArray3[phase]);  // sends phase value byte
          Wire.endTransmission();

        } else {
          // Shift output the bits for CCW rotation
          Wire.beginTransmission(0x21);  // transmit to device #44 (0x2c)
          // device address is specified in datasheet
          Wire.write(byte(0x02));         // sends instruction byte
          Wire.write(dataArray4[phase]);  // sends phase value byte
          Wire.write(dataArray4[phase]);  // sends phase value byte
          Wire.endTransmission();
        }
      } else {
        if (gratingDir == 1) {
          // Shift output the bits for CCW rotation
          Wire.beginTransmission(0x21);  // transmit to device #44 (0x2c)
          // device address is specified in datasheet
          Wire.write(byte(0x02));         // sends instruction byte
          Wire.write(dataArray4[phase]);  // sends phase value byte
          Wire.write(dataArray4[phase]);  // sends phase value byte
          Wire.endTransmission();

        } else {
          // Shift output the bits for CW rotation
          Wire.beginTransmission(0x21);  // transmit to device #44 (0x2c)
          // device address is specified in datasheet
          Wire.write(byte(0x02));         // sends instruction byte
          Wire.write(dataArray3[phase]);  // sends phase value byte
          Wire.write(dataArray3[phase]);  // sends phase value byte
          Wire.endTransmission();
        }
      }

      delay(dly);

      steps++;

      // did magnetNew change state?
      //===================================================
      magnetNew = (digitalRead(magnetPin));

      if (magnetNew != magnetOld) {
        if (magnetNew == 1) {
          backlash();
        }
        term = 0;  // This breaks us out of the for loop when done with requested steps
        homed = 1;


        stepHist = 0;

        gratPosition = 0;

        Wire.beginTransmission(0x21);  // transmit to device #44 (0x2c)
        // device address is specified in datasheet
        Wire.write(byte(0x02));  // sends instruction byte
        Wire.write(0x00);        // turns off motors to prevent heating
        Wire.write(0x00);        // turns off motors to prevent heating
        Wire.endTransmission();

        Wire.beginTransmission(0x21);  // transmit to device #44 (0x2c)
        // device address is specified in datasheet
        Wire.write(byte(0x06));  // sends instruction byte
        Wire.write(0x00);        // turns off motors to prevent heating
        Wire.write(0x00);        // turns off motors to prevent heating
        Wire.endTransmission();

        delay(dly);
      }
    }
  }

  zeroOrderSteps = zeroOrderOffset;
  zOrderSteps = 0;

  my_serial.println(" ");
  my_serial.print("Homing offset = ");
  my_serial.print(zeroOrderOffset);
  my_serial.println(" ");

  zeroOrderPhase = orderPhaseHist;

  if (gratingDir == 1) {
    // Shift output the bits for CW rotation
    Wire.beginTransmission(0x21);  // transmit to device #44 (0x2c)
    // device address is specified in datasheet
    Wire.write(byte(0x02));                  // sends instruction byte
    Wire.write(dataArray3[orderPhaseHist]);  // sends orderPhaseHist value byte
    Wire.write(dataArray3[orderPhaseHist]);  // sends orderPhaseHist value byte
    Wire.endTransmission();

  } else {
    // Shift output the bits for CCW rotation
    Wire.beginTransmission(0x21);  // transmit to device #44 (0x2c)
    // device address is specified in datasheet
    Wire.write(byte(0x02));                  // sends instruction byte
    Wire.write(dataArray4[orderPhaseHist]);  // sends orderPhaseHist value byte
    Wire.write(dataArray4[orderPhaseHist]);  // sends orderPhaseHist value byte
    Wire.endTransmission();
  }

  delay(dly);

  if (zeroOrderSteps > 0) {
    CW = 1;
  } else {
    CW = 0;
  }

  while (zOrderSteps < abs(zeroOrderSteps)) {

    term = 8;  // This is used to terminate the following for loop
    // when the number of required steps has been reached

    for (zeroOrderPhase = 0; zeroOrderPhase < term; zeroOrderPhase++) {

      if (CW > 0) {
        if (gratingDir == 1) {
          // Shift output the bits for CW rotation
          Wire.beginTransmission(0x21);  // transmit to device #44 (0x2c)
          // device address is specified in datasheet
          Wire.write(byte(0x02));                  // sends instruction byte
          Wire.write(dataArray3[zeroOrderPhase]);  // sends zero Order Phase value byte
          Wire.write(dataArray3[zeroOrderPhase]);  // sends zero Order Phase value byte
          Wire.endTransmission();

        } else {
          // Shift output the bits for CCW rotation
          Wire.beginTransmission(0x21);  // transmit to device #44 (0x2c)
          // device address is specified in datasheet
          Wire.write(byte(0x02));                  // sends instruction byte
          Wire.write(dataArray4[zeroOrderPhase]);  // sends zero Order Phase value byte
          Wire.write(dataArray4[zeroOrderPhase]);  // sends zero Order Phase value byte
          Wire.endTransmission();
        }
      } else {
        if (gratingDir == 1) {
          // Shift output the bits for CCW rotation
          Wire.beginTransmission(0x21);  // transmit to device #44 (0x2c)
          // device address is specified in datasheet
          Wire.write(byte(0x02));                  // sends instruction byte
          Wire.write(dataArray4[zeroOrderPhase]);  // sends zero Order Phase value byte
          Wire.write(dataArray4[zeroOrderPhase]);  // sends zero Order Phase value byte
          Wire.endTransmission();
        } else {
          // Shift output the bits for CW rotation
          Wire.beginTransmission(0x21);  // transmit to device #44 (0x2c)
          // device address is specified in datasheet
          Wire.write(byte(0x02));                  // sends instruction byte
          Wire.write(dataArray3[zeroOrderPhase]);  // sends zero Order Phase value byte
          Wire.write(dataArray3[zeroOrderPhase]);  // sends zero Order Phase value byte
          Wire.endTransmission();
        }
      }

      delay(dly);

      zOrderSteps++;

      if (CW == 1) {
        zeroPosition++;  //increase the position if motor is running CW
      } else {
        zeroPosition = zeroPosition - 1;  //decrease the position if motor is running CCW
      }

      if (zOrderSteps >= abs(zeroOrderSteps)) {
        term = 0;  // This breaks us out of the for loop when done with requested steps

        orderPhaseHist = zeroOrderPhase;

        delay(dly);

        Wire.beginTransmission(0x21);  // transmit to device #44 (0x2c)
        // device address is specified in datasheet
        Wire.write(byte(0x02));  // sends instruction byte
        Wire.write(0x00);        // turns off motors to prevent heating
        Wire.write(0x00);        // turns off motors to prevent heating
        Wire.endTransmission();

        Wire.beginTransmission(0x21);  // transmit to device #44 (0x2c)
        // device address is specified in datasheet
        Wire.write(byte(0x06));  // sends instruction byte
        Wire.write(0x00);        // turns off motors to prevent heating
        Wire.write(0x00);        // turns off motors to prevent heating
        Wire.endTransmission();
      }
    }
  }

  if (CW == 1)  // If CW motion the break will be executed
  {
    my_serial.print("Current Position EEPROM= ");
    my_serial.println(zeroPosition);
    my_serial.println(" ");

  } else {
    zOrderSteps = 0;

    //=========================================================
    // This routine will be used to eliminate backlash
    // it will continue driving in the CCW and then turn CW back to starting Position
    // this will always drive in a CW direction to the desired Position
    //=========================================================

    zeroOrderSteps = 200;  // each directions will go 1/2 this many steps

    while (zOrderSteps < abs(zeroOrderSteps))

    {
      term = 8;  // This is used to terminate the following for loop
      for (int zeroOrderPhase = 0; zeroOrderPhase < term; zeroOrderPhase++) {

        if (CW == 1) {
          if (gratingDir == 1) {
            // Shift output the bits for CW rotation
            Wire.beginTransmission(0x21);  // transmit to device #44 (0x2c)
            // device address is specified in datasheet
            Wire.write(byte(0x02));                  // sends instruction byte
            Wire.write(dataArray3[zeroOrderPhase]);  // sends zero Order Phase value byte
            Wire.write(dataArray3[zeroOrderPhase]);  // sends zero Order Phase value byte
            Wire.endTransmission();

          } else {
            // Shift output the bits for CCW rotation
            Wire.beginTransmission(0x21);  // transmit to device #44 (0x2c)
            // device address is specified in datasheet
            Wire.write(byte(0x02));                  // sends instruction byte
            Wire.write(dataArray4[zeroOrderPhase]);  // sends zero Order Phase value byte
            Wire.write(dataArray4[zeroOrderPhase]);  // sends zero Order Phase value byte
            Wire.endTransmission();
          }
        } else {
          if (gratingDir == 1) {
            // Shift output the bits for CCW rotation
            Wire.beginTransmission(0x21);  // transmit to device #44 (0x2c)
            // device address is specified in datasheet
            Wire.write(byte(0x02));                  // sends instruction byte
            Wire.write(dataArray4[zeroOrderPhase]);  // sends zero Order Phase value byte
            Wire.write(dataArray4[zeroOrderPhase]);  // sends zero Order Phase value byte
            Wire.endTransmission();

          } else {
            // Shift output the bits for CW rotation
            Wire.beginTransmission(0x21);  // transmit to device #44 (0x2c)
            // device address is specified in datasheet
            Wire.write(byte(0x02));                  // sends instruction byte
            Wire.write(dataArray3[zeroOrderPhase]);  // sends zero Order Phase value byte
            Wire.write(dataArray3[zeroOrderPhase]);  // sends zero Order Phase value byte
            Wire.endTransmission();
          }
        }

        delay(dly);

        zOrderSteps++;

        if (CW == 1) {
          zeroPosition++;
        } else {
          zeroPosition = zeroPosition - 1;
        }
        if (zOrderSteps >= (abs(zeroOrderSteps) / 2)) {
          CW = 1;
        }
        delay(dly);

        if (zOrderSteps >= abs(zeroOrderSteps)) {
          term = 0;

          orderPhaseHist = zeroOrderPhase;

          Wire.beginTransmission(0x21);  // transmit to device #44 (0x2c)
          // device address is specified in datasheet
          Wire.write(byte(0x02));  // sends instruction byte
          Wire.write(0x00);        // turns off motors to prevent heating
          Wire.write(0x00);        // turns off motors to prevent heating
          Wire.endTransmission();

          Wire.beginTransmission(0x21);  // transmit to device #44 (0x2c)
          // device address is specified in datasheet
          Wire.write(byte(0x06));  // sends instruction byte
          Wire.write(0x00);        // turns off motors to prevent heating
          Wire.write(0x00);        // turns off motors to prevent heating
          Wire.endTransmission();
        }
      }
    }
  }

  term = 0;  // This breaks us out of the for loop when done with requested steps
  homed = 1;


  stepHist = 0;
  gratPosition = 0;
  zeroPosition = 0;

  Wire.beginTransmission(0x21);  // transmit to device #44 (0x2c)
  // device address is specified in datasheet
  Wire.write(byte(0x02));  // sends instruction byte
  Wire.write(0x00);        // turns off motors to prevent heating
  Wire.write(0x00);        // turns off motors to prevent heating
  Wire.endTransmission();

  Wire.beginTransmission(0x21);  // transmit to device #44 (0x2c)
  // device address is specified in datasheet
  Wire.write(byte(0x06));  // sends instruction byte
  Wire.write(0x00);        // turns off motors to prevent heating
  Wire.write(0x00);        // turns off motors to prevent heating
  Wire.endTransmission();

  delay(dly);
}

void backlash() {
  delay(dly);
  steps = 0;
  while (steps < 100) {
    term = 8;  // This is used to terminate the following for loop

    for (int phase = 0; phase < term; phase++) {

      if (gratingDir == 1) {
        // Shift output the bits for CCW rotation
        Wire.beginTransmission(0x21);  // transmit to device #44 (0x2c)
        // device address is specified in datasheet
        Wire.write(byte(0x02));         // sends instruction byte
        Wire.write(dataArray4[phase]);  // sends phase value byte
        Wire.write(dataArray4[phase]);  // sends phase value byte
        Wire.endTransmission();

      } else {
        // Shift output the bits for CW rotation
        Wire.beginTransmission(0x21);  // transmit to device #44 (0x2c)
        // device address is specified in datasheet
        Wire.write(byte(0x02));         // sends instruction byte
        Wire.write(dataArray3[phase]);  // sends phase value byte
        Wire.write(dataArray3[phase]);  // sends phase value byte
        Wire.endTransmission();
       }

      delay(dly);

      steps++;
    }
  }
  // did magnetNew change state?
  //===================================================

  magnetNew = (digitalRead(magnetPin));
  delay(dly);

  while (magnetNew == 1) {
    term = 8;  // This is used to terminate the following for loop
    // when the number of required steps has been reached

    for (int phase = 0; phase < term; phase++) {

      if (gratingDir == 1) {
        // Shift output the bits for CW rotation
        Wire.beginTransmission(0x21);  // transmit to device #44 (0x2c)
        // device address is specified in datasheet
        Wire.write(byte(0x02));         // sends instruction byte
        Wire.write(dataArray3[phase]);  // sends phase value byte
        Wire.write(dataArray3[phase]);  // sends phase value byte
        Wire.endTransmission();

      } else {
        // Shift output the bits for CCW rotation
        Wire.beginTransmission(0x21);  // transmit to device #44 (0x2c)
        // device address is specified in datasheet
        Wire.write(byte(0x02));         // sends instruction byte
        Wire.write(dataArray4[phase]);  // sends phase value byte
        Wire.write(dataArray4[phase]);  // sends phase value byte
        Wire.endTransmission();
      }

      delay(dly);

      magnetNew = (digitalRead(magnetPin));

      if (magnetNew == 0) {
        term = 0;
      }
    }
    delay(dly);
  }
}
