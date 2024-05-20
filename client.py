import socket
import rsa

(public_key, private_key) = rsa.newkeys(512)

client_socket = socket.socket()
client_socket.connect(('localhost', 5153))

client_socket.send('Client'.encode())

client_public_key_pem = public_key.save_pkcs1().decode()
client_socket.send(client_public_key_pem.encode())

server_name = client_socket.recv(1024).decode()

server_public_key_pem_bytes = client_socket.recv(1024)
server_public_key_pem = server_public_key_pem_bytes.decode()
server_public_key = rsa.PublicKey.load_pkcs1(server_public_key_pem.encode())

print(f'Connected to {server_name}.')

while True:
    message = input('Enter a message: ')
    encrypted_message = rsa.encrypt(message.encode(), server_public_key)
    client_socket.send(encrypted_message)

    if message.lower() == 'exit':
        break

    encrypted_reply = client_socket.recv(1024)
    reply = rsa.decrypt(encrypted_reply, private_key).decode()
    print(f'{server_name}: {reply}')

client_socket.close()
