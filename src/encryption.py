def caesar_decrypt(text, shift):
    decrypted_text = ""
    for char in text:
        decrypted_char = chr((ord(char) - shift) % 128)
        decrypted_text += decrypted_char
    return decrypted_text

# check https://dashboard.stripe.com/products/prod_NjneJRpeYKWVDR
#^GOX)?9=9
#^GOX)9769
#^GOX);879
#^GOX)=;87
#^GOX)98<?