# Enable I2C in sudo raspi-config and reboot
# Check I2C
# i2cdetect -y 1


# ADS1115
# VDD - 5V
# GND - GND
# SCL - SCL.1 (Physical 5)
# SDA - SDA.1 (Physical 3)
# ADDR - GND
# A0 - Grove moisture Sensor output


import time
from Adafruit_ADS1x15 import ADS1115

adc = ADS1115()
channel = 0  # Change if needed

try:
    while True:
        value = adc.read_adc(channel, gain=1)
        print(f"Raw value: {value}")
        time.sleep(0.2)

except Exception as e:
    print(f"Error: {e}")
