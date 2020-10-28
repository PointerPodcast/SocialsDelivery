#!/usr/bin/env python

import base64
import os.path
from pathlib import Path
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 

#Custom_module
import crypto_utility
from PPfacebook import PP_facebook
from PPinstagram import PP_instagram


#TODO:
# is_access_token_valid --> try_catch
# tag remapper


MAX_POST_CHARS = 700 #lower_bound linkedin
MAX_POST_CHARS_TWITTER = 280


ACCESS_TOKEN_PATH = './access_tokens/'

EPISODES_PATH = './episodes'

COVER_TEMPLATES_PATH = './cover_templates/'

content_types = ['post', 'story']

#Fb, linkedin and instragram posts share the "same" post description
socials_post = ['facebook_linkedin', 'instagram', 'twitter']

story_post = ['instagram', 'linkedin']

dict_podcasting_platforms_links = {
    'Spotify': 'https://open.spotify.com/show/3XmDzcZv4rCIx1VpWrbrkh', #Spotify
    'ApplePodcast' : 'https://podcasts.apple.com/it/podcast/pointerpodcast/id1465505870', #ApplePodcast
}

post_font = '/usr/share/fonts/ubuntu/UbuntuMono-BI.ttf'
pointing_hand_short_code = '👉'

def generate_structure_episode(episode_number, cover_file):
    episode_dir = Path(EPISODES_PATH+'/'+episode_number+'/')
    exist = episode_dir.is_dir()
    if not exist:
        episode_name = input("Insert Episode Title: ")
        episode_dir.mkdir(parents=True)
        dict_paths = {}
        for content in content_types:
            dict_paths[content] = episode_dir / content
            dict_paths[content].mkdir()

        generate_cover(episode_number, episode_name, cover_file)

        for social in socials_post:
            post_file_data = dict_paths['post'] / (social+".txt")
            post_file_data.touch()
            if social == "instagram":
                post_file_data.write_text('Pointer['+episode_number+'] '+episode_name+' \n'+pointing_hand_short_code+pointing_hand_short_code+'[LINK in BIO]\n')
            else:
                post_file_data.write_text('Pointer['+episode_number+'] '+episode_name+'\n')
    return exist
     

def check_custom_cover(episode_number, cover_file):
    yes = {'yes','y', 'ye', ''}
    no = {'no','n'}
    custom_cover_choice = input("Custom Cover? [Y/n]: ").lower()
    print(custom_cover_choice)
    if custom_cover_choice in no:
        print("Autogenerating Cover...")
    elif custom_cover_choice in yes:
        input("\n > Place your custom cover in: "+cover_file+". Place it then press [ENTER]")
        if not cover_file.is_file():
            print("File not found. Exiting")
            exit()
    else:
        print("invalid response. Exiting")
        exit()

def generate_cover(episode_number, episode_name, cover_file):
    template_cover_file = Path(COVER_TEMPLATES_PATH+'cover_template.jpg')

    check_custom_cover(episode_number, cover_file)

    img = Image.open(template_cover_file.resolve())
    width, height = img.size
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(post_font, 50) #font-file, font-size)
# draw.text((x, y),"Sample Text",(r,g,b))
    draw.text(
        (width / 2,  height / 2), #Coordinates
        "Pointer["+episode_number+"]\n"+episode_name, #Text
        (255,255,255), #Color RGB
        font=font,
        align="center")
    img.save(cover_file.resolve())


def check_max_chars_post(n_chars, social):
    if social == "twitter" and n_chars > MAX_POST_CHARS_TWITTER:
        print("Twitter post exceeds maximum length ("+str(n_chars - MAX_POST_CHARS_TWITTER)+")")
        exit()
    if n_chars >= MAX_POST_CHARS:
        print("Linkedin/Facebook/Instagram post exceeds maximum length ("+str(n_chars - MAX_POST_CHARS)+")")
        exit()
    print(" >> "+social+" Post length is OK!")

def access_tokens():
    tokens = {}
    dir_access_tokens = Path(ACCESS_TOKEN_PATH)
    print("\n Access tokens found:")
    for file_access_tokens in dir_access_tokens.iterdir():
        social = file_access_tokens.stem
        print("  - "+social)
        tokens[social] = file_access_tokens
    return tokens


def append_podcasting_platforms_link(episode_number):
    episode_dir = Path(EPISODES_PATH+'/'+episode_number+'/')
    for social in socials_post:
        post_file_data = episode_dir / 'post' / (social+".txt")
        with open(post_file_data, 'a+', encoding='utf-8') as file:
            for key in dict_podcasting_platforms_links.keys(): 
                file.write('\n'+key+': '+dict_podcasting_platforms_links[key]+'\n')
            n_chars = len(file.read())
            check_max_chars_post(n_chars, social)

def main():
    episode_number = input("Episode °N: ")
    cover_file = Path(EPISODES_PATH+'/'+episode_number+'/cover_'+episode_number+'.jpg')
    if not generate_structure_episode(episode_number, cover_file):
        print("\n >> Folder structure generate for Episode N°: "+episode_number+"\n >> Fill files and rerun deliver.py specifiyng the same Episode N° "+episode_number+"\n")
        exit()
    print("\nAppending to post podcasting_platforms_link...")
    append_podcasting_platforms_link(episode_number)
    tokens = access_tokens()
    password = None
    try: 
        password = input("\nEnter Decryption Password: ")
    except EOFError:
        print("EOFError")
        exit()

    PP_facebook_token = crypto_utility.decrypt_file(tokens['facebook'].resolve(), password)
    print(PP_facebook_token)
    PP_instagram_token = crypto_utility.decrypt_file(tokens['instagram'].resolve(), password)
    print(PP_instagram_token)
    #pp_facebook = PP_facebook(PP_facebook_token)
    #pp_facebook.publish_post("ciao", cover_file.resolve())
    #pp_instagram = PP_instagram(PP_instagram_token)
    #pp_instagram.publish_post_and_story("ciao", str(cover_file.resolve()))

    #Pubblicare su Linkedin
    #Pubblicare su twitter
    
    #Storie su Instagram e Facebook


main() 
