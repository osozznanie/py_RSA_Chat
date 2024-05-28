import socket
import threading
import sys

import custom_rsa
from constants import *


class Client:
    def __init__(self, host, port):
        # Этот метод инициализирует клиента с помощью хоста и порта сервера, генерирует пару открытого и закрытого ключей,
        # создает сокет и устанавливает статус соединения в True.
        self.host = host
        self.port = port
        self.public_key, self.private_key = custom_rsa.key_generation()
        self.server_socket = socket.socket()
        self.connected = True

    def start(self):
        # Этот метод запускает клиент, подключается к серверу, отправляет открытый ключ на сервер,
        # получает открытый ключ другого клиента и начинает связь.
        try:
            self.server_socket.connect((self.host, self.port))
            print(f'Connected to {self.host}:{self.port}')

            self.server_socket.send(str(self.public_key).encode())

            other_public_key = self.receive_public_key()
            print(f'Received other client public key: {other_public_key}')

            self.communicate(other_public_key)
        except ConnectionResetError:
            print("Connection to the server was lost.")
        finally:
            self.server_socket.close()
            self.connected = False
            sys.exit(0)

    def receive_public_key(self):
        # Этот метод получает открытый ключ другого клиента с сервера.
        other_public_key = self.server_socket.recv(ENCRYPTED_MESSAGE_SIZE).decode()
        other_public_key = tuple(map(int, other_public_key.strip(ROUND_BRACKETS).split(COMMA)))
        return other_public_key

    def communicate(self, other_public_key):
        # Этот метод запускает два потока: один для получения сообщений, другой для отправки сообщений.
        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.start()

        send_thread = threading.Thread(target=self.send_messages, args=(other_public_key,))
        send_thread.start()

        receive_thread.join()
        send_thread.join()

    def send_messages(self, other_public_key):
        # Этот метод позволяет клиенту отправлять сообщения другому клиенту.
        # Сообщения шифруются открытым ключом другого клиента.
        try:
            while self.connected:
                message = input('Enter a message: ')
                if not self.connected:
                    break
                if message.lower() == EXIT_MESSAGE:
                    break
                elif not message:
                    print('Message cannot be empty.')
                    continue

                encrypted_message = custom_rsa.encrypt(message, other_public_key)
                self.server_socket.send(str(encrypted_message).encode())
        except (KeyboardInterrupt, ConnectionResetError):
            print('Connection closed.')
        finally:
            self.server_socket.close()
            self.connected = False
            sys.exit(0)

    def receive_messages(self):
        # Этот метод позволяет клиенту получать сообщения от другого клиента.
        # Сообщения расшифровываются с помощью закрытого ключа клиента.
        try:
            while self.connected:
                encrypted_reply = self.server_socket.recv(ENCRYPTED_MESSAGE_SIZE).decode()
                if not encrypted_reply:
                    print('Server has closed the connection.')
                    sys.exit(0)

                encrypted_reply = list(map(int, encrypted_reply.strip(SQUARE_BRACKETS).split(COMMA)))
                reply = custom_rsa.decrypt(encrypted_reply, self.private_key)

                print("\033", end='', flush=True)
                print("\r", end='', flush=True)

                print(f"Received: {reply}")
                print("Enter a message: ", end='', flush=True)
        except (KeyboardInterrupt, ConnectionResetError):
            print('Connection closed.')
        finally:
            self.server_socket.close()
            self.connected = False
            sys.exit(0)


if __name__ == '__main__':
    # Это точка входа в программу. Он создает клиента и запускает его.
    client = Client(SERVER_HOST, SERVER_PORT)
    client.start()