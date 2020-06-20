import socket
import sys
import getopt
import binascii

PORT = None
SERVER = None
CLIENT = None

#Constants-----------------
HEADER_LENGTH = 20
VERSION = '0x4500'
ID_FIELD = '0x1c46'
FLAGS_OFFSET = '0x4000'
TTL_PROTOCOL = '0x4006'
MOD = 1 << 16
FORMAT = 'ISO-8859-1'
DISCONNECT_MSG = "!DISCONNECT"
#---------------------------

#Methods
#---------------------------

def send(packet, packet_length):

    packet_length = bytes([packet_length])
    client.send(packet_length)
    client.send(packet)

def ones_comp_add16(num1,num2):

    result = num1 + num2
    return result if result < MOD else (result+1) % MOD

def generate_checksum(datawords):

    sum = 0x0000

    for i in datawords:
        sum = ones_comp_add16(sum, int('0x' + i, 16))

    sum = hex(sum ^ 0xFFFF)[2:]

    while len(sum) != 4:
        sum = '0' + sum

    return sum

def add_ip_header(src_ip, dest_ip):

    src_ip = list(map(int, src_ip.split('.')))
    dest_ip = list(map(int, dest_ip.split('.')))

    for i in range(0, len(src_ip)):
        src_ip[i] = hex(src_ip[i])[2:]

        while len(src_ip[i]) != 2:
            src_ip[i] = '0' + src_ip[i]


    for i in range(0, len(dest_ip)):
        dest_ip[i] = hex(dest_ip[i])[2:]

        while len(dest_ip[i]) != 2:
            dest_ip[i] = '0' + dest_ip[i]

    src_ip = [''.join(src_ip)[:4], ''.join(src_ip)[4:]]
    dest_ip = [''.join(dest_ip)[:4], ''.join(dest_ip)[4:]]

    return src_ip, dest_ip

def add_header_length(total_len):

    total_length = hex(total_len)[2:]

    if int('0x' + total_length, 16) > 65535:
        raise OverflowError

    else:
        while len(total_length) != 4:
            total_length = '0' + total_length

        return total_length
#------------------------------

argumentList = sys.argv[1:]

# Options
options = "s:c:p:"

# Long options
long_options = ["Server =", "Client =", "Port ="]

try:
    # Parsing argument
    arguments, values = getopt.getopt(argumentList, options, long_options)

    # checking each argument
    for currentArgument, currentValue in arguments:

        if currentArgument in ("-s", "--Server"):
            SERVER = str(currentValue)

        elif currentArgument in ("-c", "--Client"):
            CLIENT = str(currentValue)

        elif currentArgument in ("-p", "--Port"):
            PORT = int(currentValue)


except getopt.error as err:
    # output error, and return with an error code
    print(str(err))


ADDR = (SERVER, PORT)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


while True:

    PADDING = ''
    payload = input("Please enter message: \n")

    TOTAL_LENGTH = HEADER_LENGTH + len(payload.encode(FORMAT))

    if (TOTAL_LENGTH % 8) != 0:
        PADDING = ''.zfill(2*(8 - (TOTAL_LENGTH % 8)))

    TOTAL_LENGTH = TOTAL_LENGTH + len(PADDING)

    SOURCE_IP, DEST_IP = add_ip_header(CLIENT, SERVER)

    DATAWORDS = [VERSION[2:], add_header_length(TOTAL_LENGTH), ID_FIELD[2:], FLAGS_OFFSET[2:], TTL_PROTOCOL[2:],
                 SOURCE_IP[0], SOURCE_IP[1], DEST_IP[0], DEST_IP[1]]

    CHECKSUM = generate_checksum(DATAWORDS)

    packet = '0x' + ''.join(
        VERSION[2:] + add_header_length(TOTAL_LENGTH) + ID_FIELD[2:] + FLAGS_OFFSET[2:] + TTL_PROTOCOL[2:]
        + CHECKSUM + SOURCE_IP[0] + SOURCE_IP[1] + DEST_IP[0] + DEST_IP[1] + payload.encode(
            FORMAT).hex() + PADDING)

    packet = int(packet, 16)
    packet = packet.to_bytes(TOTAL_LENGTH, 'big')

    send(packet, TOTAL_LENGTH)

    if payload == DISCONNECT_MSG:
        break


print(f"[DISCONNECTED] This device has disconnected from {SERVER}")

