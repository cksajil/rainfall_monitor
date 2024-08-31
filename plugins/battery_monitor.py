import sys
import serial
import struct
import time


def setup_serial_connection(port, baudrate, timeout=1):
    try:
        ser = serial.Serial(port, baudrate=baudrate, timeout=timeout)
        return ser
    except serial.SerialException as e:
        print(f"Error setting up serial connection: {e}")
        sys.exit(1)


def read_uint8(serial_connection):
    try:
        byte = serial_connection.read(1)
        if byte:
            value = struct.unpack("B", byte)[0]  # Use "B" for unsigned 8-bit integer
            return value
        else:
            return None
    except Exception as e:
        print(f"Error reading from serial: {e}")
        return None


def process_data(values):
    if len(values) == 4:
        solar_voltage = values[0] / 10.0
        battery_voltage = values[1] / 10.0
        solar_current = values[2] / 10.0
        battery_current = values[3] / 10.0
        return solar_voltage, battery_voltage, solar_current, battery_current
    else:
        print(f"Unexpected number of values: {len(values)}")
        return None, None, None, None


def preprocess_dataframe(ser):
    values = []

    # Read data until start marker (21) is found
    while True:
        value = read_uint8(ser)
        if value == 21:
            break
        elif value is None:
            print("Timeout or error while waiting for start marker.")
            return None, None, None, None

    # Read the next four values
    for _ in range(4):
        value = read_uint8(ser)
        if value is not None:
            values.append(value)
        else:
            print("Timeout or error while reading data values.")
            return None, None, None, None

    # Read until end marker (75) is found
    while True:
        value = read_uint8(ser)
        if value == 75:
            break
        elif value is None:
            print("Timeout or error while waiting for end marker.")
            return None, None, None, None

    # Process and return the values
    return process_data(values)


if __name__ == "__main__":
    port = "/dev/ttyS0"  # Adjust to your port
    baudrate = 9600
    ser = setup_serial_connection(port, baudrate)

    while True:
        solar_voltage, battery_voltage, solar_current, battery_current = (
            preprocess_dataframe(ser)
        )

        if solar_voltage is not None:
            print(f"Solar Voltage: {solar_voltage:.1f} V")
            print(f"Battery Voltage: {battery_voltage:.1f} V")
            print(f"Solar Current: {solar_current:.1f} A")
            print(f"Battery Current: {battery_current:.1f} A")
        else:
            print("No valid data received.")

        time.sleep(1)  # Adjust as needed
