#############################################################################
#
# docker build -t fs1.1 .
#
# docker run -it -p 5006:5006 fs1.1
#
#
#############################################################################
FROM continuumio/anaconda3

RUN  mkdir -p /home/Flexspec/Code
COPY Code /home/Flexspec/Code
