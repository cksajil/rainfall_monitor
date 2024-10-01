import time
from Adafruit_ADS1x15 import ADS1115


# Create an ADS1115 ADC instance
adc = ADS1115()

# Set the gain (1 means +/- 4.096V)
gain = 1

# Select the channel where the sensor is connected
channel = 0  # Assuming the sensor is connected to A0

try:
    while True:
        # Read the ADC value
        moisture_value = adc.read_adc(channel, gain)

        # Convert the raw value to a moisture percentage (0 to 100)
        # This conversion may vary based on your calibration
        moisture_percentage = (moisture_value / 32767.0) * 100

        print(f"Moisture Level: {moisture_percentage:.2f}%")

        # Wait before the next reading
        time.sleep(1)

except KeyboardInterrupt:
    print("Program terminated.")
