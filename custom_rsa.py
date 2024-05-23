import random
import math

# Проверяет, является ли число простым
def is_prime(num):
    if num <= 1:
        return False
    if num == 2:
        return True
    if num % 2 == 0:
        return False

    i = 3
    while i <= math.isqrt(num):
        if num % i == 0:
            return False
        i += 2
    return True


# Генерирует случайное простое число в заданном диапазоне
def generate_prime_in_range(min_val=1000, max_val=5000):
    num = 0
    while not is_prime(num):
        num = random.randint(min_val, max_val)
    return num


# Находит наибольший общий делитель двух чисел
def greatest_common_divisor(x, y):
    while y:
        x, y = y, x % y
    return x


# Генерация ключей
def key_generation():
    prime_a = generate_prime_in_range()
    prime_b = generate_prime_in_range()
    general_module = prime_a * prime_b

    # Вычисление функции Эйлера
    phi = (prime_a - 1) * (prime_b - 1)

    # Выбор открытой экспоненты e
    open_exhibitor = random.randint(1, phi)
    gcd = greatest_common_divisor(open_exhibitor, phi)

    # Проверка взаимной простоты e и phi
    while gcd != 1:
        open_exhibitor = random.randint(1, phi)
        gcd = greatest_common_divisor(open_exhibitor, phi)

    # Вычисление закрытой экспоненты close_exhibitor
    close_exhibitor = pow(open_exhibitor, -1, phi)

    return (open_exhibitor, general_module), (close_exhibitor, general_module)


# Шифрование
def encrypt(message, public_key):
    key, prime_num = public_key
    # Преобразование символов в числа и шифрование
    encrypted = [pow(ord(char), key, prime_num) for char in message]
    return encrypted


# Дешифрование
def decrypt(ciphertext, private_key):
    key, n = private_key
    decrypted = ''.join([chr(pow(char, key, n)) for char in ciphertext])
    return decrypted

def main():
    public_key, private_key = key_generation()
    print(f'Public key: {public_key}')
    print(f'Private key: {private_key}')
    input_message = input('Enter a message: ')

    encrypted_message = encrypt(input_message, public_key)
    print(f'Encrypted message: {encrypted_message}')

    decrypted_message = decrypt(encrypted_message, private_key)
    print(f'Decrypted message: {decrypted_message}')


if __name__ == '__main__':
    main()



