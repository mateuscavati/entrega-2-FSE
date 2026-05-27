import struct

from crc16 import crc16


class ModbusProtocol:
    def __init__(self, uart):
        self.uart = uart

        self.address = 0x01

        self.matricula = bytes([0, 0, 6, 9, 9, 1])

    # =========================
    # UTILITÁRIOS
    # =========================

    def build_frame(self, function, payload):
        frame = (
            bytes([self.address]) +
            bytes([function]) +
            payload +
            self.matricula
        )

        crc = crc16(frame)

        frame += struct.pack('<H', crc)

        return frame

    def validate_crc(self, data):
        if len(data) < 2:
            return False

        received_crc = struct.unpack('<H', data[-2:])[0]

        calc_crc = crc16(data[:-2])

        return received_crc == calc_crc

    def check_exception(self, data):
        if len(data) < 3:
            return False

        function = data[1]

        if function & 0x80:
            code = data[2]

            print(f"[ERRO MODBUS] Código de exceção: {code}")

            return True

        return False

    # =========================
    # SOLICITAÇÕES
    # =========================

    def request_int(self):
        payload = bytes([0xA1])

        frame = self.build_frame(0x23, payload)

        self.uart.send(frame)

        resp = self.uart.receive_all()

        if len(resp) < 8:
            print("[ERRO] Resposta inválida")
            return

        if not self.validate_crc(resp):
            print("[ERRO] CRC inválido")
            return

        if self.check_exception(resp):
            return

        value = struct.unpack('<i', resp[2:6])[0]

        print("CRC OK")
        print(f"Inteiro recebido: {value}")

    def request_float(self):
        payload = bytes([0xA2])

        frame = self.build_frame(0x23, payload)

        self.uart.send(frame)

        resp = self.uart.receive_all()

        if len(resp) < 8:
            print("[ERRO] Resposta inválida")
            return

        if not self.validate_crc(resp):
            print("[ERRO] CRC inválido")
            return

        if self.check_exception(resp):
            return

        value = struct.unpack('<f', resp[2:6])[0]

        print("CRC OK")
        print(f"Float recebido: {value}")

    def request_string(self):
        payload = bytes([0xA3])

        frame = self.build_frame(0x23, payload)

        self.uart.send(frame)

        resp = self.uart.receive_all()

        if len(resp) < 6:
            print("[ERRO] Resposta inválida")
            return

        if not self.validate_crc(resp):
            print("[ERRO] CRC inválido")
            return

        if self.check_exception(resp):
            return

        size = resp[2]

        text = resp[3:3 + size].decode(errors='ignore')

        print("CRC OK")
        print(f"String recebida: {text}")

    # =========================
    # ENVIOS
    # =========================

    def send_int(self, value):
        payload = (
            bytes([0xB1]) +
            struct.pack('<i', value)
        )

        frame = self.build_frame(0x16, payload)

        self.uart.send(frame)

        resp = self.uart.receive_all()

        if len(resp) < 8:
            print("[ERRO] Resposta inválida")
            return

        if not self.validate_crc(resp):
            print("[ERRO] CRC inválido")
            return

        if self.check_exception(resp):
            return

        result = struct.unpack('<i', resp[2:6])[0]

        print("CRC OK")
        print(f"Resultado recebido: {result}")

    def send_float(self, value):
        payload = (
            bytes([0xB2]) +
            struct.pack('<f', value)
        )

        frame = self.build_frame(0x16, payload)

        self.uart.send(frame)

        resp = self.uart.receive_all()

        if len(resp) < 8:
            print("[ERRO] Resposta inválida")
            return

        if not self.validate_crc(resp):
            print("[ERRO] CRC inválido")
            return

        if self.check_exception(resp):
            return

        result = struct.unpack('<f', resp[2:6])[0]

        print("CRC OK")
        print(f"Resultado recebido: {result}")

    def send_string(self, text):
        encoded = text.encode()

        payload = (
            bytes([0xB3]) +
            bytes([len(encoded)]) +
            encoded
        )

        frame = self.build_frame(0x16, payload)

        self.uart.send(frame)

        resp = self.uart.receive_all()

        if len(resp) < 6:
            print("[ERRO] Resposta inválida")
            return

        if not self.validate_crc(resp):
            print("[ERRO] CRC inválido")
            return

        if self.check_exception(resp):
            return

        size = resp[2]

        text = resp[3:3 + size].decode(errors='ignore')

        print("CRC OK")
        print(f"Resposta: {text}")