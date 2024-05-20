import socket
import rsa
from constants import *


def main():
    (public_key, private_key) = rsa.newkeys(PUBLIC_KEY_SIZE)

    with socket.socket() as client_socket:
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        client_socket.send(CLIENT_NAME.encode())

        client_public_key_pem = public_key.save_pkcs1().decode()
        client_socket.send(client_public_key_pem.encode())

        server_name = client_socket.recv(ENCRYPTED_MESSAGE_SIZE).decode()
        server_public_key_pem_bytes = client_socket.recv(ENCRYPTED_MESSAGE_SIZE)
        server_public_key_pem = server_public_key_pem_bytes.decode()
        server_public_key = rsa.PublicKey.load_pkcs1(server_public_key_pem.encode())

        print(f'Connected to {server_name}.')

        try:
            while True:
                message = input('Enter a message: ')
                if message.lower() == EXIT_MESSAGE:
                    break

                encrypted_message = rsa.encrypt(message.encode(), server_public_key)
                client_socket.send(encrypted_message)

                encrypted_reply = client_socket.recv(ENCRYPTED_MESSAGE_SIZE)
                reply = rsa.decrypt(encrypted_reply, private_key).decode()
                print(f'{server_name}: {reply}')
        except (KeyboardInterrupt, ConnectionResetError):
            print('Connection closed.')


if __name__ == '__main__':
    main()
