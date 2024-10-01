import time
import RPi.GPIO as GPIO


# Setup GPIO pins
CS_PIN = 8
DIN_PIN = 10
DOUT_PIN = 9
CLK_PIN = 11

GPIO.setmode(GPIO.BCM)
GPIO.setup(CS_PIN, GPIO.OUT)
GPIO.setup(DIN_PIN, GPIO.OUT)
GPIO.setup(DOUT_PIN, GPIO.IN)
GPIO.setup(CLK_PIN, GPIO.OUT)


def read_adc(channel):
    if channel > 1:
        return -1

    # Start communication
    GPIO.output(CS_PIN, GPIO.LOW)
    GPIO.output(DIN_PIN, channel)

    # Create a clock pulse
    value = 0
    for _ in range(10):
        GPIO.output(CLK_PIN, GPIO.HIGH)
        value <<= 1
        GPIO.output(CLK_PIN, GPIO.LOW)
        if GPIO.input(DOUT_PIN):
            value |= 0x01

    GPIO.output(CS_PIN, GPIO.HIGH)
    return value


try:
    while True:
        moisture_value = read_adc(0)  # Read from channel 0
        print(f"Moisture Level: {moisture_value}")
        time.sleep(1)  # Delay for 1 second
except KeyboardInterrupt:
    print("Exiting program")
finally:
    GPIO.cleanup()
