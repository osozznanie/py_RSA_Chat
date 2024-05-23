import pickle
import socket
import rsa
from constants import *


def main():
    public_key, private_key = rsa.generate_key_pair_for_encrypt()
    print(f"Client's public key: {public_key}")

    with socket.socket() as client_socket:
        client_socket.connect((SERVER_HOST, SERVER_PORT))

        print(f"Sent client name: {CLIENT_NAME}")

        public_key_str = str(public_key)
        public_key_bytes = public_key_str.encode()
        client_socket.send(public_key_bytes)
        print(f"Sent client public key: {public_key_bytes}")

        server_name = SERVER_NAME
        print(f"Received server name: {server_name}")

        server_public_key = client_socket.recv(512)
        public_key_str = server_public_key.decode()
        public_key = tuple(map(int, public_key_str.strip('()').split(',')))
        print(f"Received server public key: {public_key}")

        print(f'Connected to {server_name}.')

        try:
            while True:
                message = input('Enter a message: ')
                if message.lower() == EXIT_MESSAGE:
                    break

                encrypted_message = rsa.encrypt_msg(message, server_public_key)
                encrypted_message_bytes = pickle.dumps(encrypted_message)  # Convert the list to bytes
                client_socket.send(encrypted_message_bytes)
                print('Encrypted message:', ''.join(map(lambda x: str(x), encrypted_message)))

                encrypted_reply_bytes = client_socket.recv(ENCRYPTED_MESSAGE_SIZE)
                encrypted_reply = pickle.loads(encrypted_reply_bytes)  # Convert the bytes back to a list
                reply = rsa.decrypt_msg(encrypted_reply, private_key)
                print(f"Received encrypted reply: {encrypted_reply}")
                print(f"Decrypted reply: {reply}")

        except (KeyboardInterrupt, ConnectionResetError):
            print('Connection closed.')


if __name__ == '__main__':
    main()
