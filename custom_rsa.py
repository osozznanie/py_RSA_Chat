import random
import math


def is_prime(num):
    """Проверяет, является ли число простым."""
    if num <= 1:
        return False
    if num == 2:
        return True
    if num % 2 == 0:
        return False

    # Проверяем делители до квадратного корня из числа
    i = 3
    while i <= math.isqrt(num):
        if num % i == 0:
            return False
        i += 2
    return True


def generate_prime(min_val=0, max_val=100):
    """Генерирует случайное простое число в заданном диапазоне."""
    num = 0
    while not is_prime(num):
        num = random.randint(min_val, max_val)
    return num


def gcd(x, y):
    """Находит наибольший общий делитель двух чисел."""
    while y:
        x, y = y, x % y
    return x


def key_generation():
    """Генерирует открытый и закрытый ключи RSA."""
    # Генерация двух простых чисел p и q
    p = generate_prime()
    q = generate_prime()
    n = p * q  # Общий модуль

    # Вычисление функции Эйлера
    phi = (p - 1) * (q - 1)

    # Выбор открытой экспоненты e
    e = random.randint(1, phi)
    g = gcd(e, phi)

    # Проверка взаимной простоты e и phi
    while g != 1:
        e = random.randint(1, phi)
        g = gcd(e, phi)

    # Вычисление закрытой экспоненты d
    d = pow(e, -1, phi)
    return (e, n), (d, n)


def encrypt(message, public_key):
    """Шифрует сообщение с использованием открытого ключа."""
    key, n = public_key
    # Преобразование каждого символа сообщения в его шифрованное представление
    encrypted = [pow(ord(char), key, n) for char in message]
    return encrypted


def decrypt(ciphertext, private_key):
    """Дешифрует сообщение с использованием закрытого ключа."""
    key, n = private_key
    # Восстановление оригинальных символов из зашифрованных данных
    decrypted = ''.join([chr(pow(char, key, n)) for char in ciphertext])
    return decrypted


if __name__ == '__main__':
    # Генерация ключей
    public_key, private_key = key_generation()
    print(f'Открытый ключ: {public_key}')
    print(f'Закрытый ключ: {private_key}')

    # Ввод сообщения от пользователя
    message = input('Введите сообщение: ')

    # Шифрование сообщения
    encrypted_message = encrypt(message, public_key)
    print('Зашифрованное сообщение:', encrypted_message)

    # Дешифрование сообщения
    decrypted_message = decrypt(encrypted_message, private_key)
    print('Расшифрованное сообщение:', decrypted_message)
