import serial
import time


class UART:
    def __init__(self, port="/dev/serial0", baudrate=115200, timeout=2):
        self.ser = serial.Serial(
            port=port,
            baudrate=baudrate,
            bytesize=8,
            parity='N',
            stopbits=1,
            timeout=timeout
        )

    def send(self, data: bytes):
        print("\n==============================")
        print("TX:", data.hex(' ').upper())
        print("==============================")

        self.ser.write(data)

    def receive(self, size: int):
        data = self.ser.read(size)

        if len(data) == 0:
            print("[ERRO] Timeout")
            return b''

        print("RX:", data.hex(' ').upper())

        return data

    def receive_all(self):
        time.sleep(0.1)

        data = self.ser.read_all()

        if len(data) == 0:
            print("[ERRO] Timeout")
            return b''

        print("RX:", data.hex(' ').upper())

        return data

    def close(self):
        self.ser.close()