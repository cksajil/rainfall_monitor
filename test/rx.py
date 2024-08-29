import time
from serial import Serial, SerialException
import os


def find_active_serial_ports():
    # List all serial devices
    serial_ports = [
        f"/dev/{dev}"
        for dev in os.listdir("/dev")
        if dev.startswith("ttyS")
        or dev.startswith("ttyAMA")
        or dev.startswith("ttyUSB")
    ]
    active_ports = []

    for port in serial_ports:
        try:
            # Open the serial port
            ser = Serial(port=port, baudrate=9600, timeout=1)
            print(f"Testing port: {port}")

            # Attempt to send and receive data
            ser.write(b"Test\n")
            time.sleep(1)
            if ser.in_waiting > 0:
                response = ser.readline().decode("utf-8").strip()
                if response == "Test":
                    print(f"Active port found: {port}")
                    active_ports.append(port)

            ser.close()
        except SerialException as e:
            print(f"SerialException on {port}: {e}")
        except OSError as e:
            print(f"OSError on {port}: {e}")
        except Exception as e:
            print(f"Unexpected error on {port}: {e}")

    return active_ports


def read_from_serial(ser):
    while True:
        if ser.in_waiting > 0:
            message = ser.readline().decode("utf-8").strip()
            if message:
                print(f"Received: {message}")


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

        # Start the reading thread
        read_thread = threading.Thread(target=read_from_serial, args=(ser,))
        read_thread.start()

        # Wait for the thread to complete (it runs indefinitely)
        read_thread.join()

    except SerialException as e:
        print(f"SerialException: {e}")

    except OSError as e:
        print(f"OSError: {e}")

    finally:
        ser.close()


if __name__ == "__main__":
    main()
