import socket
import threading
from constants import *


class Server:
    def __init__(self, host, port, limit_listen):
        self.host = host
        self.port = port
        self.limit_listen = limit_listen
        self.server_socket = socket.socket()
        self.client_sockets = []

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(self.limit_listen)
        print(f'Server is listening on {self.host}:{self.port}...')

        while len(self.client_sockets) < 2:
            client_socket, client_address = self.server_socket.accept()
            self.client_sockets.append(client_socket)
            print(f"Client {client_address} connected.")

        # After two clients are connected, exchange their public keys and start handling them
        if len(self.client_sockets) == 2:
            self.exchange_keys()
            for client_socket in self.client_sockets:
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
                client_thread.start()

    def handle_client(self, client_socket):
        other_client_socket = next((cs for cs in self.client_sockets if cs is not client_socket), None)
        while True:
            try:
                # Receive encrypted message from the client
                encrypted_message = client_socket.recv(ENCRYPTED_MESSAGE_SIZE).decode()
                print(f"Received message from {client_socket.getpeername()}: {encrypted_message}")
                if not encrypted_message:
                    print('Empty message received.')
                    continue

                # Send the encrypted message to the other client
                other_client_socket.send(encrypted_message.encode())
            except Exception as e:
                print(f"An error occurred: {e}")
                self.client_sockets.remove(client_socket)
                client_socket.close()
                break

    def exchange_keys(self):
        client1_socket, client2_socket = self.client_sockets

        # Receive public key from client 1
        client1_public_key = client1_socket.recv(ENCRYPTED_MESSAGE_SIZE).decode()
        # Receive public key from client 2
        client2_public_key = client2_socket.recv(ENCRYPTED_MESSAGE_SIZE).decode()

        # Send client 2's public key to client 1
        client1_socket.send(client2_public_key.encode())
        # Send client 1's public key to client 2
        client2_socket.send(client1_public_key.encode())

        print('Public keys exchanged between clients.')


if __name__ == '__main__':
    server = Server(CLIENT_HOST, SERVER_PORT, LIMIT_LISTEN)
    server.start()
