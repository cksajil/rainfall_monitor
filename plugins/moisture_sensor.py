import time
from Adafruit_ADS1x15 import ADS1115

# Create an ADS1115 ADC instance
adc = ADS1115()

# Set the gain (adjust based on your expected voltage range)
GAIN = 1  # Change as needed (1 for +/- 4.096V)

try:
    while True:
        # Read the value from A0
        moisture_value = adc.read_adc(0, gain=GAIN)
        print(f"Moisture Level: {moisture_value}")
        time.sleep(1)  # Delay for 1 second
except KeyboardInterrupt:
    print("Exiting program")
