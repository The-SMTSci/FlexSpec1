#!/bin/bash

sudo usermod -aG sudo $USER
sed -i -e "\$a

# needed to compile xephem
sudo apt install build-essential groff-base libmotif-dev libssl-dev libxext-dev libxmu-dev libxt-dev
