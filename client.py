import socket
import rsa
from constants import *


def main():
    public_key, private_key = rsa.generate_key_pair_for_encrypt()
    print(f"Client's public key: {public_key}")

    with socket.socket() as client_socket:
        client_socket.connect((SERVER_HOST, SERVER_PORT))

        print(f"Sent client name: {CLIENT_NAME}")

        client_public_key_pem = rsa.convert_public_key_to_string(public_key)
        client_socket.send(client_public_key_pem.encode())
        print(f"Sent client public key: {client_public_key_pem}")

        server_name = SERVER_NAME
        print(f"Received server name: {server_name}")

        server_public_key_pem_bytes = client_socket.recv(512)
        server_public_key = rsa.load_public_key(server_public_key_pem_bytes)
        print(f"Received server public key: {server_public_key}")

        print(f'Connected to {server_name}.')

        try:
            while True:
                message = input('Enter a message: ')
                if message.lower() == EXIT_MESSAGE:
                    break

                encrypted_message = rsa.encrypt_msg(message.encode(), server_public_key)
                client_socket.send(encrypted_message)
                print(f"Sent encrypted message: {encrypted_message}")

                encrypted_reply = client_socket.recv(ENCRYPTED_MESSAGE_SIZE)
                reply = rsa.decrypt_msg(encrypted_reply, private_key)
                print(f"Received encrypted reply: {encrypted_reply}")
                print(f"Decrypted reply: {reply}")
        except (KeyboardInterrupt, ConnectionResetError):
            print('Connection closed.')


if __name__ == '__main__':
    main()
