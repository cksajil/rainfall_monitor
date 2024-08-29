import serial.tools.list_ports


def list_ports():
    """List all available ports and their descriptions."""
    ports = list(serial.tools.list_ports.comports())
    for port in ports:
        print(
            f"Port: {port.device}, Description: {port.description}, HWID: {port.hwid}"
        )
    return ports


def main():
    active_ports = list_ports()
    print(active_ports)
    if not active_ports:
        print("No active serial ports found.")
        return


if __name__ == "__main__":
    main()
