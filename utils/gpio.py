import RPi.GPIO as GPIO
from .helper import load_config


config = load_config("config.yaml")
POWER_PIN = config["rain_gpi0_power_pin"]
RAIN_PIN = config["rain_gpio_input_pin"]


def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(POWER_PIN, GPIO.OUT)  # configure the power pin as an OUTPUT
    GPIO.setup(RAIN_PIN, GPIO.IN)
