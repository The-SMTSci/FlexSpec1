FROM ubuntu

ARG TOOLCHAIN_ARCHIVE=https://github.com/arduino/toolchain-avr/archive/master.zip

RUN apt-get update -y && \
    apt-get install -y \
        build-essential \
        gperf \
        bison \
        subversion \
        texinfo \
        zip \
        automake \
        flex \
        libtinfo-dev \
        pkg-config \
        git \
        wget

RUN wget $TOOLCHAIN_ARCHIVE -O /tmp/toolchain-avr.zip && \
    unzip /tmp/toolchain-avr.zip && \
    rm /tmp/toolchain-avr.zip && \
    mv toolchain-avr*/* . && \
    rm -rf toolchain-avr*/ && \
    ./tools.bash && \
    ./binutils.build.bash && \
    ./gcc.build.bash && \
    ./avr-libc.build.bash && \
    ./gdb.build.bash && \
    ./package-avr-gcc.bash

ENV PATH=/objdir/bin:$PATH
