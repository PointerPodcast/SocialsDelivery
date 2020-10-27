import base64
import crypto_utility
from PPfacebook import PP_facebook


def main():
    PP_facebook_token = crypto_utility.decrypt_file("./access_tokens/Facebook_token.enc")
    pp_facebook = PP_facebook(PP_facebook_token)
    pp_facebook.get_message('836872193518697')


main() 
