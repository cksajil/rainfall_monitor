import time
from serial import Serial, SerialException

serial_port = "/dev/ttyS0"  # Adjust based on your setup

try:
    ser = Serial(port=serial_port, baudrate=9600, timeout=1)
    print(f"Connected to {serial_port}")
    time.sleep(2)

    while True:
        message = "Hello from Raspberry Pi 5\n"
        ser.write(message.encode("utf-8"))
        print(f"Sent: {message.strip()}")
        time.sleep(1)

except SerialException as e:
    print(f"SerialException: {e}")

except OSError as e:
    print(f"OSError: {e}")

finally:
    ser.close()
