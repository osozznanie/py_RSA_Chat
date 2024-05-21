import socket
import threading
import rsa
from constants import *


def handle_client(client_socket, client_address, client_public_key):
    try:
        while True:
            encrypted_message = client_socket.recv(ENCRYPTED_MESSAGE_SIZE)
            if not encrypted_message:
                break

            decrypted_message = rsa.decrypt_msg(encrypted_message, private_key)
            print(f'{client_address}: {decrypted_message}')

            if decrypted_message.lower() == EXIT_MESSAGE:
                break

            reply = input('Enter a reply: ')
            encrypted_reply = rsa.encrypt_msg(reply.encode(), client_public_key)
            client_socket.send(encrypted_reply)
    except Exception as e:
        print(f"Error handling client {client_address}: {e}")
    finally:
        client_socket.close()
        print(f"Connection with {client_address} closed.")


def main():
    global private_key, public_key

    public_key, private_key = rsa.generate_key_pair_for_encrypt()
    print(f"Server's public key: {public_key}")

    with socket.socket() as server_socket:
        server_socket.bind((SERVER_HOST, SERVER_PORT))
        server_socket.listen(LIMIT_LISTEN)
        print('Server is listening...')

        while True:
            client_socket, client_address = server_socket.accept()

            client_name = CLIENT_NAME
            print(f"Received client name: {client_name}")

            client_public_key_pem_bytes = client_socket.recv(ENCRYPTED_MESSAGE_SIZE)
            client_public_key = rsa.load_public_key(client_public_key_pem_bytes)
            print(f"Received client public key: {client_public_key}")

            print(f'{client_name} has connected from {client_address}.')

            client_socket.send(rsa.convert_public_key_to_string(public_key).ljust(512).encode())

            client_thread = threading.Thread(target=handle_client,
                                             args=(client_socket, client_address, client_public_key))
            client_thread.start()


if __name__ == '__main__':
    main()
