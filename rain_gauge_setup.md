# Acoustic Rain Gauge Setup Guide

## Hardware Setup
- Use Raspberry Pi Zero W as board 
- Insert SD Card
- Connect USB Microphone
- Connect Rain sensor to GPIO pin number 4 and ground

## Software Setup
### 1. Flash Ubuntu Server 23.10 (64 bit ) preferably using Raspberry Pi Imager v1.7.2

- Please make sure to connect card reader to USB port in the backside of PC to avoid write verification fail
- Avoid quick format to reduce write error
- Provide WiFi credentials, TimeZone, enable SSH while flashing

### 2. Check IP is getting assigned for Wifi

```bash
hostname -I
```

### 3. Update and upgrade OS

```bash
sudo apt update
sudo apt upgrade
sudo reboot
```

### 4. Increase swap space
```bash
sudo nano /etc/dphys-swapfile

# modify the following line
CONF_SWAPSIZE=4096

sudo systemctl restart dphys-swapfile

#check current size
free -m
```

### 5. Install dependencies

```bash
sudo apt install -y alsa-utils
sudo apt install -y pulseaudio
sudo apt-get install -y dphys-swapfile
sudo apt install -y python3-pip
pip install --upgrade pip
sudo apt install python3.11-venv
```

### 6. Create venv and activate

```bash
python3 -m venv venv
source venv/bin/activate
```

```bash
pip install PyYAML
pip install librosa
pip install RPi.GPIO
pip install influxdb-client
pip install tflite-runtime
pip install --upgrade tflite_runtime
pip uninstall numpy
pip install numpy==1.23.5
```
### 7. Create folder structure
```bash
mkdir raingauge
mkdir raingauge/model raingauge/data
cd raingauge/
git clone https://github.com/cksajil/rainfall_monitor.git
mv rainfall_monitor code
cd code/
git checkout pizero
cd ..
```

### 8. Download and convert to TFLite Model
Check Kaggle notebook version 92 outputs to see the model without LSTM blocks
```bash
wget --no-check-certificate 'https://rb.gy/kdojrr' -O model/seq_stft.tflite
```


### 9. Check in command line if microphone is detected
```bash
lsusb
```
This will list out all the USB devices connected to Raspberry Pi. To make sure that microphone is getting detected run the above command without connecting microphone and see the output. Repeat the same after connecting the microphone. Now the microphone or soundcard name should appear in the list as an additional entry.

### 10. Check if $arecord$ command lists the input devices
```bash
arecord -l
```

### 11. Reboot the Raspberry Pi
```bash
sudo reboot
```

### 12. After rebooting check if $arecord$ command is working
```bash
# Records a 5 second test audio as wav file
arecord --duration=5 sample.wav

# Delete the test file
rm sample.wav
```

### 13. Add influx-db yaml file (`influxdb_api.yaml`) to config folder

### 14. Add the device to Zerotier account

Follow the instructions on [Zerotier for Raspberry Pi Tutorial](https://pimylifeup.com/raspberry-pi-zerotier/). Go to  [Zerotier](https://my.zerotier.com/) platform and login with the credentials shared via email/open project to monitor/connect to device IPs.

### 15. Add Python scripts to bashrc file  

```bash
nano ~/.bashrc

# Appened the following line to the end of .bashrc file
source ~/venv/bin/activate
python3 /home/ubuntu/raingauge/code/daq_pi.py

# Reboot the device
sudo reboot
```


