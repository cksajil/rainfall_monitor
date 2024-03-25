# Acoustic Rain Gauge Setup Guide

## Hardware Setup
- Use Raspberry Pi 4 as board 
- Insert SD Card
- Connect USB Microphone and LAN
- Connect Davis to GPIO pin number 13 and ground (optional)

## Software Setup
1. Install Ubuntu Server 22.04.4 LTS (64-bit) using **Raspberry Pi Imager** Software
![screenshot_1](./images/screenshot_1.png)


2. Enable SSH Settings, give user credentials and WiFi credentials
![screenshot_2](./images/screenshot_2.png)
![screenshot_3](./images/screenshot_3.png)
![screenshot_4](./images/screenshot_4.png)

3. Flash the operating system and boot the Raspberry Pi

4. Update and upgrade OS

```bash
sudo apt update
sudo apt upgrade
```

5. Install audio related packages & reboot

```bash
sudo apt install alsa-utils
sudo apt install pulseaudio
sudo reboot
```

6. Check in command line if microphone is detected
```bash
lsusb
```
This will list out all the USB devices connected to Raspberry Pi. To make sure that microphone is getting detected run the above command without connecting microphone and see the output. Repeat the same after connecting the microphone. Now the microphone or soundcard name should appear in the list as an additional entry.

7. Check if $arecord$ command lists the input devices
```bash
arecord -l
```

8. Reboot the Raspberry Pi
```bash
sudo reboot
```

9. After rebooting check if $arecord$ command is working
```bash
# Records a 5 second test audio as wav file
arecord --duration=5 sample.wav

# Delete the test file
rm sample.wav
```

10. Install PIP
```bash
sudo apt install python3-pip
```

11. GPIO setup of logging davis data via GPIO
```bash
sudo apt install python3-rpi.gpio
pip install lgpio==0.0.0.2
sudo chmod 777 /sys/class/gpio/export 
sudo echo 6 > /sys/class/gpio/export 
sudo chmod 777 /sys/class/gpio/gpio6/direction 
sudo echo in > /sys/class/gpio/gpio6/direction 
sudo chmod 777 /sys/class/gpio/gpio6/edge
```


12. Create folder structure needed
```bash
mkdir raingauge logs  model data
```

13. Copy the trained model files to models folder
```bash
wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=17yY89nn5k9YEcEXLsZiXsKorpf9Mzlvr' -O model/rain_stft.hdf5

wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=15YwpKMOJ8MyvhM9zoIHB-H_u-d09p6Xz' -O model/seq_stft.hdf5
```

14. Clone the project repository to $raingauge$ folder
```bash
# Change directory
cd raingauge

# Clone the repository
git clone https://github.com/cksajil/rainfall_monitor.git

# Rename the directory
mv rainfall_monitor code

# Change directory
cd code

# Checkout gitlab branch
git checkout gitlab

# Dependency setup in Raspberry Pi
python3 -m pip install -r requirements.txt

# Install required packages independently in case of dependency issue above
pip install packagename
```

15. Add influx-db yaml file (**influxdb_api.yaml**) to config folder


16. Enable autologin 
```bash
sudo nano /etc/systemd/logind.conf
# Uncomment lines starting with NAutoVTs=6 and ReserveVT=6, save and exit

# Create an autologin service
sudo mkdir /etc/systemd/system/getty@tty1.service.d/
sudo nano /etc/systemd/system/getty@tty1.service.d/override.conf
```
Add the following content to override.conf file

```bash
# Here replace username with your Raspberry Pi username
[Service]
ExecStart=
ExecStart=-/sbin/agetty --noissue --autologin username %I $TERM
Type=idle
```

17. Add Python scripts to Bashrc 
```bash
nano ~/.bashrc

# Appened the following line to the end of .bashrc file
python3 /home/pi/raingauge/code/daq_pi.py & python3 /home/pi/raingauge/code/davis_logger.py
```

18. Reboot the Raspberry Pi
```bash
sudo reboot
```