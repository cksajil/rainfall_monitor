#!/bin/bash
# Bash script to automate Pizero deployment

username="ubuntu"

echo '*************************** ENABLING AUTO LOGIN **************************'
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
echo '************************ AUTO LOGIN SETUP COMPLETED ***********************'



echo '************************** INSTALLING DEPENDENCIES **********************'
sudo apt update
sudo apt upgrade
sudo apt install alsa-utils
sudo apt install -y pulseaudio
sudo apt install python3-pip
pip install librosa
pip install pandas
pip install RPi.GPIO
pip install influxdb-client
pip install keras
sudo apt-get install libatlas-base-dev
pip3 install tflite-runtime
echo '************************** INSTALLED DEPENDENCIES ***********************'



echo '************************ CREATING FOLDER STRUCTURE ***********************'
mkdir raingauge
mkdir raingauge/model raingauge/data raingauge/logs
cd raingauge/
git clone https://github.com/cksajil/rainfall_monitor.git
mv rainfall_monitor code
cd code/
git checkout pizero
cd ..
wget --no-check-certificate 'https://rb.gy/7b80vv' -O model/seq_stft.tflite
echo '************************ CREATED FOLDER STRUCTURE ***********************'


echo '*************************** REBOOTING DEVICE ****************************'
sudo reboot





