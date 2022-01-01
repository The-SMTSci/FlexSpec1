#############################################################################
# Makefile -- ... SAS_NA1_3D_Spectrograph/FS1Code-V1/Makefile
# https://retrylife.ca/blog/2020/09/03/bazel-and-avr
# make -r
#
# REGRESSION   -- up top; used to run REGRESSION tests on some platform
#                 usually blocks iostream! a monster in Arduinos.
#
#
#
#
# 2021-04-13T10:38:59-0600 wlg
#############################################################################

### Using a platform hint, try to extend this makefile.
###   makefile.linux makefile.pi

REGRESSION = -D__REGRESSION__
INCFILES = 

# clear suffixes and remember to use -R when running makefile for iso files.
.SUFFIXES:

# (wg-browser "https://www.gnu.org/software/make/manual/html_node/Conditional-Syntax.html")
# force /bin/bash -- sorry Microsoft. Get with it!
SHELL=/bin/bash
UNAME   := $(shell uname)

# allow running on platform.
# override SYSARCH from command line SYSARCH=nano

ifeq ($(SYSARCH),nano)
   include makefile.nano
$(info "Using nano architecture")
else ifeq ($(SYSARCH),xaio)
   include makefile.xaio
$(info "Using xaio architecture")
else ifeq ($(SYSARCH),armv7l)
   include makefile.pi
   $(info "Using Linux pi architecture")
   REGRESSION += -D__RPI__
else ifeq ($(UNAME),Linux)
   include makefile.linux
   $(info "Using local Linux architecture")
else
  prefix       = /usr/local
  SHARLIB      = g++ -shared -Wl,-soname,libfoo.so.$(LIBVERSION) -o libfoo.so.$(LIBVERSION)
endif

ifeq ($(SYSARCH),"")
SYSARCH := $(shell arch)
$(info "Using default shell")
endif

SRCS    = FlexPool.cpp \
          FlexOrientation.cpp

# cruft .. TODO strip cruft
#FlexParser.cpp
#FlexSerial.cpp
#FlexVariableMap.cpp

#FlexOrientation.h
#FlexParser.h
#FlexPool.h
#FlexSerial.h
#FlexVariableMap.h

#FlexOrientation.h
#FlexParser.cpp : FlexParser.h
#FlexSerial.cpp : FlexSerial.h
#FlexVariableMap.cpp : FlexVariableMap.h

INCS     = Patron.h \
           PostMaster.h \
           FS_Dispatcher.h \
           FS_RGBlinky.h \
           FS_StepperMotor.h

PENDING  = Message.h \
           MessagePool.h \
           FS_Dispatcher.h \
           FS_Inventory.h \
           FS_Blinky.h \
           FS_Event.h \
           FS_EventPool.h \
           FS_SerialPort.h \
           FS_SerialServer.h \
           FS_I2CPort.h \
           FS_Focuser.h \
           FS_CAMLinearFocuser.h \
           FS_HelicalFocuser.h \
           FS_LinearFocuser.h \
           FS_Rotator.h \
           FS_LimitedRotator.h \
           FS_FullRotator.h \
           FS_Sensor.h \
           FS_IMU.h \
           FS_MQTT.h \
           FS_Processor.h \
           FS_Switch.h \
           FS_SimpleSwitch.h \
           FS_TimedSwitch.h

MAYBE    = FS_Timer.h

all: FS_StepperMotor.h
	$(CPP) $(INCFILES) -c FS_StepperMotor.h

FS_Dispatcher: FS_Dispatcher.h FS_Dispatcher.cpp
	$(CPP) $(INCFILES) -D__REGRESSION__ -o FS_Dispatcher FS_Dispatcher.cpp


#all: $(SRCS:.cpp=.o)

clean:
	-rm -f *.o

#FlexPool          : FlexPool.o
#	$(CPP) -o FlexPool FlexPool.o
#
#FlexPool.cpp      : FlexPool.h
#FlexPostmaster.o  : FlexPostmaster.cpp
#FlexOrientation.o : FlexOrientation.cpp
#
#FlexOrientation: FlexOrientation.o FlexPostmaster.o FlexPool.o
#	g++ -o FlexOrientation  FlexOrientation.o FlexPostmaster.o FlexPool.o
#
## General dependencies
#
#FlexOrientation.cpp : FlexOrientation.h
#FlexPostmaster.cpp  : FlexPostmaster.h
#FlexSerial.cpp      : FlexSerial.h
#
#depends : $(SRCS)
#	g++ -MM $? > deps.d
#	cat deps.d
#
