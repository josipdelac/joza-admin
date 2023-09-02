import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

"""
# Funkcija za generiranje ključa i spremanje u varijable okruženja
def generate_and_save_encryption_key():
    encryption_key = get_random_bytes(32)  # Generiranje 256-bitnog ključa za AES-256
    encrypted_key = encryption_key.hex()
    
    # Spremi ključ u varijablu okruženja
    os.environ["ENCRYPTION_KEY"] = encrypted_key

# Generiraj i spremi ključ u varijable okruženja
generate_and_save_encryption_key()
print("Encryption key generated and saved to environment variable.")
"""


# Dohvati šifrirani ključ iz varijable okruženja
encrypted_key_hex = os.environ["ENCRYPTION_KEY"]
encryption_key = bytes.fromhex(encrypted_key_hex)


if encryption_key is None:
    print("Šifrirani ključ nije postavljen. Postavite ENCRYPTION_KEY varijablu okruženja.")
else:
    print("Šifrirani ključ uspješno učitan.")
    print(encryption_key)
    
# Kriptiranje
cipher = AES.new(encryption_key, AES.MODE_EAX)
plaintext = b"Hello, world!"
ciphertext, tag = cipher.encrypt_and_digest(plaintext)

# Dekriptiranje
cipher = AES.new(encryption_key, AES.MODE_EAX, nonce=cipher.nonce)
decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)

print("Kriptirani tekst je:",ciphertext)
print("Original:", plaintext)
print("Decrypted:", decrypted_data.decode())