import socket
import threading

#server is this DESKTOP

MAX_PACKET_SIZE = 255 #max possible bytes
HEADER_LENGTH = 20
PORT = 8888
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'ISO-8859-1'
DISCONNECT_MSG = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):

    print(f"[NEW CONNECTION] {addr} connected. ")

    connected = True
    while connected:

        packet_length = int.from_bytes(conn.recv(MAX_PACKET_SIZE), byteorder='big')

        if packet_length:

            packet = conn.recv(packet_length) #contains packet information in bytes format
            payload = packet[HEADER_LENGTH:]
            payload = payload.decode(FORMAT, errors='ignore')

            if payload == DISCONNECT_MSG:
                connected = False

            print(f"The data recieved from [{addr}] is {payload}")
            print(f"Total packet length received {packet_length} bytes")
            print(f"Payload length received {packet_length-20} bytes")

            conn.send("Msg recieved".encode(FORMAT))

    conn.close()
    print(f"[DISCONNECTED] CLIENT {addr} has disconnected")


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")

    while True:
        conn, addr = server.accept() #when connection occurs store in conn and addr

        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")



print("[STARTING] server is starting... ")
start()