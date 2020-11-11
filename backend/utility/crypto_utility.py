import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from pathlib import Path
import json


def get_key(password):
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(password)
    return base64.urlsafe_b64encode(digest.finalize())

def encrypt_and_store():
    access_tokens_dir = './../access_tokens/'
    Path(access_tokens_dir).mkdir(parents=True, exist_ok=True)
    password = None
    token = None
    social_name = None

    try: 
        password = input("Enter Encryption Password: ")
        token = input("What to encrypt: ").encode()
        social_name = input("Name of the social: ")
    except EOFError:
        print("EOFError")

    fernet = Fernet(get_key(password.encode('utf-8')))
    encrypted = fernet.encrypt(token)

    #Store to file
    f = open(access_tokens_dir+social_name+'.enc', 'wb')
    f.write(encrypted)
    f.close



def decrypt_file(file_name, password):
    fernet = Fernet(get_key(password.encode('utf-8')))

    f = open(file_name, 'rb')
    encrypted_token = f.read()
    f.close()

    try:
        decrypted = fernet.decrypt(encrypted_token)
    except Exception:
        print("Invalid Password.")
        raise Exception("Invalid Password. Retry")
    return decrypted.decode()

if __name__ == '__main__':
    encrypt_and_store()
