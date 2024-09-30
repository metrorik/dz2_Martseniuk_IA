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

def encrypt_table_cipher(text, key):
    """
    Шифрує текст за допомогою табличного шифру на основі ключа.
    """
    key_order = create_key_order(key)
    key_length = len(key)
    
    # Видаляємо пробіли та переводимо текст у верхній регістр
    plaintext = text.replace(" ", "").upper()
    
    # Додаємо заповнювачі 'X', якщо необхідно
    num_padding = key_length - (len(plaintext) % key_length)
    if num_padding != key_length:
        plaintext += 'X' * num_padding
    
    # Розбиваємо текст на блоки
    blocks = [plaintext[i:i + key_length] for i in range(0, len(plaintext), key_length)]
    
    # Створюємо матрицю з цих блоків
    matrix = [list(block) for block in blocks]
    
    # Створюємо словник, де ключ - порядковий номер, значення - список символів стовпця
    columns = {}
    for index, order in enumerate(key_order):
        if order not in columns:
            columns[order] = []
        for row in matrix:
            columns[order].append(row[index])
    
    # Переставляємо стовпці за порядком номерів ключа та формуємо шифротекст
    ciphertext = ''
    for order in sorted(columns):
        ciphertext += ''.join(columns[order])
    
    return ciphertext

def decrypt_table_cipher(ciphertext, key):
    """
    Дешифрує текст за допомогою табличного шифру на основі ключа.
    """
    key_order = create_key_order(key)
    key_length = len(key)
    num_rows = math.ceil(len(ciphertext) / key_length)
    
    # Створюємо словник для зберігання стовпців
    columns = {}
    sorted_key_order = sorted([(order, index) for index, order in enumerate(key_order)], key=lambda x: (x[0], x[1]))
    
    # Визначаємо кількість символів у кожному стовпці
    total_chars = len(ciphertext)
    col_lengths = [num_rows] * key_length
    # Якщо текст не заповнює матрицю повністю, останні стовпці можуть бути коротшими
    num_full_cols = total_chars % key_length
    if num_full_cols != 0:
        for i in range(key_length - num_full_cols):
            col_lengths[key_length - 1 - i] -= 1
    
    # Розподіляємо шифротекст по стовпцях згідно з порядком ключа
    start = 0
    for order, index in sorted_key_order:
        length = col_lengths[index]
        columns[index] = list(ciphertext[start:start + length])
        start += length
    
    # Відновлюємо матрицю, читаючи символи по рядках
    matrix = []
    for row in range(num_rows):
        current_row = []
        for col in range(key_length):
            if row < len(columns[col]):
                current_row.append(columns[col][row])
            else:
                current_row.append('')  # Якщо стовпець коротший, додаємо порожній символ
        matrix.append(current_row)
    
    # Збираємо розшифрований текст
    decrypted_text = ''.join([''.join(row) for row in matrix])
    
    # Видаляємо заповнювачі 'X'
    decrypted_text = decrypted_text.rstrip('X')
    
    return decrypted_text

# Приклад використання
if __name__ == "__main__":
    key = "MATRIX"
    
    print(f"текст: {text}")
    
    # Шифрування
    encrypted = encrypt_table_cipher(text, key)
    print(f"Зашифрований текст: {encrypted}")
    
    # Дешифрування
    decrypted = decrypt_table_cipher(encrypted, key)
    print(f"Розшифрований текст: {decrypted}")
