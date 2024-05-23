import socket
import custom_rsa
from constants import *

def main():
    # Генерация ключей RSA
    public_key, private_key = custom_rsa.key_generation()

    with socket.socket() as client_socket:
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        print('Connected to the server.')

        # Получение открытого ключа сервера
        server_public_key = client_socket.recv(1024).decode()
        server_public_key = tuple(map(int, server_public_key.strip('()').split(', ')))
        print('Public key:', public_key)

        # Получение имени сервера
        server_name = SERVER_NAME
        print(f'Connected to server named: {server_name}')

        print('Received server public key:', server_public_key)

        # Отправка открытого ключа серверу
        client_socket.send(str(public_key).encode())

        try:
            while True:
                message = input('Enter a message: ')
                print("\033[93mWaiting for the server to receive the reply...\033[0m")

                if message.lower() == EXIT_MESSAGE:
                    break

                # Шифрование и отправка сообщения серверу
                encrypted_message = custom_rsa.encrypt(message, server_public_key)
                client_socket.send(str(encrypted_message).encode())

                # Получение и расшифровка ответа от сервера
                encrypted_reply = client_socket.recv(1024).decode()
                encrypted_reply = list(map(int, encrypted_reply.strip('[]').split(', ')))
                reply = custom_rsa.decrypt(encrypted_reply, private_key)
                print(f'{server_name}: {reply}')
        except (KeyboardInterrupt, ConnectionResetError):
            print('Connection closed.')

if __name__ == '__main__':
    main()
