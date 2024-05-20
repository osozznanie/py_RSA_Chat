import socket
import threading
import rsa

def handle_client(client_socket, client_address, client_public_key):
    while True:
        try:
            encrypted_message = client_socket.recv(1024)
            message = rsa.decrypt(encrypted_message, private_key).decode()

            if message:
                print(f'{client_address}: {message}')
                if message.lower() == 'exit':
                    break
                reply = input('Enter a reply: ')
                encrypted_reply = rsa.encrypt(reply.encode(), client_public_key)
                client_socket.send(encrypted_reply)
            else:
                break
        except Exception as e:
            print(f"Error handling client {client_address}: {e}")
            break
    client_socket.close()
    print(f"Connection with {client_address} closed.")

(public_key, private_key) = rsa.newkeys(512)

server_socket = socket.socket()
server_socket.bind(('localhost', 5153))
server_socket.listen(5)

print('Server is listening...')

while True:
    client_socket, client_address = server_socket.accept()

    client_name = client_socket.recv(1024).decode()

    client_public_key_pem_bytes = client_socket.recv(1024)
    client_public_key_pem = client_public_key_pem_bytes.decode()
    client_public_key = rsa.PublicKey.load_pkcs1(client_public_key_pem.encode())

    print(f'{client_name} has connected from {client_address}.')

    client_socket.send('Server'.encode())
    client_socket.send(public_key.save_pkcs1())

    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address, client_public_key))
    client_thread.start()