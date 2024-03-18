# Audio setup in Raspberry Pi
sudo apt install alsa-utils
sudo apt-get install pulseaudio

# Dependency setup in Raspberry Pi
python3 -m pip install -r requirements.txt

# GPIO setup in Raspberry Pi
sudo apt-get install python3-rpi.gpio
pip install lgpio==0.0.0.2
ls -l /sys/class/gpio/
sudo chmod 777 /sys/class/gpio/export 
sudo echo 6 > /sys/class/gpio/export 
ls /sys/class/gpio/
ls -l /sys/class/gpio/gpio6/ 
sudo chmod 777 /sys/class/gpio/gpio6/direction 
sudo echo in > /sys/class/gpio/gpio6/direction 
ls -l /sys/class/gpio/gpio6/direction 
ls -l /sys/class/gpio/gpio6/edge 
sudo chmod 777 /sys/class/gpio/gpio6/edge 