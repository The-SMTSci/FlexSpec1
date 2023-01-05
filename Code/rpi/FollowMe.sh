#!/bin/bash
#############################################################################
# FlexSpec1 - FollowMe.sh -- the script to follow when putting together
#   The raspberry pi script.
#
# Note: This script is located in a github repo: Kinda need that
#
# /home/git/FlexSpec1/Code/rpi/FollowMe.sh
#
# We won't install:
#    ds9   -- run it on your machine
#
# We will  install:
#    astrometry.net (that is handy locally)
#    sextractor
#
#
#
# git/external/FlexSpec1/Code/rpi/FollowMe.sh
# 2022-09-19T16:15:12-0600 wlg
#
#############################################################################
# ssh -l pier15 pier15.local  # see remove old key above
sudo apt-get update
sudo apt-get upgrade                          # N - keep the provider's /etc/apt-fast.conf
sudo apt-get dist-upgrade
# (accumulate a) list of packages to make sure we have.
flexpackages   = ("openssh-server" "linux-modules-extra-raspi" "net-tools" \
                  "curl" "gawk" "vim" "minicom" "git" "locate" "libx11-dev" \
                  "zlib1g-dev" "libxml2-dev" "libxslt1-dev" "autoconf" "swig" \
                  "python3-dev" "python3-pip" "python3-virtualenv" "sqlite3" \
                  "pip" "sqlitebrowser" "supervisor" "samba" "samba-tools"\
                  "build-essential" "apache2-utils" "filezilla" \
                  "nginx" "sqlite3" "indi-full" "gsc" "iraf" "python-pyraf3" )

basepackages   = ("ufw" "systemctl" "bind9")

pythonpackages = ( "numpy" "scipy" "pandas" "matplotlib" "bokeh" "pandas" \
                   "astropy" "gunicorn" "pysqlite3" "xpa")

usage   { echo "This script is located in a github repo:";
          echo "/home/git/FlexSpec1/Code/rpi/FollowMe.sh";
          echo "As root: ";
          echo "mkdir -p /home/git";
          echo "apt install -y git";
          echo "cd /home/git";
          echo "git clone https://github.com/The-SMTSci/FlexSpec1.git";
          echo "cd /home/git/Code/rpi";
          echo "bash FollowMe.sh";
          echo "Packages: $flexpackages $basepackages $pythonpackages";
          if test -e /sys/firmware/devicetree/base/model ; then
              echo $(cat /sys/firmware/devicetree/base/model);
          fi
}
#############################################################################
# The real work as root.
#############################################################################

# Make sure we have git and github's authentication
# https://github.com/cli/cli/blob/trunk/docs/install_linux.md
if [[ "$(which git)" == "" ]] ; then
    apt install git -y;
    type -p curl >/dev/null || apt install curl -y
    curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg && \
        chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg && \
        echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | tee /etc/apt/sources.list.d/github-cli.list > /dev/null     && \
        apt update                                                   && \
        apt install gh -y
fi

mkdir -p /home/git
cd /home/git
git clone https://github.com/The-SMTSci/FlexSpec1.git


# get my local net, using...
#export mylocalnet=$(ip r | gawk -- '/kernel/ {printf("%s", $1);}')

#hostnamectl set-hostname pier15          # force hostname

# add a special user, all system configuration activity here.
useradd -m -d /home/flex -G dialout -p "$(openssl passwd -1 'happy startrails')" flex

export FLEXUSER=flex

usermod -aG dialout $FLEXUSER     # allow user 'flex' ability to use facilities
usermod -aG tty     $FLEXUSER

# load up on packages!

apt     install -y ufw                       # uncomplicated firewall
apt     install -y openssh-server            # add openssh capability
systemctl status ssh                         # open the interface
ufw allow ssh                                # allow ssh in the firewall

apt     install -y linux-modules-extra-raspi # raspi-config hardware/boot bridge
apt     install -y net-tools                 # both ip ifconfig worlds

apt     install -y curl                      # because,,, curl! (astrometry.net)
apt     install -y gawk                      # IDIOTS -- don't ever use mawk!
apt     install -y vim                       # because,,, vi!

# Force VI as the editor. Really.
if test -e /etc/alternatives/editor ; then
   if test -e /usr/bin/vim.basic ; then
       ln -s /usr/bin/vim.basic /etc/alternatives/editor
   fi
fi

apt     install -y minicom                   # because,,, handy interface to serial

