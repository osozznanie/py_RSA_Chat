import socket
import custom_rsa
from constants import *


class Server:
    def __init__(self, host, port, limit_listen):
        self.host = host
        self.port = port
        self.limit_listen = limit_listen
        self.public_key, self.private_key = custom_rsa.key_generation()
        self.client_public_key = None
        self.client_socket = None
        self.server_socket = socket.socket()

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(self.limit_listen)
        print(f'Server is listening on {self.host}:{self.port}...')

        self.client_socket, client_address = self.server_socket.accept()
        print(f'Connection from {client_address} has been established.')

        self.client_socket.send(str(self.public_key).encode())

        self.client_public_key = self.receive_public_key()
        client_name = CLIENT_NAME
        print(f'Client name: {client_name}')

        self.communicate(client_name)

    def receive_public_key(self):
        client_public_key = self.client_socket.recv(ENCRYPTED_MESSAGE_SIZE).decode()
        client_public_key = tuple(map(int, client_public_key.strip(ROUND_BRACKETS).split(COMMA)))
        print(f'Received client public key: {client_public_key}')
        return client_public_key

    def communicate(self, client_name):
        try:
            while True:
                message = input('Enter a message: ')
                if message.lower() == EXIT_MESSAGE:
                    break
                elif not message or message == '':
                    print('Message cannot be empty.')
                    continue

                encrypted_message = custom_rsa.encrypt(message, self.client_public_key)
                self.client_socket.send(str(encrypted_message).encode())
                print("\033[93mMessage sent to the client...\033[0m")

                encrypted_reply = self.client_socket.recv(ENCRYPTED_MESSAGE_SIZE).decode()
                encrypted_reply = list(map(int, encrypted_reply.strip(SQUARE_BRACKETS).split(COMMA)))
                reply = custom_rsa.decrypt(encrypted_reply, self.private_key)
                print(f'{client_name}: {reply}')
        except (KeyboardInterrupt, ConnectionResetError):
            print('Connection closed.')
        finally:
            self.client_socket.close()


if __name__ == '__main__':
    server = Server(SERVER_HOST, SERVER_PORT, LIMIT_LISTEN)
    server.start()
