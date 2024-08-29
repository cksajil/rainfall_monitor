import serial
import serial.tools.list_ports
import time


def list_ports():
    """List all available ports and their descriptions."""
    ports = list(serial.tools.list_ports.comports())
    for port in ports:
        print(
            f"Port: {port.device}, Description: {port.description}, HWID: {port.hwid}"
        )
    return ports


def receive_data(port_name, baudrate=9600):
    """Receive data from the specified serial port."""
    try:
        with serial.Serial(port_name, baudrate, timeout=1) as ser:
            print(f"Listening on {port_name}...")
            while True:
                if ser.in_waiting > 0:
                    data = ser.read(ser.in_waiting).decode("utf-8")
                    print(f"Received data: {data}")
                time.sleep(0.1)  # Add a small delay to avoid high CPU usage
    except serial.SerialException as e:
        print(f"Error opening or using serial port {port_name}: {e}")


def main():
    ports = list_ports()
    if not ports:
        print("No active serial ports found.")
        return

    # Example: Select the first port (you might want to specify which port to use)
    port_name = ports[0].device

    receive_data(port_name)


if __name__ == "__main__":
    main()
