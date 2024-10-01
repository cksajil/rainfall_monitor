import time
from Adafruit_ADS1x15 import ADS1115

adc = ADS1115()
channel = 0  # Change if needed

try:
    while True:
        value = adc.read_adc(channel, gain=10)
        print(f"Raw value: {value}")
        time.sleep(0.2)

except Exception as e:
    print(f"Error: {e}")
