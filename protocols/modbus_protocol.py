import struct

from crc16 import crc16


class ModbusProtocol:
    def __init__(self, uart):
        self.uart = uart

        # TESTAR 0x00 PRIMEIRO
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

        print(f"CRC Calculado: 0x{crc:04X}")

        # CRC little-endian
        frame += struct.pack('<H', crc)

        return frame

    def validate_crc(self, data):
        if len(data) < 2:
            return False

        received_crc = struct.unpack('<H', data[-2:])[0]

        calc_crc = crc16(data[:-2])

        print(f"CRC Recebido: 0x{received_crc:04X}")
        print(f"CRC Calculado: 0x{calc_crc:04X}")

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
    # SOLICITA INT
    # =========================

    def request_int(self):
        payload = bytes([0xA1])

        frame = self.build_frame(0x23, payload)

        self.uart.send(frame)

        resp = self.uart.receive(8)

        if len(resp) != 8:
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

    # =========================
    # SOLICITA FLOAT
    # =========================

    def request_float(self):
        payload = bytes([0xA2])

        frame = self.build_frame(0x23, payload)

        self.uart.send(frame)

        resp = self.uart.receive(8)

        if len(resp) != 8:
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

    # =========================
    # SOLICITA STRING
    # =========================

    def request_string(self):
        payload = bytes([0xA3])

        frame = self.build_frame(0x23, payload)

        self.uart.send(frame)

        header = self.uart.receive(3)

        if len(header) != 3:
            print("[ERRO] Resposta inválida")
            return

        size = header[2]

        if size > 200:
            print("[ERRO] Tamanho inválido")
            return

        body = self.uart.receive(size + 2)

        if len(body) != size + 2:
            print("[ERRO] Resposta inválida")
            return

        resp = header + body

        if not self.validate_crc(resp):
            print("[ERRO] CRC inválido")
            return

        if self.check_exception(resp):
            return

        text = resp[3:3 + size].decode(errors='ignore')

        print("CRC OK")
        print(f"String recebida: {text}")

    # =========================
    # ENVIA INT
    # =========================

    def send_int(self, value):
        payload = (
            bytes([0xB1]) +
            struct.pack('<i', value)
        )

        frame = self.build_frame(0x16, payload)

        self.uart.send(frame)

        resp = self.uart.receive(8)

        if len(resp) != 8:
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

    # =========================
    # ENVIA FLOAT
    # =========================

    def send_float(self, value):
        payload = (
            bytes([0xB2]) +
            struct.pack('<f', value)
        )

        frame = self.build_frame(0x16, payload)

        self.uart.send(frame)

        resp = self.uart.receive(8)

        if len(resp) != 8:
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

    # =========================
    # ENVIA STRING
    # =========================

    def send_string(self, text):
        encoded = text.encode()

        payload = (
            bytes([0xB3]) +
            bytes([len(encoded)]) +
            encoded
        )

        frame = self.build_frame(0x16, payload)

        self.uart.send(frame)

        header = self.uart.receive(3)

        if len(header) != 3:
            print("[ERRO] Resposta inválida")
            return

        size = header[2]

        if size > 200:
            print("[ERRO] Tamanho inválido")
            return

        body = self.uart.receive(size + 2)

        if len(body) != size + 2:
            print("[ERRO] Resposta inválida")
            return

        resp = header + body

        if not self.validate_crc(resp):
            print("[ERRO] CRC inválido")
            return

        if self.check_exception(resp):
            return

        response_text = resp[3:3 + size].decode(errors='ignore')

        print("CRC OK")
        print(f"Resposta: {response_text}")