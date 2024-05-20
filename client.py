import socket
import threading
import sys
import rsa

def receive_messages(socket_server, server_name, private_key):
    while True:
        try:
            encrypted_message = socket_server.recv(1024)
            message = rsa.decrypt(encrypted_message, private_key).decode()

            if message:
                # Clear the input line
                sys.stdout.write('\r' + ' ' * (len(input_prompt) + len(current_input)) + '\r')
                sys.stdout.flush()

                print(f'{server_name}: {message}')

                # Reprint the input prompt
                sys.stdout.write(input_prompt + current_input)
                sys.stdout.flush()
            else:
                break
        except Exception as e:
            print(f"Error receiving message: {e}")
            break
    socket_server.close()
    print(f"Connection with {server_name} closed.")

def send_messages(socket_server, server_public_key):
    global current_input
    while True:
        try:
            message = input(input_prompt)
            current_input = ''
            if message:
                encrypted_message = rsa.encrypt(message.encode(), server_public_key)
                socket_server.send(encrypted_message)
            else:
                break
        except Exception as e:
            print(f"Error sending message: {e}")
            break
    socket_server.close()

# Generate public and private keys for the client
(public_key, private_key) = rsa.newkeys(512)

socket_server = socket.socket()

name = input('Enter your name: ')
socket_server.connect(('localhost', 5152))  # Use the same port as server
socket_server.send(name.encode())
socket_server.send(public_key.save_pkcs1())

# Receive the server's name
server_name = socket_server.recv(1024).decode()

# Receive the server's public key in PEM format
server_public_key_pem_bytes = socket_server.recv(1024)
server_public_key_pem = server_public_key_pem_bytes.decode()
server_public_key = rsa.PublicKey.load_pkcs1(server_public_key_pem.encode())

print(f'{server_name} has connected.')


input_prompt = 'You: '
current_input = ''

receive_thread = threading.Thread(target=receive_messages, args=(socket_server, server_name, private_key))
send_thread = threading.Thread(target=send_messages, args=(socket_server, server_public_key))

receive_thread.start()
send_thread.start()

receive_thread.join()
send_thread.join()
print("Client has stopped.")