import time
import serial


# Setup UART communication
ser = serial.Serial(
    port="/dev/serial0",  # The serial port name
    baudrate=9600,  # Baud rate (ensure this matches your microcontroller)
    timeout=1,  # Timeout for read operations
)

time.sleep(2)  # Give some time for the connection to stabilize

try:
    while True:
        if ser.in_waiting > 0:
            voltage = ser.readline().decode("utf-8").strip()
            print(f"Battery Voltage: {voltage}V")
        time.sleep(1)
except KeyboardInterrupt:
    print("Program terminated")
finally:
    ser.close()
