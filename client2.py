import socket
import threading

import custom_rsa
from constants import *


class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.public_key, self.private_key = custom_rsa.key_generation()
        self.server_socket = socket.socket()

    def start(self):
        self.server_socket.connect((self.host, self.port))
        print(f'Connected to {self.host}:{self.port}')

        # Send own public key to the server
        self.server_socket.send(str(self.public_key).encode())

        # Receive the other client's public key from the server
        other_public_key = self.receive_public_key()
        print(f'Received other client public key: {other_public_key}')

        # Proceed with communication using the received public key
        self.communicate(other_public_key)

    def receive_public_key(self):
        other_public_key = self.server_socket.recv(ENCRYPTED_MESSAGE_SIZE).decode()
        other_public_key = tuple(map(int, other_public_key.strip(ROUND_BRACKETS).split(COMMA)))
        return other_public_key

    def communicate(self, other_public_key):
        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.start()

        send_thread = threading.Thread(target=self.send_messages, args=(other_public_key,))
        send_thread.start()

        receive_thread.join()
        send_thread.join()

    def send_messages(self, other_public_key):
        try:
            while True:
                message = input('Enter a message: ')
                if message.lower() == EXIT_MESSAGE:
                    break
                elif not message:
                    print('Message cannot be empty.')
                    continue

                encrypted_message = custom_rsa.encrypt(message, other_public_key)
                self.server_socket.send(str(encrypted_message).encode())
                print("\033[93m\033[1A\033[2KMessage sent to the other client...\033[0m")
        except (KeyboardInterrupt, ConnectionResetError):
            print('Connection closed.')
        finally:
            self.server_socket.close()

    def receive_messages(self):
        while True:
            try:
                encrypted_reply = self.server_socket.recv(ENCRYPTED_MESSAGE_SIZE).decode()
                if not encrypted_reply:
                    print('Empty reply received.')
                    continue

                encrypted_reply = list(map(int, encrypted_reply.strip(SQUARE_BRACKETS).split(COMMA)))
                reply = custom_rsa.decrypt(encrypted_reply, self.private_key)

                # Save the current cursor position
                print("\033[s", end='')

                # Move the cursor up one line, clear the line, and print the received message
                print("\033[1A\033[2K\033[94mReceived: {}\033[0m".format(reply))

                # Restore the cursor position and reprint the input prompt
                print("\033[uEnter a message: ", end='', flush=True)
            except (KeyboardInterrupt, ConnectionResetError):
                print('Connection closed.')
                break


if __name__ == '__main__':
    client = Client(SERVER_HOST, SERVER_PORT)
    client.start()
