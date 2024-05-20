import socket
import threading
import sys

import rsa


def receive_messages(conn, client_name):
    while True:
        try:
            message = conn.recv(1024).decode()
            if message:
                # Clear the input line
                sys.stdout.write('\r' + ' ' * (len(input_prompt) + len(current_input)) + '\r')
                sys.stdout.flush()

                print(f'{client_name}: {message}')

                # Reprint the input prompt
                sys.stdout.write(input_prompt + current_input)
                sys.stdout.flush()
            else:
                break
        except Exception as e:
            print(f"Error receiving message: {e}")
            break
    conn.close()
    print(f"Connection with {client_name} closed.")


def send_messages(conn):
    global current_input
    while True:
        try:
            message = input(input_prompt)
            current_input = ''
            if message:
                conn.send(message.encode())
            else:
                break
        except Exception as e:
            print(f"Error sending message: {e}")
            break
    conn.close()


# Generate public and private keys for the server
(public_key, private_key) = rsa.newkeys(512)

new_socket = socket.socket()
new_socket.bind(('127.0.0.1', 5152))  # Use an available port
new_socket.listen()

print('Waiting for connection...')
name = input('Enter your name: ')
conn, addr = new_socket.accept()

# Serialize and send the server's public key in PEM format
public_key_pem = public_key.save_pkcs1().decode()
conn.send(public_key_pem.encode())

conn.send(name.encode())

client_name = conn.recv(1024).decode()
print(f'{client_name} has connected.')

input_prompt = 'You: '
current_input = ''

receive_thread = threading.Thread(target=receive_messages, args=(conn, client_name))
send_thread = threading.Thread(target=send_messages, args=(conn,))

receive_thread.start()
send_thread.start()

receive_thread.join()
send_thread.join()
print("Server has stopped.")
