import serial
import struct
import sys
import time


def setup_serial_connection(port, baudrate, timeout):
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
        pass


def main():
    port = "/dev/ttyS0"  # Adjust as needed
    baudrate = 9600
    timeout = 1

    ser = setup_serial_connection(port, baudrate, timeout)

    try:
        while True:
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

            # Process and print the values
            solar_voltage, battery_voltage, solar_current, battery_current = (
                process_data(values)
            )
            print(f"Solar Voltage: {solar_voltage:.1f} V")
            print(f"Battery Voltage: {battery_voltage:.1f} V")
            print(f"Solar Current: {solar_current:.1f} A")
            print(f"Battery Current: {battery_current:.1f} A")

            # Wait for 3 minutes before the next reading
            time.sleep(180)

    except KeyboardInterrupt:
        print("Battery monitory interrupted by user.")
    finally:
        ser.close()
        print("Serial port closed.")


if __name__ == "__main__":
    main()
