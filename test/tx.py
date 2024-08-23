ChatGPT 4o mini

Log in

Sign up
You said:
i am tryring uart communication between two raspberry pis. I want to send data from raspberry pi5 to raspberry pi 4. Following is the code at the pi4. write me code to send data at raspberry pi 5. import time
from serial import Serial, SerialException


serial_port = "/dev/serial0"

try:

    ser = Serial(port=serial_port, baudrate=9600, timeout=1)
    print(f"Connected to {serial_port}")
    time.sleep(2)

    try:
        while True:
            if ser.in_waiting > 0:
                print("Reading battery voltage")
                voltage = ser.readline().decode("utf-8").strip()
                print(f"Battery Voltage: {voltage}V")
            else:
                print("Not inside SER waiting")
            time.sleep(1)
    except KeyboardInterrupt:
        print("Program terminated by user")
    finally:
        ser.close()

except SerialException as e:
    print(f"Error: {e}")
ChatGPT said:
ChatGPT
To send data from a Raspberry Pi 5 to a Raspberry Pi 4 using UART, you'll need to set up serial communication properly on both devices. You've provided the code for receiving data on the Raspberry Pi 4, so now I'll give you the code to send data from the Raspberry Pi 5.

Here’s how you can write the Python script for the Raspberry Pi 5 to send data:

Ensure Serial Communication Setup:
Make sure the UART is enabled on both Raspberry Pi boards and that they are connected via the GPIO pins.

Send Data from Raspberry Pi 5:

Here’s a Python script that you can run on the Raspberry Pi 5 to send data over UART:

python
Copy code
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
            ser.write(message.encode('utf-8'))
            print(f"Sent: {message.strip()}")
            
            time.sleep(1)  # Delay before sending next message

    except KeyboardInterrupt:
        print("Program terminated by user")
    finally:
        ser.close()

except SerialException as e:
    print(f"Error: {e}")
