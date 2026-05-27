import struct


class SimpleProtocol:
    def __init__(self, uart):
        self.uart = uart

        self.matricula = bytes([0, 0, 6, 9, 9, 1])

    # =========================
    # SOLICITAÇÕES
    # =========================

    def request_int(self):
        packet = bytes([0xA1]) + self.matricula

        self.uart.send(packet)

        resp = self.uart.receive(4)

        if len(resp) != 4:
            return

        value = struct.unpack('<i', resp)[0]

        print(f"Inteiro recebido: {value}")

    def request_float(self):
        packet = bytes([0xA2]) + self.matricula

        self.uart.send(packet)

        resp = self.uart.receive(4)

        if len(resp) != 4:
            return

        value = struct.unpack('<f', resp)[0]

        print(f"Float recebido: {value}")

    def request_string(self):
        packet = bytes([0xA3]) + self.matricula

        self.uart.send(packet)

        size_data = self.uart.receive(1)

        if len(size_data) != 1:
            return

        size = size_data[0]

        if size > 200:
            print("[ERRO] Tamanho inválido")
            return

        msg = self.uart.receive(size)

        print(f"String recebida: {msg.decode(errors='ignore')}")

    # =========================
    # ENVIOS
    # =========================

    def send_int(self, value: int):
        packet = (
            bytes([0xB1]) +
            struct.pack('<i', value) +
            self.matricula
        )

        self.uart.send(packet)

        resp = self.uart.receive(4)

        if len(resp) != 4:
            return

        result = struct.unpack('<i', resp)[0]

        print(f"Resultado recebido: {result}")

    def send_float(self, value: float):
        packet = (
            bytes([0xB2]) +
            struct.pack('<f', value) +
            self.matricula
        )

        self.uart.send(packet)

        resp = self.uart.receive(4)

        if len(resp) != 4:
            return

        result = struct.unpack('<f', resp)[0]

        print(f"Resultado recebido: {result}")

    def send_string(self, text: str):
        encoded = text.encode()

        size = len(encoded)

        packet = (
            bytes([0xB3]) +
            bytes([size]) +
            encoded +
            self.matricula
        )

        self.uart.send(packet)

        size_data = self.uart.receive(1)

        if len(size_data) != 1:
            return

        resp_size = size_data[0]

        resp = self.uart.receive(resp_size)

        print(f"Resposta: {resp.decode(errors='ignore')}")