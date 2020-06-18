import socket
import sys
import getopt
import binascii

PORT = None
SERVER = None
DATAWORDS = ['4500', '0028', '1c46', '4000', '4006', 'c0a8', '0003', 'c0a8', '0001']
MOD = 1 << 16

argumentList = sys.argv[1:]

# Options
options = "s:p:"

# Long options
long_options = ["Server =", "Port ="]

try:
    # Parsing argument
    arguments, values = getopt.getopt(argumentList, options, long_options)

    # checking each argument
    for currentArgument, currentValue in arguments:

        if currentArgument in ("-s", "--Server"):
            SERVER = str(currentValue)

        elif currentArgument in ("-p", "--Port"):
            PORT = int(currentValue)


except getopt.error as err:
    # output error, and return with an error code
    print(str(err))


HEADER = 64
FORMAT = 'utf-8'
DISCONNECT_MSG = "!DISCONNECT"

ADDR = (SERVER, PORT)


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):

    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)


def ones_comp_add16(num1,num2):
    result = num1 + num2
    return result if result < MOD else (result+1) % MOD


def generate_checksum(datawords):

    sum = 0x0000

    for i in datawords:
        sum = ones_comp_add16(sum, int.from_bytes(binascii.unhexlify(i), byteorder="big"))

    sum = hex(sum ^ 0xFFFF) #XOR
    return sum



while True:

    payload = input("Please enter message: \n")
    packet = int.from_bytes(
        binascii.unhexlify(''.join(DATAWORDS[0:5]) + generate_checksum(DATAWORDS)[2:] + ''.join(DATAWORDS[5:9]) + payload)
                            , byteorder="big")


    send(packet)

    if payload == DISCONNECT_MSG:
        break


print(f"[DISCONNECTED] This device has disconnected from {SERVER}")

