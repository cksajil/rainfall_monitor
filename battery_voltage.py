import time
from serial import Serial, SerialException
from serial.tools import list_ports



def list_ports():
    ports = list(list_ports.comports())
    for port in ports:
        print(f"Port: {port.device}, Description: {port.description}, HWID: {port.hwid}")
    return ports


# print(list_ports())
serial_port = "/dev/serial0"

try:
    
    ser = Serial(port=serial_port,
        baudrate=9600,
        timeout=1)
    print(f"Connected to {serial_port}")
    time.sleep(2)  

    try:
        while True:
            if ser.in_waiting > 0:
                voltage = ser.readline().decode("utf-8").strip()
                print(f"Battery Voltage: {voltage}V")
            time.sleep(1)
    except KeyboardInterrupt:
        print("Program terminated")
    finally:
        ser.close()

 except SerialException as e:
        print(f"Error: {e}")
