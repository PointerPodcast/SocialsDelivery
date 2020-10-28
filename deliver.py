#!/usr/bin/env python

import base64
import os.path
from pathlib import Path

#Custom_module
import crypto_utility
from PPfacebook import PP_facebook


ACCESS_TOKEN_PATH = './access_tokens/'

EPISODES_PATH = './Episodes'

content_types = ['post', 'story']

#Fb, linkedin and instragram posts share the "same" post description
socials_post = ['facebook_linkedin', 'instagram', 'twitter']

story_post = ['instagram', 'linkedin']

podcasting_platforms_link = {
    'Spotify': 'https://open.spotify.com/show/3XmDzcZv4rCIx1VpWrbrkh', #Spotify
    'ApplePodcast' : 'https://podcasts.apple.com/it/podcast/pointerpodcast/id1465505870', #ApplePodcast
}

pointing_hand_short_code = ':backhand_index_pointing_right_light_skin_tone:'

def generate_structure_episode(episode_number):
    episode_name = input("Insert Episode Title: ")
    episode_dir = Path(EPISODES_PATH+'/'+episode_number+'/')
    exist = episode_dir.is_dir()

    if not exist:
        episode_dir.mkdir(parents=True)
        dict_paths = {}
        for content in content_types:
            dict_paths[content] = episode_dir / content
            dict_paths[content].mkdir()

        for social in socials_post:
            post_file_data = dict_paths['post'] / (social+".txt")
            post_file_data.touch()
            if social == "instagram":
                post_file_data.write_text('Pointer['+episode_number+'] '+episode_name+' \n'+pointing_hand_short_code+pointing_hand_short_code+'[LINK in BIO]\n')
            else:
                post_file_data.write_text('Pointer['+episode_number+'] '+episode_name+'\n')
    return exist
     

def generate_cover():
    pass

def access_tokens():
    tokens = {}
    dir_access_tokens = Path(ACCESS_TOKEN_PATH)
    print("Access tokens found:")
    for file_access_tokens in dir_access_tokens.iterdir():
        social = file_access_tokens.stem
        print("  - "+social)
        tokens[social] = file_access_tokens
    return tokens

def main():
    episode_number = input("Episode °N: ")
    if not generate_structure_episode(episode_number):
        print("\n >>Folder structure generate for Episode N°: "+episode_number+".\n >>Fill files and rerun deliver.py specifiyng the same Episode N° ("+episode_number+")\n")
        exit()
    access_tokens()

    #PP_facebook_token = crypto_utility.decrypt_file("./access_tokens/Facebook_token.enc")
    #pp_facebook = PP_facebook(PP_facebook_token)
    #pp_facebook.get_message('836872193518697')


main() 
