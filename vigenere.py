
def extend_key(text, key):
    """
    розширення ключа для відповідності довжині тексту (пропуск неалфавітних символів)
    """
    # key = key.upper()
    extended_key = []
    key_index = 0
    for char in text:
        if char.isalpha():  # Ключ використовується лише для алфавітних символів
            extended_key.append(key[key_index % len(key)])
            key_index += 1
        else:
            extended_key.append(char)  # Залишаємо пробіли та інші символи без змін
    return ''.join(extended_key)


def vigenere_encrypt(text, key):
    """
    шифрування тексту за допомогою шифру Віженера (всі букви у верхньому регістрі)
    """
    text = ''.join(filter(str.isalpha, text.upper()))

    key = extend_key(text, key)  # розширення ключа
    cipher_text = []
    for i in range(len(text)):
        if text[i].isalpha():
            shift = ord(key[i]) - ord('A')
            encrypted_char = chr((ord(text[i]) - ord('A') + shift) % 26 + ord('A'))
            cipher_text.append(encrypted_char)
        else:
            cipher_text.append(text[i])  # Не шифруємо неалфавітні символи
    return ''.join(cipher_text)

def vigenere_decrypt(cipher_text, key):
    """
    дешифрування тексту, зашифрованого шифром Віженера (всі букви у верхньому регістрі)
    """
    key = extend_key(cipher_text, key)  # розширення ключа
    original_text = []
    for i in range(len(cipher_text)):
        if cipher_text[i].isalpha():
            shift = ord(key[i]) - ord('A')
            decrypted_char = chr((ord(cipher_text[i]) - ord('A') - shift + 26) % 26 + ord('A'))
            original_text.append(decrypted_char)
        else:
            original_text.append(cipher_text[i])  # Не дешифруємо неалфавітні символи
    return ''.join(original_text)

# Використання
text = """The artist is the creator of beautiful things. To reveal art and conceal the artist is art's aim. The critic is he who can 
translate into another manner or a new material his impression of beautiful things. The highest, as the lowest, form of criticism is 
a mode of autobiography. Those who find ugly meanings in beautiful things are corrupt without being charming. This is a fault. Those 
who find beautiful meanings in beautiful things are the cultivated. For these there is hope. They are the elect to whom beautiful 
things mean only Beauty. There is no such thing as a moral or an immoral book. Books are well written, or badly written. That is all. 
The nineteenth-century dislike of realism is the rage of Caliban seeing his own face in a glass. The nineteenth-century dislike of 
Romanticism is the rage of Caliban not seeing his own face in a glass. The moral life of man forms part of the subject matter of the 
artist, but the morality of art consists in the perfect use of an imperfect medium. No artist desires to prove anything. Even things 
that are true can be proved. No artist has ethical sympathies. An ethical sympathy in an artist is an unpardonable mannerism of style. 
No artist is ever morbid. The artist can express everything. Thought and language are to the artist instruments of an art. Vice and 
virtue are to the artist materials for an art. From the point of view of form, the type of all the arts is the art of the musician. 
From the point of view of feeling, the actor's craft is the type. All art is at once surface and symbol. Those who go beneath the 
surface do so at their peril. Those who read the symbol do so at their peril. It is the spectator, and not life, that art really 
mirrors. Diversity of opinion about a work of art shows that the work is new, complex, vital. When critics disagree the artist is in 
accord with himself. We can forgive a man for making a useful thing as long as he does not admire it. The only excuse for making a 
useless thing is that one admires it intensely. All art is quite useless.
"""
key = "CRYPTOGRAPHY"

# Шифрування тексту
encrypted_text = vigenere_encrypt(text, key)
print(f"Зашифрований текст: {encrypted_text}")

# Дешифрування тексту
decrypted_text = vigenere_decrypt(encrypted_text, key)
print(f"Розшифрований текст: {decrypted_text}")
