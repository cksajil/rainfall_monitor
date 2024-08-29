import time
from serial import Serial, SerialException
import os
import threading


def find_active_serial_ports():
    serial_ports = [
        f"/dev/{dev}"
        for dev in os.listdir("/dev")
        if dev.startswith("ttyS")
        or dev.startswith("ttyAMA")
        or dev.startswith("ttyUSB")
    ]

    return serial_ports


def write_to_serial(ser):
    while True:
        message = "Hello from Raspberry Pi 5\n"
        ser.write(message.encode("utf-8"))
        print(f"Sent: {message.strip()}")
        time.sleep(1)


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
        time.sleep(2)

        # Start the sending thread
        write_thread = threading.Thread(target=write_to_serial, args=(ser,))
        write_thread.start()

        # Wait for the thread to complete (it runs indefinitely)
        write_thread.join()

    except SerialException as e:
        print(f"SerialException: {e}")

    except OSError as e:
        print(f"OSError: {e}")

    finally:
        ser.close()


if __name__ == "__main__":
    main()
