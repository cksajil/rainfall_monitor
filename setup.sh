#!/bin/bash
# this file contain bash script to automating deployment environment setup 

# progress bar animation
progress_bar() {
    local duration=$1
    local color="\033[1;31m"  # red color
    local reset="\033[0m"     # Reset color to default

    already_done() { for ((done=0; done<$filled; done++)); do printf "${color}▇${reset}"; done }
    remaining() { for ((remain=$filled; remain<$bar_width; remain++)); do printf " "; done }
    percentage() { printf "| %s%%" $((elapsed * 100 / duration)); }

    for ((elapsed=1; elapsed<=duration; elapsed++)); do
        local term_width=$(tput cols)  # Get the current terminal width dynamically
        local bar_width=$((term_width - 6))  # Adjust for percentage display (| XX%)

        filled=$((elapsed * bar_width / duration))  # Calculate the number of filled blocks
        
        printf "\r"  # Return to the beginning of the line
        already_done; remaining; percentage
        sleep 0.07  # Simulating the work being done (adjust as needed)
    done
    printf "\n"  # New line after completion
}

print_centered_message() {
    local message="$1"
    local padding_char="#"

    # Get the current terminal width
    local term_width=$(tput cols)
    local message_length=${#message}  # Length of the message
    local total_length=$((term_width - 4))  # Total length of the line, accounting for borders

    # Calculate padding on both sides
    local padding_length=$(( (total_length - message_length) / 2 ))

    # Ensure padding length is non-negative
    if (( padding_length < 0 )); then
        padding_length=0
    fi

    # Create the line with padding
    local line=$(printf "%s" "${padding_char}$(printf "%*s" $padding_length "" | tr " " "$padding_char") $message $(printf "%*s" $padding_length "" | tr " " "$padding_char")${padding_char}")

    # Print the line
    printf "\r"  # Move to the start of the line
    tput el  # Clear the current line to ensure no residual characters
    printf "%s\n" "$line"  # Print the constructed line
}

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

print_centered_message "AUTO LOGIN SETUP COMPLETED"
progress_bar 20

# setting up folder structure and cloning repository
mkdir raingauge
mkdir raingauge/model raingauge/data raingauge/logs
cd raingauge/
git clone https://github.com/cksajil/rainfall_monitor.git
mv rainfall_monitor code
cd code/
git checkout deployment
cd ..
wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=15rnz_j0QYxJM-4zMHGyLYQMw8a8ndjzs' -O model/seq_stft.hdf5
# wget --no-check-certificate 'https://drive.google.com/file/d/1-P7dm65AwHHd9gw4DtFe9Bf5Z1nIH1dE/view?usp=drive_link' -O model/seq_stft_enc2.hdf5

print_centered_message "ENVIRONMENT CREATED"
progress_bar 20

#installing dependencies
print_centered_message "INSTALLING DEPENDENCIES"
sudo apt-get install -y python3-pip
export PATH="$HOME/.local/bin:$PATH" # adding f2py path to system environment variable
echo '****************************************** "/home/pi/.local/bin" PATH ADDED TO ENVIRONMENT VARIABLES ******************************************'
# sudo apt install -y python3.12-venv
# python3 -m venv venv
# source venv/bin/activate
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
pip install PyYAML
pip install pyserial
pip install Adafruit-ADS1x15
sudo apt install i2c-tools
sudo apt install raspi-config
pip install RPi.GPIO
print_centered_message "INSTALLED DEPENDENCIES"
progress_bar 20
print_centered_message "REBOOTING DEVICE"
sudo reboot





# issues
# how to resolve asking password input when using sudo command?
# how to install influxdb credentials automatically
# if we move github repo contain bash script to another directory while executing bash.will that effect execution.(we can solve the issue by moving desired files only)
# how to automate audio checking functionality
# make progress bar for each sections.that is progress bar on the bottom side and installation will run in background