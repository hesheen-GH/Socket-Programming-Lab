import socket
import threading
import getopt
import sys


#server is this DESKTOP

SERVER = socket.gethostbyname(socket.gethostname()) #default
PORT = 8888 #default

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


MAX_PACKET_SIZE = 255 #max possible bytes
HEADER_LENGTH = 20
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'ISO-8859-1'
DISCONNECT_MSG = "!DISCONNECT"
MOD = 1 << 16

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def ones_comp_add16(num1,num2):

    result = num1 + num2
    return result if result < MOD else (result+1) % MOD

def generate_checksum(datawords):

    sum = 0x0000

    for i in datawords:
        sum = ones_comp_add16(sum, int('0x' + i, 16))

    return sum ^ 0xFFFF

def handle_client(conn, addr):

    print(f"[NEW CONNECTION] {addr} connected. ")

    connected = True
    while connected:

        message = []
        packet_length = int.from_bytes(conn.recv(MAX_PACKET_SIZE), byteorder='big')

        if packet_length:

            packet = conn.recv(packet_length) #contains packet information in bytes format
            packet = hex(int.from_bytes(packet, 'big'))[2:]

            if (len(packet) % 8) != 0:
                packet.zfill(2 * (8 - (packet_length % 8)))

            packet = [packet[i:i + 4] for i in range(0, len(packet), 4)]
            header = packet[0:10]

            payload = "".join(packet[10:])
            payload = [payload[i:i+2] for i in range(0, len(payload), 2)]

            for i in payload:
                message.append(bytes.fromhex(i).decode(FORMAT))

            message = ''.join(message)

            if message == DISCONNECT_MSG:
                connected = False

            print(f"The data recieved from [{addr}] is {message}\n")
            print(f"Total packet length received {packet_length} bytes\n")
            print(f"Payload length received {len(bytes.fromhex(message.encode(FORMAT).hex()))} bytes\n")

            chksm = generate_checksum(header)

            if chksm == 0:
                print("The verification of the checksum demonstrates the packet is correct\n")

            else:
                print("The verification of the checksum demonstrates the packet is corrupted, packet discarded!\n")


            conn.send("Msg recieved".encode(FORMAT))

    conn.close()
    print(f"[DISCONNECTED] CLIENT {addr} has disconnected")


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on IP: {SERVER}, PORT: {PORT}")

    while True:
        conn, addr = server.accept() #when connection occurs store in conn and addr

        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")




print("[STARTING] server is starting... ")
start()