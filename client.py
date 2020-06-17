import socket
import sys
import getopt

PORT = None
SERVER = None

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


while True:

    msg = input("Please enter message: \n")
    send(msg)

    if msg == DISCONNECT_MSG:
        break


print(f"[DISCONNECTED] This device has disconnected from {SERVER}")

