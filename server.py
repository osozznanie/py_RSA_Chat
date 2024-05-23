import pickle
import socket
import threading

import rsa
from constants import *


class Server:
    def __init__(self):
        self.rsa = rsa
        self.public_key, self.private_key = self.rsa.generate_key_pair_for_encrypt()
        print(f"Server's public key: {self.public_key}")

    def handle_client(self, client_socket, client_address, client_public_key):
        try:
            while True:
                encrypted_message = client_socket.recv(ENCRYPTED_MESSAGE_SIZE)
                if not encrypted_message:
                    break

                decrypted_message = self.rsa.decrypt_msg(encrypted_message, self.private_key)
                print(f'{client_address}: {decrypted_message}')

                if decrypted_message.lower() == EXIT_MESSAGE:
                    break

                reply = input('Enter a reply: ')
                encrypted_reply = self.rsa.encrypt_msg(reply.encode(), client_public_key)
                client_socket.send(encrypted_reply)
        except Exception as e:
            print(f"Error handling client {client_address}: {e}")
        finally:
            client_socket.close()
            print(f"Connection with {client_address} closed.")

    def start(self):
        with socket.socket() as server_socket:
            server_socket.bind((SERVER_HOST, SERVER_PORT))
            server_socket.listen(LIMIT_LISTEN)
            print('Server is listening...')

            while True:
                client_socket, client_address = server_socket.accept()

                client_name = CLIENT_NAME
                print(f"Received client name: {client_name}")

                client_public_key = client_socket.recv(512)
                public_key_str = client_public_key.decode()
                public_key = tuple(map(int, public_key_str.strip('()').split(',')))
                print(f"Received client public key: {public_key}")

                print(f'{client_name} has connected from {client_address}.')

                public_key_str = str(public_key)
                public_key_bytes = public_key_str.encode()
                client_socket.send(public_key_bytes)
                print(f"Sent server public key: {public_key_bytes}")

                client_thread = threading.Thread(target=self.handle_client,
                                                 args=(client_socket, client_address, client_public_key))
                client_thread.start()


if __name__ == '__main__':
    server = Server()
    server.start()
