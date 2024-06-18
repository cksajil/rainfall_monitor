# Acoustic Rain Gauge Setup Guide

## Hardware Setup
- Use Raspberry Pi Zero W as board 
- Insert SD Card
- Connect USB Microphone
- Connect Rain sensor to GPIO pin number 4 and ground

## Software Setup
### 1. Download suitable OS image
Download Ubuntu (64-bit ARM (ARMv8/AArch64) server install image) from https://cdimage.ubuntu.com/releases/focal/release/

OR from

https://ubuntu.com/download/server/arm. Please see [Alternative and previous releases section](https://cdimage.ubuntu.com/releases/?_gl=1*1st8y8i*_gcl_au*NjIzMTM3MzE0LjE3MTg2OTA4MzM.&_ga=2.97407837.315200084.1718690833-1252984037.1710486708)

### 2. Flash the operating system using balenaEtcher and boot the Raspberry Pi
Please make sure to connect card reader to USB port in the backside of PC to avoid write verification fail
### 3. Update default user credentials
Credential update will be asked on first log in using default username (ubuntu/root)
### 4. Add WiFi credentials
```bash
sudo vim  /etc/netplan/50-cloud-init.yaml
```
Add the following content to the file (use Vim editor to make sure consistent indentation)
```yaml
network:
    ethernets:
        eth0:
            dhcp4: true
            optional: true
    version: 2
    wifis:
        wlan0:
            dhcp4: true
            optional: true
            access-points:
                "wifi_name":
                        password: "password"

```
```bash
sudo netplan generate
sudo netplan apply
```
### 5. Check IP is getting assigned for Wifi

```bash
hostname -I
```

### 5. Update and upgrade OS

```bash
sudo apt update
sudo apt upgrade
sudo reboot
```

### 6. Download and run setup.sh for automating environment setup

```bash
sudo apt install python3-pip
pip install pandas
pip install RPi.GPIO
pip install influxdb-client
pip install keras
pip install tensorflow --no-cache-dir
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
git checkout pizero
```

### 14. Add Python scripts to bashrc file  

```bash
nano ~/.bashrc

# Appened the following line to the end of .bashrc file (this may cause path errors)
python3 /home/pi/raingauge/code/daq_pi.py

# Reboot the device
sudo reboot
```


