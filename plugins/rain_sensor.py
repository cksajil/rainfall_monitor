import os
import yaml
import time
import RPi.GPIO as GPIO


def load_config(config_name: str, CONFIG_PATH="/home/pi/raingauge/code/config") -> dict:
    """
    A function to load and return config file in YAML format
    """
    with open(os.path.join(CONFIG_PATH, config_name)) as file:
        config = yaml.safe_load(file)
    return config


config = load_config("config.yaml")
POWER_PIN = config["rain_sensor_power_pin"]
RAIN_PIN = config["rain_sensor_input_pin"]


def setup_rain_sensor_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(POWER_PIN, GPIO.OUT)  # configure the power pin as an OUTPUT
    GPIO.setup(RAIN_PIN, GPIO.IN)


def enable_rain_sensor():
    GPIO.output(POWER_PIN, GPIO.HIGH)


def disable_rain_sensor():
    GPIO.output(POWER_PIN, GPIO.LOW)


def read_rain_sensor():
    rain_status = GPIO.input(RAIN_PIN)
    return rain_status


def gpio_cleanup():
    GPIO.cleanup([POWER_PIN, RAIN_PIN])


def read_loop():
    setup_rain_sensor_gpio()
    enable_rain_sensor()
    time.sleep(0.01)
    rain_status = read_rain_sensor()
    disable_rain_sensor()
    gpio_cleanup()
    return rain_status


if __name__ == "__main__":
    try:
        setup_rain_sensor_gpio()
        while True:
            enable_rain_sensor()
            time.sleep(0.01)
            rain_status = read_rain_sensor()
            disable_rain_sensor()
            if rain_status == GPIO.HIGH:
                print("The rain is NOT detected")
            else:
                print("The rain is detected")
            time.sleep(1)
    except KeyboardInterrupt:
        gpio_cleanup()
