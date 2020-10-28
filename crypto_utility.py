import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import json


def get_key(password):
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(password)
    return base64.urlsafe_b64encode(digest.finalize())

def encrypt_and_store():
    password = None
    token = None
    file_name = None

    try: 
        password = input("Enter Encryption Password: ")
        token = input("What to encrypt: ").encode()
        file_name = input("Where to store: ")
    except EOFError:
        print("EOFError")

    fernet = Fernet(get_key(password.encode('utf-8')))
    encrypted = fernet.encrypt(token)

    #Store to file
    f = open(file_name, 'wb')
    f.write(encrypted)
    f.close



def decrypt_file(file_name, password):
    fernet = Fernet(get_key(password.encode('utf-8')))

    f = open(file_name, 'rb')
    encrypted_token = f.read()
    f.close()

    decrypted = fernet.decrypt(encrypted_token)
    return decrypted.decode()

if __name__ == '__main__':
    encrypt_and_store()
