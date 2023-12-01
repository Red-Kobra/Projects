import base64
import hashlib
import secrets
from cryptography.fernet import Fernet

def generate_key(password, salt):
    hashed = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    key = base64.urlsafe_b64encode(hashed)
    return key

def encrypt(input_file, key):
    f = Fernet(key)
    with open(input_file, 'rb') as file:
        file_data = file.read()
        encrypted = f.encrypt(file_data)
    with open(input_file + '.encrypted', 'wb') as file:
        file.write(encrypted)

def decrypt(input_file, key):
    f = Fernet(key)
    with open(input_file, 'rb') as file:
        encrypted = file.read()
        decrypted = f.decrypt(encrypted)
    with open(input_file + '.decrypted', 'wb') as file:
        file.write(decrypted)

# Esempio di utilizzo
password = "123456"
salt = secrets.token_bytes(16)
key = generate_key(password, salt)

encrypt('file.txt', key)
decrypt('file.txt.encrypted', key)