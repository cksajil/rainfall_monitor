# Power Supply: Make sure to power the RFM95 module with 3.3V, not 5V, as the module operates at 3.3V.
# SPI Configuration: Enable SPI on the Raspberry Pi using raspi-config.
# GPIO Pins: Ensure no conflicts with other connected devices or GPIO configurations.

#  +----------------------------+       +----------------------------+
#  |        RFM95 Module        |       |        Raspberry Pi 4      |
#  +----------------------------+       +----------------------------+
#  | VCC ------------------- 3.3V (Pin 1)                          |
#  | GND ------------------- GND (Pin 6)                           |
#  | GND (optional)--------- GND (any available GND pin)           |
#  | GND (optional)--------- GND (any available GND pin)           |
#  | SCK ------------------- Pin 23                                |
#  | MISO ------------------ Pin 21                                |
#  | MOSI ------------------ Pin 19                                |
#  | NSS ------------------- Pin 24                                |
#  | RST ------------------- Pin 22                                |
#  | DIO0 ------------------ Pin 26                                |
#  | DIO1 ------------------ Pin 12 (optional)                     |
#  | DIO2 ------------------ Pin 16 (optional)                     |
#  | DIO3 ------------------ Pin 18 (optional)                     |
#  | DIO4 ------------------ Pin 22 (optional)                     |
#  +----------------------------+       +----------------------------+

# sudo pip3 install smbus2 spidev


import time
import spidev
import smbus2

# RFM95 module constants
RFM95_REG_VERSION = 0x42
RFM95_VERSION = 0x12

# Replace with your LoRaWAN parameters
DEVADDR = bytearray([0x00, 0x01, 0x02, 0x03])
NWKSKEY = bytearray(
    [
        0x01,
        0x23,
        0x45,
        0x67,
        0x89,
        0xAB,
        0xCD,
        0xEF,
        0x01,
        0x23,
        0x45,
        0x67,
        0x89,
        0xAB,
        0xCD,
        0xEF,
    ]
)
APPSKEY = bytearray(
    [
        0xFE,
        0xDC,
        0xBA,
        0x98,
        0x76,
        0x54,
        0x32,
        0x10,
        0xFE,
        0xDC,
        0xBA,
        0x98,
        0x76,
        0x54,
        0x32,
        0x10,
    ]
)

# Initialize SPI
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 500000

# Initialize I2C
bus = smbus2.SMBus(1)  # Use 1 for Raspberry Pi Model B+
i2c_address = 0x6B


def setup():
    # Check RFM95 module version
    version = spi.xfer2([RFM95_REG_VERSION, 0])[1]
    if version != RFM95_VERSION:
        print("RFM95 module not found!")
        return False
    print("RFM95 module found")
    return True


def send_data(message):
    # Send data implementation using SPI/I2C
    print("Sending message:", message)
    # Implement your LoRaWAN message sending logic here


# Main execution
if __name__ == "__main__":
    if setup():
        try:
            while True:
                send_data("Hello, LoRa!")
                time.sleep(10)
        except KeyboardInterrupt:
            print("\nTerminated by user")
        finally:
            spi.close()
