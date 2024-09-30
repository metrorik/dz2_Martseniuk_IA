import math
from vigenere import text


def create_key_order(key):
    """
    Створює порядковий номер для кожної букви ключа на основі алфавітного порядку.
    Якщо буква повторюється, їй присвоюється порядковий номер згідно з її порядком появи в ключі.
    """
    key = key.upper()
    key_letters = list(key)
    
    # Створюємо список кортежів (буква, оригінальний індекс)
    sorted_letters = sorted([(letter, index) for index, letter in enumerate(key_letters)], key=lambda x: (x[0], x[1]))
    
    order = {}
    for i, (letter, original_index) in enumerate(sorted_letters, 1):
        # Якщо буква вже є в словнику, додаємо до списку порядкових номерів
        if letter in order:
            order[letter].append(i)
        else:
            order[letter] = [i]
    
    key_order = []
    letter_count = {}
    for letter in key_letters:
        if letter in letter_count:
            letter_count[letter] += 1
        else:
            letter_count[letter] = 1
        # Присвоюємо порядковий номер згідно з порядком появи
        key_order.append(order[letter][letter_count[letter]-1])
    return key_order

def encrypt_single_transposition(plaintext, key):
    """
    Шифрує текст за допомогою одного шифру перестановки на основі ключа.
    """
    key_order = create_key_order(key)
    key_length = len(key)
    
    # Видаляємо пробіли та переводимо текст у верхній регістр
    plaintext = plaintext.replace(" ", "").upper()
    
    # Додаємо заповнювачі 'X', якщо необхідно
    num_padding = key_length - (len(plaintext) % key_length)
    if num_padding != key_length:
        plaintext += 'X' * num_padding
    
    # Розбиваємо текст на блоки
    blocks = [plaintext[i:i + key_length] for i in range(0, len(plaintext), key_length)]
    
    # Створюємо матрицю з цих блоків
    matrix = [list(block) for block in blocks]
    
    # Отримуємо порядок сортування стовпців на основі ключа
    sorted_key_order = sorted(range(len(key_order)), key=lambda k: key_order[k])
    
    # Переставляємо стовпці згідно з порядковими номерами ключа
    ciphertext = ''
    for col in sorted_key_order:
        for row in matrix:
            ciphertext += row[col]
    
    return ciphertext

def decrypt_single_transposition(ciphertext, key):
    """
    Дешифрує текст за допомогою одного шифру перестановки на основі ключа.
    """
    key_order = create_key_order(key)
    key_length = len(key)
    
    # Обчислюємо кількість рядків у матриці
    num_rows = math.ceil(len(ciphertext) / key_length)
    
    # Отримуємо порядок сортування стовпців на основі ключа
    sorted_key_order = sorted(range(len(key_order)), key=lambda k: key_order[k])
    
    # Ініціалізуємо порожню матрицю
    matrix = [''] * num_rows
    
    # Розподіляємо шифротекст по стовпцях згідно з порядком ключа
    start = 0
    columns = {}
    for sorted_index, original_col in enumerate(sorted_key_order):
        # Визначаємо кінцевий індекс для поточного стовпця
        end = start + num_rows
        columns[original_col] = ciphertext[start:end]
        start = end
    
    # Відновлюємо матрицю, читаючи символи по рядках
    decrypted_text = ''
    for row in range(num_rows):
        for col in range(key_length):
            if row < len(columns[col]):
                decrypted_text += columns[col][row]
    
    # Видаляємо заповнювачі 'X'
    decrypted_text = decrypted_text.rstrip('X')
    
    return decrypted_text

def encrypt_double_transposition(plaintext, key1, key2):
    """
    Шифрує текст за допомогою подвійної перестановки на основі двох ключів.
    """
    # Перший шифр перестановки
    first_encryption = encrypt_single_transposition(plaintext, key1)
    # Другий шифр перестановки
    second_encryption = encrypt_single_transposition(first_encryption, key2)
    return second_encryption

def decrypt_double_transposition(ciphertext, key1, key2):
    """
    Дешифрує текст за допомогою подвійної перестановки на основі двох ключів.
    """
    # Перший дешифр перестановки (зворотній до другого шифрування)
    first_decryption = decrypt_single_transposition(ciphertext, key2)
    # Другий дешифр перестановки (зворотній до першого шифрування)
    second_decryption = decrypt_single_transposition(first_decryption, key1)
    return second_decryption

# Приклад використання
if __name__ == "__main__":
    key1 = "SECRET"
    key2 = "CRYPTO"
    plaintext = text
    
    print(f"текст: {plaintext}")
    
    # Шифрування подвійною перестановкою
    encrypted = encrypt_double_transposition(plaintext, key1, key2)
    print(f"Зашифрований текст: {encrypted}")
    
    # Дешифрування подвійною перестановкою
    decrypted = decrypt_double_transposition(encrypted, key1, key2)
    print(f"Розшифрований текст: {decrypted}")