# Load these packages now, get it over with for ds9.
# Handy anyway.
apt     install -y locate                    # bacause,,, locate!
apt     install -y build-essential           # get the compilers...
apt     install -y libx11-dev                # needed for local compiles
apt     install -y zlib1g-dev                # needed for local compiles
apt     install -y libxml2-dev               # needed for local compiles
apt     install -y libxslt1-dev              # needed for local compiles
apt     install -y autoconf                  # needed for local compiles

# for astrometry.net
apt     install -y swig
apt     install -y python3-dev python3-pip python3-virtualenv

#############################################################################
# fixup .bashrc
#############################################################################
cd ~/git                                     # get the FlexSpec and install
git clone https://github.com/The-SMTSci/FlexSpec1.git
cd ~/git/FlexSpec1/Code/HOME
cp pi.aliases ~/.pi.aliases
cp vimrc      ~/.vimrc
cp vimrc /root                               # add a decent vimrc for sudo
mkdir -p /var/www/html/FlexSpec1
cp -pr ~/git/FlexSpec1/buil/hdtml/* /var/www/html/FlexSpec1 # install FlexHelp

# helper for flex login
cd $HOME/$FLEXUSER
cat >> ~/.bashrc  <<EOF                      # add our aliases for FLEXUSER
source .pi.aliases
EOF

#############################################################################
# This is a dedicated system, pound our opinion of python at the
# system level, not a virtualenv.
# Load up Python3 with the extra bits we really want.
# These support the FlexSpec Bokeh information, other visualizations.
#############################################################################
apt install sqlite3                          # lightweight database for general use.
apt install pip
#apt install pypy
pip install numpy
pip install scipy
pip install pandas
pip install matplotlib
pip install bokeh
pip install pandas
pip install astropy
pip install gunicorn
pip install pysqlite3
apt install -y sqlite3 sqlitebrowser
apt install -y supervisor

#############################################################################
# Load up Kstars/Ekos/libindi and drivers.
#############################################################################
apt-add-repository ppa:mutlaqja/ppa          # Libindi etc.
apt     update
apt     install  -y indi-full
apt     install  -y gsc
#apt     install -y kstars-bleeding

#############################################################################
# Add some file connectivity.
# DIFS is Common Internet Fileshares
#############################################################################
apt install -y samba samba-tools smbclient cifs-utils
systemctl enable --now smbd                  # retister for all reboots
ufw allow samba
usermod -aG sambashare flex
smbpasswd -a "flex%time has come"
mkdir -p /samba/{$FLEXUSER,flex}             # make shares for the two main users
chgrp -R sambashare /samba
usermod -aG sambashare $FLEXUSER             # add these users to group
usermod -aG sambashare flex
#smb://winhost/shared-folder-name
# TODO mod /etc/samba/smb.conf
systemctl restart smbd
systemctl restart nmbd

#############################################################################
# NFS - for other linux like clients
#############################################################################
apt install nfs-kernel-server
mkdir -p /mnt/share
chown -R nobody:nogroup /mnt/share/
chmod 777 /mnt/share/
exportfs -a
systemctl restart nfs-kernel-server

# add daemons
# cp ANCHOR/bokeh/bokeh.service /etc/systemd/system/bokeh.service
# cp ANCHOR/bokeh/flexdispatch.service /etc/systemd/system/bokeh.service
# systemctl daemon-reload
# systemctl enable bokeh.service

apt install -y nginx                         # nginx local access to bokeh
apt install -y apache2-utils                 # for auth with usernames and passwords
# create default passwords for $FLEXUSER and our flex default user.
htpasswd -cb /etc/nginx/.htpasswd $FLEXUSER "PwD4$USER"
htpasswd -b  /etc/nginx/.htpasswd flex  "Flex"  # TODO  make more secure.

mkdir -p /var/log/nginx/flexspec/
# create access and error logs for our instrument in usual place.
touch /var/log/nginx/flexspec/{access,error}.log
# install our pre-backed files
cp $ANCHOR/nginx/sites-available/flexspec /etc/nginx/sites-available/flexspec

# get it operational now.
systemctl restart nginx

ufw allow in on eth0 from 10.1.10.0/16
ufw allow from 10.1.10.0/16 to any port 5006 proto tcp
ufw allow from 10.1.10.0/16 to any port 5006 proto udp

setxkbmap us  # needed because initial install went sideways

# ip -4 show eth0
# ssh root@titan.local -N -D 5006

#############################################################################
# Allow DNS as a subdomain controler.
#############################################################################
apt install -y bind9 bind9-utils             # DNS

#############################################################################
# Add handy user code
#############################################################################
apt install -y filezilla                     # GUI to move files between systems

#############################################################################
# Add Iraf/Pyraf
#############################################################################

apt install -y iraf
apt install -y python-pyraf3

