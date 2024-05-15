import RPi.GPIO as GPIO
from .helper import load_config
import time

config = load_config("config.yaml")
POWER_PIN = config["rain_gpio_power_pin"]
RAIN_PIN = config["rain_gpio_input_pin"]


def setup_rain_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(POWER_PIN, GPIO.OUT)  # configure the power pin as an OUTPUT
    GPIO.setup(RAIN_PIN, GPIO.IN)


def enable_rain_sensor():
    GPIO.output(POWER_PIN, GPIO.HIGH)


def disable_rain_sensor():
    GPIO.output(POWER_PIN, GPIO.LOW)


def gpio_cleanup():
    GPIO.cleanup()


def read_rain_sensor():
    rain_state = GPIO.input(RAIN_PIN)
    return rain_state


def read_loop():
    enable_rain_sensor()
    time.sleep(0.01)

    rain_state = read_rain_sensor()
    disable_rain_sensor()

    if rain_state == GPIO.HIGH:
        print("The rain is NOT detected")
    else:
        print("The rain is detected")

    time.sleep(1)


if __name__ == "__main__":
    try:
        setup_rain_gpio()
        while True:
            read_loop()
    except KeyboardInterrupt:
        gpio_cleanup()
