def caesar_decrypt(text, shift):
    decrypted_text = ""
    for char in text:
        decrypted_char = chr((ord(char) - shift) % 128)
        decrypted_text += decrypted_char
    return decrypted_text