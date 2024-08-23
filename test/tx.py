import time
from serial import Serial, SerialException

# Specify the serial port for Raspberry Pi 5
serial_port = "/dev/serial0"  # This might be /dev/ttyS0 or /dev/ttyAMA0 depending on your configuration

try:
    # Configure serial communication
    ser = Serial(port=serial_port, baudrate=9600, timeout=1)
    print(f"Connected to {serial_port}")
    time.sleep(2)

    try:
        while True:
            # Example data to send
            battery_voltage = "3.7"  # Replace with actual data or computation
            message = f"Battery Voltage: {battery_voltage}V\n"

            # Send data over serial
            ser.write(message.encode("utf-8"))
            print(f"Sent: {message.strip()}")

            time.sleep(1)  # Delay before sending next message

    except KeyboardInterrupt:
        print("Program terminated by user")
    finally:
        ser.close()

except SerialException as e:
    print(f"Error: {e}")
