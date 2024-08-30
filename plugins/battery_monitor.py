import sys
import serial
import struct


def setup_serial_connection(port, baudrate, timeout=1):
    try:
        ser = serial.Serial(port, baudrate=baudrate, timeout=timeout)
        return ser
    except serial.SerialException as e:
        sys.exit(1)


def read_int8(serial_connection):
    try:
        byte = serial_connection.read(1)
        if byte:
            value = struct.unpack("b", byte)[0]
            return value
        else:
            return None
    except Exception as e:
        return None


def process_data(values):
    if len(values) == 4:
        solar_voltage = values[0] / 10.0
        battery_voltage = values[1] / 10.0
        solar_current = values[2] / 10.0
        battery_current = values[3] / 10.0
        return solar_voltage, battery_voltage, solar_current, battery_current
    else:
        return None


def preprocess_dataframe(ser):
    values = []

    # Read data until start marker (21) is found
    while True:
        value = read_int8(ser)
        if value == 21:
            break

    # Read the next four values
    for _ in range(4):
        value = read_int8(ser)
        if value is not None:
            values.append(value)

    # Read until end marker (75) is found
    while True:
        value = read_int8(ser)
        if value == 75:
            break

    # Process and return the values
    return process_data(values)
