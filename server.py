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

            message = rsa.decrypt(encrypted_message, private_key).decode()
            print(f'{client_address}: {message}')

            if message.lower() == EXIT_MESSAGE:
                break

            reply = input('Enter a reply: ')
            encrypted_reply = rsa.encrypt(reply.encode(), client_public_key)
            client_socket.send(encrypted_reply)
    except Exception as e:
        print(f"Error handling client {client_address}: {e}")
    finally:
        client_socket.close()
        print(f"Connection with {client_address} closed.")

def main():
    global private_key

    (public_key, private_key) = rsa.newkeys(PUBLIC_KEY_SIZE)

    with socket.socket() as server_socket:
        server_socket.bind((SERVER_HOST, SERVER_PORT))
        server_socket.listen(LIMIT_LISTEN)

        print('Server is listening...')

        while True:
            client_socket, client_address = server_socket.accept()

            client_name = client_socket.recv(ENCRYPTED_MESSAGE_SIZE).decode()

            client_public_key_pem_bytes = client_socket.recv(ENCRYPTED_MESSAGE_SIZE)
            client_public_key_pem = client_public_key_pem_bytes.decode()
            client_public_key = rsa.PublicKey.load_pkcs1(client_public_key_pem.encode())

            print(f'{client_name} has connected from {client_address}.')

            client_socket.send(SERVER_NAME.encode())
            client_socket.send(public_key.save_pkcs1())

            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address, client_public_key))
            client_thread.start()

if __name__ == '__main__':
    main()