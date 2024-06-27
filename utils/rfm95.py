# Power Supply: Make sure to power the RFM95 module with 3.3V, not 5V, as the module operates at 3.3V.
# SPI Configuration: Enable SPI on the Raspberry Pi using raspi-config.
# GPIO Pins: Ensure no conflicts with other connected devices or GPIO configurations.

# sudo pip3 install pySX127x lora-pico
# RFM95 Pin   | Raspberry Pi Pin
# ------------------------------
# VCC         | 3.3V (Pin 1)
# GND         | GND (Pin 6)
# SCK         | GPIO11 (Pin 23)
# MISO        | GPIO9 (Pin 21)
# MOSI        | GPIO10 (Pin 19)
# NSS         | GPIO8 (Pin 24)
# RST         | GPIO25 (Pin 22)
# DIO0        | GPIO7 (Pin 26)
# DIO1        | GPIO18 (Pin 12) (optional)
# DIO2        | GPIO23 (Pin 16) (optional)
# DIO3        | GPIO24 (Pin 18) (optional)
# DIO4        | GPIO25 (Pin 22) (optional)


from time import sleep
from SX127x.LoRa import *
from SX127x.board_config import BOARD
from LoRaWAN.LoRaWAN import LoRaWAN
from LoRaWAN.MHDR import MHDR
import binascii

BOARD.setup()


class LoRaRFM95(LoRa):
    def __init__(self, verbose=False):
        super(LoRaRFM95, self).__init__(verbose)
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([1, 0, 0, 0, 0, 0])

    def on_tx_done(self):
        print("TxDone")
        self.set_mode(MODE.STDBY)
        self.set_mode(MODE.TX)
        self.clear_irq_flags(TxDone=1)

    def send_lorawan(self, devaddr, nwkskey, appskey, data):
        lorawan = LoRaWAN.new(nwkskey, appskey)
        lorawan.create(
            MHDR.UNCONF_DATA_UP,
            {"devaddr": devaddr, "fcnt": 1, "data": list(data.encode("utf-8"))},
        )
        payload = lorawan.to_raw()
        self.write_payload(payload)
        self.set_mode(MODE.TX)
        sleep(0.5)
        self.set_mode(MODE.STDBY)


# Define your device address, network session key, and application session key
DEVADDR = [0x26, 0x01, 0x1B, 0xA1]
NWKSKEY = [
    0x1F,
    0xB2,
    0x8D,
    0x22,
    0xF4,
    0xE1,
    0xF3,
    0x7B,
    0x8E,
    0x54,
    0x7A,
    0x67,
    0xC6,
    0x45,
    0x11,
    0x0A,
]
APPSKEY = [
    0xD7,
    0xF7,
    0xE6,
    0xD9,
    0xAC,
    0xE1,
    0x2D,
    0xB7,
    0x55,
    0x1A,
    0xE5,
    0x74,
    0x91,
    0xC7,
    0x9E,
    0xF2,
]

lora = LoRaRFM95(verbose=True)
lora.set_mode(MODE.STDBY)
lora.set_freq(868.0)

try:
    while True:
        lora.send_lorawan(DEVADDR, NWKSKEY, APPSKEY, "Hello, Gateway from ICFOSS!")
        sleep(10)
except KeyboardInterrupt:
    print("Interrupted")
finally:
    lora.set_mode(MODE.SLEEP)
    BOARD.teardown()
