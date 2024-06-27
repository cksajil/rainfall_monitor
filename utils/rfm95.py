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
import RPi.GPIO as GPIO
import time


# RFM95 module constants
RFM95_REG_VERSION = 0x42
RFM95_VERSION = 0x12
DIO0_PIN = 7

# Replace with your LoRaWAN parameters
DEVADDR = bytearray([0xFC, 0x00, 0x94, 0x2D])
NWKSKEY = bytearray(
    [
        0xCB,
        0xFA,
        0xF1,
        0xC5,
        0xE0,
        0xB4,
        0x5D,
        0x80,
        0x48,
        0x3A,
        0x63,
        0xCF,
        0xC6,
        0x00,
        0xE5,
        0x9A,
    ]
)
APPSKEY = bytearray(
    [
        0xFA,
        0x98,
        0xEF,
        0x7A,
        0x27,
        0xCD,
        0xE4,
        0xD4,
        0xFB,
        0x33,
        0xB9,
        0x24,
        0x46,
        0x51,
        0x21,
        0xBD,
    ]
)


def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(DIO0_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


def wait_for_interrupt():
    setup_gpio()

    # Use edge detection to wait for rising edge (packet received)
    try:
        GPIO.wait_for_edge(DIO0_PIN, GPIO.RISING)
        return True
    except KeyboardInterrupt:
        return False
    finally:
        GPIO.cleanup()


# Initialize SPI
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 500000

# Initialize I2C
bus = smbus2.SMBus(1)  # Use 1 for Raspberry Pi Model B+
i2c_address = 0x6B

# LoRaWAN packet constants
CONFIRMED_DATA_UP = 0x80
UNCONFIRMED_DATA_UP = 0x40
FPORT = 1


def setup():
    # Check RFM95 module version
    version = spi.xfer2([RFM95_REG_VERSION, 0])[1]
    if version != RFM95_VERSION:
        print("RFM95 module not found!")
        return False
    print("RFM95 module found")
    return True


def send_data(message, confirmed=False):
    if confirmed:
        packet_type = CONFIRMED_DATA_UP
    else:
        packet_type = UNCONFIRMED_DATA_UP

    # Construct LoRaWAN payload
    payload = bytes([FPORT]) + bytes(message, "utf-8")

    # Encrypt payload if necessary (AES-128 encryption)
    encrypted_payload = encrypt_payload(payload, NWKSKEY, APPSKEY)

    # Construct LoRaWAN packet
    lorawan_packet = bytearray([packet_type])  # Confirmed/Unconfirmed data up
    lorawan_packet += DEVADDR
    lorawan_packet += bytes([0x00])  # FCtrl (ADR + ADRACKReq + ACK + FPending)
    lorawan_packet += bytes([0x00])  # FCnt (Frame counter)
    lorawan_packet += bytes([FPORT])  # FPort
    lorawan_packet += encrypted_payload  # Encrypted payload

    # Send LoRaWAN packet using RFM95 module
    spi.xfer2(lorawan_packet)

    print("Sent message:", message)


def receive_data():
    # Listen for incoming LoRaWAN packets and handle them
    while True:
        # Wait for DIO0 interrupt (packet received)
        dio0 = wait_for_interrupt()

        if dio0:
            # Read incoming packet from RFM95 module
            rx_packet = spi.xfer2(
                [0x00] * 256
            )  # Read up to 256 bytes (adjust as needed)

            # Parse LoRaWAN packet
            lorawan_data = parse_lorawan_packet(rx_packet)

            if lorawan_data:
                # print("Received data:", lorawan_data)

                # Check if ACK is received
                if is_ack(lorawan_data):
                    print("ACK received for last transmission")
                else:
                    # Handle other received data as needed
                    handle_received_data(lorawan_data)


def wait_for_interrupt():
    # Simulate waiting for DIO0 interrupt (not fully implemented here)
    # Replace with actual interrupt handling or polling mechanism
    time.sleep(1)  # Example: wait 1 second for demo purposes
    return True  # Placeholder for demo


def parse_lorawan_packet(packet):
    # Implement parsing of incoming LoRaWAN packet (not fully implemented here)
    # Example: Extract device address, FPort, and payload from packet
    if len(packet) > 0:
        return packet  # Placeholder for demo
    return None


def is_ack(packet):
    # Implement ACK detection logic (not fully implemented here)
    # Example: Check if the packet is an ACK message
    return False  # Placeholder for demo


def handle_received_data(data):
    # Implement handling of received data (not fully implemented here)
    # Example: Process incoming data from LoRaWAN server
    pass


def encrypt_payload(payload, nwskey, appskey):
    # Implement AES-128 encryption (LoRaWAN specification)
    # Example: Dummy encryption (replace with actual AES-128 implementation)
    return payload


# Main execution
if __name__ == "__main__":
    if setup():
        try:
            send_data("Hello, LoRa!", confirmed=True)  # Send confirmed data
            receive_data()  # Listen for acknowledgments or other responses
        except KeyboardInterrupt:
            print("\nTerminated by user")
        finally:
            spi.close()
