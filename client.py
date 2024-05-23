import socket
import custom_rsa
from constants import *


class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.public_key, self.private_key = custom_rsa.key_generation()
        self.server_public_key = None
        self.client_socket = socket.socket()

    def start(self):
        self.client_socket.connect((self.host, self.port))
        print(f'Connected to {self.host}:{self.port}...')

        self.server_public_key = self.receive_public_key()
        print(f'Received server public key: {self.server_public_key}')

        self.client_socket.send(str(self.public_key).encode())

        server_name = SERVER_NAME
        print(f'Server name: {server_name}')

        self.communicate(server_name)

    def receive_public_key(self):
        server_public_key = self.client_socket.recv(ENCRYPTED_MESSAGE_SIZE).decode()
        server_public_key = tuple(map(int, server_public_key.strip(ROUND_BRACKETS).split(COMMA)))
        return server_public_key

    def communicate(self, server_name):
        try:
            while True:
                encrypted_message = self.client_socket.recv(ENCRYPTED_MESSAGE_SIZE).decode()
                encrypted_message = list(map(int, encrypted_message.strip(SQUARE_BRACKETS).split(COMMA)))
                print(encrypted_message)
                message = custom_rsa.decrypt(encrypted_message, self.private_key)
                print(f'{server_name}: {message}')

                reply = input('Enter a message: ')
                if reply.lower() == EXIT_MESSAGE:
                    break

                encrypted_reply = custom_rsa.encrypt(reply, self.server_public_key)
                self.client_socket.send(str(encrypted_reply).encode())
                print("\033[93mReply sent to the server...\033[0m")
        except (KeyboardInterrupt, ConnectionResetError):
            print('Connection closed.')
        finally:
            self.client_socket.close()


if __name__ == '__main__':
    client = Client(SERVER_HOST, SERVER_PORT)
    client.start()
