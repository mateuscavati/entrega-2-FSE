from uart import UART

from protocols.simple_protocol import SimpleProtocol
from protocols.modbus_protocol import ModbusProtocol


uart = UART()

simple = SimpleProtocol(uart)

modbus = ModbusProtocol(uart)


while True:
    print("\n==============================")
    print("PROTOCOLO")
    print("==============================")
    print("1 - Simplificado")
    print("2 - MODBUS")
    print("0 - Sair")

    protocol_choice = input("Escolha: ")

    if protocol_choice == '0':
        break

    print("\n==============================")
    print("COMANDOS")
    print("==============================")
    print("1 - Solicitar inteiro")
    print("2 - Solicitar float")
    print("3 - Solicitar string")
    print("4 - Enviar inteiro")
    print("5 - Enviar float")
    print("6 - Enviar string")

    cmd = input("Escolha: ")

    protocol = simple if protocol_choice == '1' else modbus

    if cmd == '1':
        protocol.request_int()

    elif cmd == '2':
        protocol.request_float()

    elif cmd == '3':
        protocol.request_string()

    elif cmd == '4':
        value = int(input("Digite o inteiro: "))

        protocol.send_int(value)

    elif cmd == '5':
        value = float(input("Digite o float: "))

        protocol.send_float(value)

    elif cmd == '6':
        text = input("Digite a string: ")

        protocol.send_string(text)

    else:
        print("Comando inválido")

uart.close()