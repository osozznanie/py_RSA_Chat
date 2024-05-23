import socket
import custom_rsa
from constants import *

def main():
    # Генерация ключей RSA
    public_key, private_key = custom_rsa.key_generation()

    with socket.socket() as server_socket:
        server_socket.bind((SERVER_HOST, SERVER_PORT))
        server_socket.listen(LIMIT_LISTEN)
        print('Server is listening...')

        client_socket, client_address = server_socket.accept()
        print(f'Connected to {client_address}.')

        # Отправка открытого ключа клиенту
        client_socket.send(str(public_key).encode())
        print('Public key:', public_key)

        # Получение имени клиента
        client_name = CLIENT_NAME
        print(f'Client name: {client_name}')

        # Получение открытого ключа клиента
        client_public_key = client_socket.recv(1024).decode()
        client_public_key = tuple(map(int, client_public_key.strip('()').split(', ')))
        print("Received client public key:", client_public_key)

        try:
            while True:
                message = input('Enter a message: ')
                print("\033[93mWaiting for the client to receive the reply...\033[0m")

                if message.lower() == EXIT_MESSAGE:
                    break

                # Шифрование и отправка сообщения клиенту
                encrypted_message = custom_rsa.encrypt(message, client_public_key)
                client_socket.send(str(encrypted_message).encode())

                # Получение и расшифровка ответа от клиента
                encrypted_reply = client_socket.recv(1024).decode()
                encrypted_reply = list(map(int, encrypted_reply.strip('[]').split(', ')))
                reply = custom_rsa.decrypt(encrypted_reply, private_key)
                print(f'{client_name}: {reply}')
        except (KeyboardInterrupt, ConnectionResetError):
            print('Connection closed.')

if __name__ == '__main__':
    main()
