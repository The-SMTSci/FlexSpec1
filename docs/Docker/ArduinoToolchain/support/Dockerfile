# /home/git/external/docker-arduino-toolchain/toolchain/Dockerfile
# Build on top of the container made ../base: arduino_base:v1
# Add the system support for non-arduino support.
# docker build -t arduino_base:v2 .
FROM arduino_base:v1

ARG TOOLCHAIN_ARCHIVE=https://github.com/arduino/toolchain-avr/archive/master.zip

RUN apt-get install -y build-essential \
                       gperf \
                       bison \
                       flex \
                       automake \
                       libtinfo-dev \
                       pkg-config \
                       zip \
                       wget\
                       git \
                       subversion 

ENV PATH=/objdir/bin:$PATH
echo docker run -it --rm build -t arduino_base:v2 /bin/bash
echo and apt-get install -y texinfo to answer questions.
echo then docker commit <container> arduino_base:v3

