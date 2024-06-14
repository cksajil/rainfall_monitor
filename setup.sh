#!/bin/bash
# this file contain bash script to automating deployment environment setup 

username="pi"

# enabling auto login service
sudo chmod 777 /etc/systemd/logind.conf
echo "#  This file is part of systemd.
#
#  systemd is free software; you can redistribute it and/or modify it under the
#  terms of the GNU Lesser General Public License as published by the Free
#  Software Foundation; either version 2.1 of the License, or (at your option)
#  any later version.
#
# Entries in this file show the compile time defaults. Local configuration
# should be created by either modifying this file, or by creating "drop-ins" in
# the logind.conf.d/ subdirectory. The latter is generally recommended.
# Defaults can be restored by simply deleting this file and all drop-ins.
#
# Use 'systemd-analyze cat-config systemd/logind.conf' to display the full config.
#
# See logind.conf(5) for details.

[Login]
NAutoVTs=6
ReserveVT=6
#KillUserProcesses=no
#KillOnlyUsers=
#KillExcludeUsers=root
#InhibitDelayMaxSec=5
#UserStopDelaySec=10
#HandlePowerKey=poweroff
#HandleSuspendKey=suspend
#HandleHibernateKey=hibernate
#HandleLidSwitch=suspend
#HandleLidSwitchExternalPower=suspend
#HandleLidSwitchDocked=ignore
#HandleRebootKey=reboot
#PowerKeyIgnoreInhibited=no
#SuspendKeyIgnoreInhibited=no
#HibernateKeyIgnoreInhibited=no
#LidSwitchIgnoreInhibited=yes
#RebootKeyIgnoreInhibited=no
#HoldoffTimeoutSec=30s
#IdleAction=ignore
#IdleActionSec=30min
#RuntimeDirectorySize=10%
#RuntimeDirectoryInodesMax=400k
#RemoveIPC=yes
#InhibitorsMax=8192
#SessionsMax=8192" > /etc/systemd/logind.conf

sudo mkdir /etc/systemd/system/getty@tty1.service.d/
sudo chmod 777 /etc/systemd/system/getty@tty1.service.d/
echo "[Service]
ExecStart=
ExecStart=-/sbin/agetty --noissue --autologin $username %I \$TERM
Type=idle" > /etc/systemd/system/getty@tty1.service.d/override.conf
echo '********************************************************* AUTO LOGIN SETUP COMPLETED **********************************************************'

# setting up folder structure and cloning repository
mkdir raingauge
mkdir raingauge/model raingauge/data raingauge/logs
cd raingauge/
git clone https://github.com/cksajil/rainfall_monitor.git
mv rainfall_monitor code
cd code/
git checkout gitlab
cd ..
wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=17yY89nn5k9YEcEXLsZiXsKorpf9Mzlvr' -O model/rain_stft.hdf5
wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=15YwpKMOJ8MyvhM9zoIHB-H_u-d09p6Xz' -O model/seq_stft.hdf5
echo '*********************************************************** ENVIRONMENT CREATED ***************************************************************'

#installing dependencies
echo '******************************************************** INSTALLING DEPENDENCIES **************************************************************'
sudo apt install python3-pip
export PATH="$HOME/.local/bin:$PATH" # adding f2py path to system environment variable
echo '****************************************** "/home/pi/.local/bin" PATH ADDED TO ENVIRONMENT VARIABLES ******************************************'
pip install --upgrade pip
sudo apt-get install -y pkg-config
sudo apt-get install -y libhdf5-dev
sudo apt install -y python3-rpi.gpio
sudo apt install -y alsa-utils
sudo apt install -y pulseaudio
sudo apt-get install -y usbutils
pip install influxdb-client
pip install pandas # numpy will automatically install with pandas
pip install librosa
pip install keras
pip install tensorflow
echo '********************************************************** REBOOTING DEVICE *******************************************************************'
sudo reboot





# issues
# how to resolve asking password input when using sudo command?
# how to install influxdb credentials automatically
# if we move github repo contain bash script to another directory while executing bash.will that effect execution.(we can solve the issue by moving desired files only)
# how to automate audio checking functionality