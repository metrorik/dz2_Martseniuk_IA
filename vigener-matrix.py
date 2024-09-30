import math
from vigenere import text


# Функція для шифрування за допомогою шифру Віженера
def vigenere_encrypt(plaintext, key):
    """
    шифрування тексту за допомогою шифру Віженера
    """
    key = key.upper()
    plaintext = ''.join([c.upper() for c in plaintext if c.isalpha()])  # Видалення неалфавітних символів
    ciphertext = ''
    key_index = 0
    for char in plaintext:
        if char.isalpha():
            shift = ord(key[key_index % len(key)]) - ord('A')
            encrypted_char = chr(((ord(char) - ord('A') + shift) % 26) + ord('A'))
            ciphertext += encrypted_char
            key_index += 1
    return ciphertext

# Функція для шифрування табличним шифром
def columnar_transposition_encrypt(plaintext, key):
    """
    шифрування тексту за допомогою табличного шифру з ключем
    """
    key_length = len(key)
    key_order = sorted(list(key))

    # Додавання заповнювачів, щоб текст можна було розділити на стовпці
    num_rows = math.ceil(len(plaintext) / key_length)
    padded_text = plaintext.ljust(num_rows * key_length, 'X')  # Додаємо 'X' як заповнювач

    # Створення таблиці
    table = [padded_text[i:i + key_length] for i in range(0, len(padded_text), key_length)]

    # Зашифрований текст буде братися по стовпцях в порядку ключа
    ciphertext = ''
    key_mapping = {key_order[i]: i for i in range(len(key_order))}
    for col in sorted(key_mapping):
        col_index = key_mapping[col]
        for row in table:
            ciphertext += row[col_index]
    
    return ciphertext

# Функція для дешифрування табличного шифру
def columnar_transposition_decrypt(ciphertext, key):
    """
    дешифрування тексту, зашифрованого табличним шифром
    """
    key_length = len(key)
    key_order = sorted(list(key))
    num_rows = math.ceil(len(ciphertext) / key_length)
    
    # Створення таблиці для дешифрування
    table = [''] * key_length
    index = 0
    key_mapping = {key_order[i]: i for i in range(len(key_order))}
    
    for col in sorted(key_mapping):
        col_index = key_mapping[col]
        table[col_index] = ciphertext[index:index + num_rows]
        index += num_rows

    # Відновлення рядків
    plaintext = ''
    for row in range(num_rows):
        for col in range(key_length):
            if row < len(table[col]):
                plaintext += table[col][row]
    
    return plaintext.rstrip('X')  # Видалення заповнювачів

# Функція для дешифрування шифру Віженера
def vigenere_decrypt(ciphertext, key):
    """
    дешифрування тексту, зашифрованого шифром Віженера
    """
    key = key.upper()
    ciphertext = ciphertext.upper()
    plaintext = ''
    key_index = 0
    for char in ciphertext:
        if char.isalpha():
            shift = ord(key[key_index % len(key)]) - ord('A')
            decrypted_char = chr(((ord(char) - ord('A') - shift) % 26) + ord('A'))
            plaintext += decrypted_char
            key_index += 1
    return plaintext

# Основна функція для шифрування і дешифрування
def main():
    # Текст для шифрування
    plaintext = text

    # Перший ключ для шифру Віженера
    key = "CRYPTO"

    print(f"Відкритий текст:\n{plaintext}\n")

    # Шифрування за допомогою шифру Віженера
    vigenere_ciphertext = vigenere_encrypt(plaintext, key)
    print(f"Зашифрований текст (Віженер):\n{vigenere_ciphertext}\n")

    # Шифрування за допомогою табличного шифру
    final_ciphertext = columnar_transposition_encrypt(vigenere_ciphertext, key)
    print(f"Зашифрований текст (Табличний шифр після Віженера):\n{final_ciphertext}\n")

    # Дешифрування табличного шифру
    decrypted_columnar_text = columnar_transposition_decrypt(final_ciphertext, key)
    print(f"Текст після дешифрування табличного шифру:\n{decrypted_columnar_text}\n")

    # Дешифрування шифру Віженера
    final_plaintext = vigenere_decrypt(decrypted_columnar_text, key)
    print(f"Розшифрований текст після двох шифрів:\n{final_plaintext}\n")

if __name__ == "__main__":
    main()
