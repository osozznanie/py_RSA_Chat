import random
import math


def is_number_prime(checked_num):
    if checked_num == 2:
        return True
    if checked_num < 2 or checked_num % 2 == 0:
        return False
    for i in range(3, int(math.sqrt(checked_num)) + 1, 2):
        if checked_num % i == 0:
            return False
    return True


def generate_prime_number(start=1, end=100):
    while True:
        checked_num = random.randint(start, end)
        if is_number_prime(checked_num):
            return checked_num


def greatest_common_divisor(a, b):
    while b:
        a, b = b, a % b
    return a


def generate_key_pair_for_encrypt():
    first_num = generate_prime_number(100, 200)
    second_num = generate_prime_number(100, 200)
    checked_num = first_num * second_num
    phi = (first_num - 1) * (second_num - 1)

    while True:
        open_exhibitor = random.randrange(1, phi)
        if greatest_common_divisor(open_exhibitor, phi) == 1:
            break

    closed_exhibitor = pow(open_exhibitor, -1, phi)
    return (open_exhibitor, checked_num), (closed_exhibitor, checked_num)


def encrypt_msg(message, public_key):
    key, n = public_key
    return [pow(ord(char), key, n) for char in message]


def decrypt_msg(encrypted_message, private_key):
    closed_exhibitor, checked_num = private_key
    decrypted_message = bytearray()
    for encrypted_char in encrypted_message:
        decrypted_char = pow(encrypted_char, closed_exhibitor, checked_num)
        decrypted_message.append(decrypted_char)
    return bytes(decrypted_message)
