import time
from Adafruit_ADS1x15 import ADS1115


channel = 0  # Change if needed


def read_moisture_sensor(channel, gain=1):
    adc = ADS1115()
    try:
        moisture_value = adc.read_adc(channel, gain)
    except Exception as e:
        moisture_value = None
    return moisture_value


def main():
    while True:
        value = read_moisture_sensor(channel, gain=1)
        if value:
            print(f"Raw value: {value}")
        else:
            print(f"Cannot read moisture sensor {value}")
        time.sleep(0.2)


if __name__ == "__main__":
    main()

"""
Enable I2C in sudo raspi-config and reboot
Check I2C with the command : i2cdetect -y 1

connection
ADC  Module: ADS1115
VDD - 5V
GND - GND
SCL - SCL.1 (Physical 5)
SDA - SDA.1 (Physical 3)
ADDR - GND
A0 - Grove moisture Sensor output 
"""