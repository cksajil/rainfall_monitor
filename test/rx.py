import serial
import struct

# Set up the serial connection (adjust parameters as needed)
ser = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=1)


def read_int8(serial_connection):
    # Read one byte from the serial port
    byte = serial_connection.read(1)

    if byte:
        # Convert the byte to a signed int8 value
        value = struct.unpack("b", byte)[0]
        return value
    else:
        return None


def process_data(values):
    if len(values) == 4:
        # Divide each value by 10
        solar_voltage = values[0] / 10.0
        battery_voltage = values[1] / 10.0
        solar_current = values[2] / 10.0
        battery_current = values[3] / 10.0

        # Print adjusted values
        print(f"Solar Voltage: {solar_voltage:.1f} V")
        print(f"Battery Voltage: {battery_voltage:.1f} V")
        print(f"Solar Current: {solar_current:.1f} A")
        print(f"Battery Current: {battery_current:.1f} A")
    else:
        print("Unexpected number of values")


def main():
    print("Listening on /dev/ttyS0...")

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
        process_data(values)


if __name__ == "__main__":
    main()

# Close the serial connection when done
ser.close()
