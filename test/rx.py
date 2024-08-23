import time
from serial import Serial, SerialException

serial_port = "/dev/ttyS0"  # Adjust based on your setup

try:
    ser = Serial(port=serial_port, baudrate=9600, timeout=1)
    print(f"Connected to {serial_port}")
    time.sleep(2)

    while True:
        if ser.in_waiting > 0:
            message = ser.readline().decode("utf-8").strip()
            print(f"Received: {message}")
        else:
            print("Waiting for data...")
        time.sleep(1)

except SerialException as e:
    print(f"SerialException: {e}")

except OSError as e:
    print(f"OSError: {e}")

finally:
    ser.close()
