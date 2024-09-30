from vigenere import vigenere_decrypt, encrypted_text  
from collections import Counter

# Функція для обчислення коефіцієнта збігу (Index of Coincidence, IC)
def calculate_ic(text):
    n = len(text)
    frequencies = Counter(text)
    ic = sum(f * (f - 1) for f in frequencies.values()) / (n * (n - 1))
    return ic

# Функція для оцінки довжини ключа за методом Фрідмана
def friedman_estimate_key_length(ciphertext):
    expected_ic_random = 1 / 26
    expected_ic_english = 0.068

    ic = calculate_ic(ciphertext)

    # Оцінка довжини ключа
    key_length = (expected_ic_english - expected_ic_random) / (ic - expected_ic_random)
    return round(key_length)

# Функція для частотного аналізу і відновлення кількох варіантів ключа
def recover_key(ciphertext, estimated_key_length):
    """
    Відновлення ключа на основі частотного аналізу для кожної групи літер
    """
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    most_common_english_letter = 'E'  # Найпоширеніша літера в англійській мові

    # Зберігатиме відновлений ключ
    recovered_key = []

    # Розбиваємо текст на групи залежно від довжини ключа
    for i in range(estimated_key_length):
        group = ciphertext[i::estimated_key_length]
        
        # Обчислюємо частоти символів у групі
        frequencies = Counter(group)
        most_common_char = frequencies.most_common(1)[0][0]  # Найпоширеніший символ у цій групі
        
        # Розраховуємо зсув, враховуючи, що найпоширенішою літерою є 'E'
        shift = (ord(most_common_char) - ord(most_common_english_letter)) % 26
        recovered_key.append(alphabet[shift])

    return ''.join(recovered_key)


# Застосування методу Фрідмана
def main():
    filtered_ciphertext = encrypted_text

    # Оцінка довжини ключа за методом Фрідмана
    estimated_key_length = friedman_estimate_key_length(filtered_ciphertext)
    print(f"Оцінена довжина ключа: {estimated_key_length}")

    # Відновлення ключа
    recovered_key = recover_key(filtered_ciphertext, estimated_key_length)
    print(f"Відновлений ключ: {recovered_key}")

    # Дешифрування тексту з відновленим ключем
    decrypted_text = vigenere_decrypt(encrypted_text, recovered_key)
    print("Розшифрований текст:")
    print(decrypted_text)

if __name__ == "__main__":
    main()
