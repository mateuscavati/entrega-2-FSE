def crc16(data: bytes):
    crc = 0xFFFF

    for pos in data:
        crc ^= pos

        for _ in range(8):
            if (crc & 1) != 0:
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1

    return crc & 0xFFFF