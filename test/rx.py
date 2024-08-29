import os
import time
import select
import threading
from serial import Serial, SerialException


def find_active_serial_ports():
    serial_ports = [
        f"/dev/{dev}"
        for dev in os.listdir("/dev")
        if dev.startswith("ttyS")
        or dev.startswith("ttyAMA")
        or dev.startswith("ttyUSB")
    ]

    return serial_ports


def read_from_serial(ser):
    while True:
        try:
            # Check if data is available to read
            readable, _, _ = select.select([ser], [], [], 1)
            if readable:
                message = ser.readline().decode("utf-8").strip()
                if message:
                    print(f"Received: {message}")
            else:
                print("No data incoming")
        except Exception as e:
            print(f"Error reading from serial port: {e}")
            break


def main():
    active_ports = find_active_serial_ports()

    if not active_ports:
        print("No active serial ports found.")
        return

    # Use the first active port found
    serial_port = active_ports[0]
    print(f"Using serial port: {serial_port}")

    try:
        ser = Serial(port=serial_port, baudrate=9600, timeout=1)
        print(f"Connected to {serial_port}")

        # Start the reading thread
        read_thread = threading.Thread(target=read_from_serial, args=(ser,))
        read_thread.start()

        # Allow the reading thread to run
        read_thread.join()

    except SerialException as e:
        print(f"SerialException: {e}")
    except OSError as e:
        print(f"OSError: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        if ser and ser.is_open:
            ser.close()


if __name__ == "__main__":
    main()
