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


print("Listening on /dev/ttyS0...")
while True:
    value = read_int8(ser)
    if value is not None:
        print(f"Received int8_t value: {value}")

# Close the serial connection when done
ser.close()
