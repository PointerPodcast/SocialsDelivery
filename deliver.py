import base64

from PPfacebook import PP_facebook

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

def get_key(password):
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(password)
    return base64.urlsafe_b64encode(digest.finalize())

def decrypt_file(password, file_name):
    fernet = Fernet(get_key(password.encode('utf-8')))
    f = open(file_name, 'rb')
    encrypted_token = f.read()
    f.close()
    d = fernet.decrypt(encrypted_token)
    return d.decode()

def main():
    password = None
    try: 
        password = input("Enter Decryption Password: ")
    except EOFError:
        print("EOFError")

    PP_facebook_token = decrypt_file(password, "./access_tokens/Facebook_token.enc")
    pp_facebook = PP_facebook(PP_facebook_token)
    pp_facebook.get_message('836872193518697')


main()
    



