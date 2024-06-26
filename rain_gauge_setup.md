# Acoustic Rain Gauge Setup Guide

## Hardware Setup
- Use Raspberry Pi 4 as board 
- Insert SD Card
- Connect USB Microphone and LAN
- Connect Davis to GPIO pin number 13 and ground (optional)

## Software Setup
### 1. Install Ubuntu Server 22.04.4 LTS (64-bit) using **Raspberry Pi Imager** Software
![screenshot_1](./images/screenshot_1.png)

### 2. Enable SSH Settings, give user credentials and WiFi credentials
![screenshot_2](./images/screenshot_2.png)
![screenshot_3](./images/screenshot_3.png)
![screenshot_4](./images/screenshot_4.png)

### 3. Flash the operating system and boot the Raspberry Pi

### 4. Check IP is getting assigned in Ethernet and Wifi

```bash
ip -br a
```
Both Ethernet and Wifi should be UP and IP should be assigned

### 5. Update and upgrade OS

```bash
sudo apt update
sudo apt upgrade
sudo reboot
```

### 6. Download and run setup.sh for automating environment setup

```bash
# Download setup.sh
wget 'https://raw.githubusercontent.com/cksajil/rainfall_monitor/hari/setup.sh'

# run setup.sh
bash setup.sh
```

### 7. Check in command line if microphone is detected
```bash
lsusb
```
This will list out all the USB devices connected to Raspberry Pi. To make sure that microphone is getting detected run the above command without connecting microphone and see the output. Repeat the same after connecting the microphone. Now the microphone or soundcard name should appear in the list as an additional entry.

### 8. Check if $arecord$ command lists the input devices
```bash
arecord -l
```

### 9. Reboot the Raspberry Pi
```bash
sudo reboot
```

### 10. After rebooting check if $arecord$ command is working
```bash
# Records a 5 second test audio as wav file
arecord --duration=5 sample.wav

# Delete the test file
rm sample.wav
```

### 11. Add influx-db yaml file (`influxdb_api.yaml`) to config folder

### 12. Add the device to Zerotier account

Follow the instructions on [Zerotier for Raspberry Pi Tutorial](https://pimylifeup.com/raspberry-pi-zerotier/). Go to  [Zerotier](https://my.zerotier.com/) platform and login with the credentials shared via email/open project to monitor/connect to device IPs.

### 13. change present working directory to code

```bash
cd /home/pi/raingauge/code/
```

### 14. Add Python scripts to bashrc file  

```bash
nano ~/.bashrc

# Appened the following line to the end of .bashrc file (this may cause path errors)
python3 /home/pi/raingauge/code/daq_pi.py & python3 /home/pi/raingauge/code/davis_logger.py

# Reboot the device
sudo reboot
```


