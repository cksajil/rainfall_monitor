import serial
import serial.tools.list_ports


def list_ports():
    """List all available ports and their descriptions."""
    ports = list(serial.tools.list_ports.comports())
    for port in ports:
        print(
            f"Port: {port.device}, Description: {port.description}, HWID: {port.hwid}"
        )
    return ports


def send_data(port_name, data, baudrate=9600):
    """Send data via the specified serial port."""
    try:
        with serial.Serial(port_name, baudrate, timeout=1) as ser:
            ser.write(data.encode("utf-8"))
            print(f"Data sent to {port_name}: {data}")
    except serial.SerialException as e:
        print(f"Error opening or using serial port {port_name}: {e}")


def main():
    ports = list_ports()
    if not ports:
        print("No active serial ports found.")
        return

    # Example: Select the first port (you might want to specify which port to use)
    port_name = ports[0].device
    data_to_send = "Hello, Raspberry Pi!"

    send_data(port_name, data_to_send)


if __name__ == "__main__":
    main()
