#!/usr/bin/env python

import sys
import base64
import os.path
import shutil
from pathlib import Path
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 

#Custom_module
from utility import crypto_utility
from utility.colors_prints import bcolors
from PPSocials.PPfacebook import PP_facebook
from PPSocials.PPinstagram import PP_instagram
from PPSocials.PPtwitter import PP_twitter


#TODO:
# Telegram bot send image to saved message (o sul gruppo)
# Schedule deploy
# tag remapper


MAX_POST_CHARS = 700 #lower_bound linkedin
MAX_POST_CHARS_TWITTER = 280

ACCESS_TOKEN_PATH = './access_tokens'

EPISODES_PATH = './episodes'

COVER_TEMPLATES_PATH = './cover_templates'

content_types = ['post', 'story']

#Fb, linkedin and instragram posts share the "same" post description
#socials_post = ['facebook', 'linkedin', 'instagram', 'twitter']
#story_post = ['instagram', 'linkedin']

dict_podcasting_platforms_links = {
    'Spotify': 'https://open.spotify.com/show/3XmDzcZv4rCIx1VpWrbrkh', #Spotify
    'ApplePodcast' : 'https://podcasts.apple.com/it/podcast/pointerpodcast/id1465505870', #ApplePodcast
}

socialToClass = {
    'facebook' : PP_facebook,
    'instagram' : PP_instagram,
    'twitter' : PP_twitter,
}

post_font = '/usr/share/fonts/ubuntu/UbuntuMono-BI.ttf'
pointing_hand_short_code = '👉'

def generate_structure_episode(episode_dir, episode_number):
    exist = episode_dir.is_dir()
    if not exist:
        episode_dir.mkdir(parents=True)
        dict_paths = {}
        for content in content_types:
            dict_paths[content] = episode_dir / content
            dict_paths[content].mkdir()
        for social in socialToClass.keys():
            post_file_data = dict_paths['post'] / (social+".txt")
            post_file_data.touch()
    return exist
     

def _append_podcasting_platforms_link(episode_dir, social, post_file_data):
    print(bcolors.OKGREEN + "\nAppending to post podcasting_platforms_link..." + bcolors.ENDC)
    with open(post_file_data, 'a+', encoding='utf-8') as file:
        for key in dict_podcasting_platforms_links.keys(): 
            file.write('\n'+key+': '+dict_podcasting_platforms_links[key]+'\n')


def _check_max_chars_post(social, post_file_data):
    with open(post_file_data, 'r', encoding='utf-8') as file:
        n_chars = len(file.read())
        if social == "twitter" and n_chars > MAX_POST_CHARS_TWITTER:
            print("Twitter post exceeds maximum length ("+str(n_chars - MAX_POST_CHARS_TWITTER)+")")
            exit()
        if n_chars >= MAX_POST_CHARS:
            print("Linkedin/Facebook/Instagram post exceeds maximum length ("+str(n_chars - MAX_POST_CHARS)+")")
            exit()
    print(" >> "+social+" Post length is OK!")


#real_name,facebook,instagram,twitter,linkedin;* --> if not present = #
def _mentions_remapper(mentions, post_facebook_linkedin_instagram, post_twitter):
    socialToPost = {}
    for social in socialToClass.keys():
        if social == 'twitter':
            socialToPost[social] = post_twitter
        else:
            socialToPost[social] = post_facebook_linkedin_instagram
    users = mentions.split(";")
    for user in users:
        socials = user.split(",")
        userToSocial = {}
        real_name = socials[0]
        userToSocial['facebook'] = socials[1].strip()
        userToSocial['instagram'] = socials[2].strip()
        userToSocial['twitter'] = socials[3].strip()
        userToSocial['linkedin'] = socials[4].strip()
        for social in socialToPost.keys():
            if(userToSocial[social] == '#'):
                continue
            socialToPost[social] = socialToPost[social].replace(real_name, '@'+userToSocial[social]) 
    return socialToPost
        


def posts_creation(episode_dir, episode_number, episode_name, post_facebook_linkedin_instagram, post_twitter, mentions):
    socialToPost = _mentions_remapper(mentions, post_facebook_linkedin_instagram, post_twitter)
    for social in socialToClass.keys():
        post_file_data = episode_dir / 'post' / (social+".txt")
        if social == "instagram":
            post_file_data.write_text('Pointer['+episode_number+'] '+episode_name+' \n'+pointing_hand_short_code+pointing_hand_short_code+'[LINK in BIO]\n')
            with open(post_file_data, 'a+', encoding='utf-8') as file:
                file.write('\n'+socialToPost[social]+'\n')
        else:
            post_file_data.write_text('Pointer['+episode_number+'] '+episode_name+'\n')
            with open(post_file_data, 'a+', encoding='utf-8') as file:
                file.write('\n'+socialToPost[social]+'\n')
            if social != 'twitter':
                _append_podcasting_platforms_link(episode_dir, social, post_file_data) #Appending only to facebook, linkedin and twitter
        _check_max_chars_post(social, post_file_data)


def generate_cover(episode_dir, episode_number, episode_name, cover_file):
    print("\n" + bcolors.HEADER + " Autogenerating cover..." + bcolors.ENDC )
    template_cover_file = Path(COVER_TEMPLATES_PATH+'/cover_template.jpg')
    img = Image.open(template_cover_file.resolve())
    width, height = img.size
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(post_font, 50) #font-file, font-size)
    draw.text(
        (width / 2,  height / 2), #Coordinates
        "Pointer["+episode_number+"]\n"+episode_name, #Text
        (255,255,255), #Color RGB
        font=font,
        align="center")
    img.save(cover_file.resolve())


def access_tokens(password):
    print(bcolors.OKGREEN + "\n Access tokens found:" + bcolors.ENDC)
    tokens = {}
    dir_access_tokens = Path(ACCESS_TOKEN_PATH)
    for file_access_tokens in dir_access_tokens.iterdir():
        social = file_access_tokens.stem
        print("  - "+social)
        tokens[social] = crypto_utility.decrypt_file(file_access_tokens.resolve(), password)
    return tokens


def delete_episode(episode_number):
    episode_delete = Path(EPISODES_PATH + "/" +episode_number)
    shutil.rmtree(episode_delete)
    print("Removed Episode: "+episode_number)


#RETURN COVER IMAGE TO POST ON INSTAGRAM_STORIES
def main():
    episode_number = sys.argv[1].strip()
    episode_name = sys.argv[2].strip()
    post_facebook_linkedin_instagram_path = sys.argv[3].strip()
    post_twitter_path = sys.argv[4].strip()
    mentions_path = sys.argv[5].strip()
    password = sys.argv[6].strip()
    custom_cover_path = sys.argv[5]

    if not episode_number or not episode_number or not post_facebook_linkedin_instagram_path or not post_twitter_path or not password:
        print("A value is empty")
        exit()

    post_facebook_linkedin_instagram = Path(post_facebook_linkedin_instagram_path).read_text()
    post_twitter = Path(post_twitter_path).read_text()
    mentions = Path(mentions_path).read_text()

    episode_dir = Path(EPISODES_PATH+'/'+episode_number+'/')
    cover_file = episode_dir / str('cover_'+episode_number+'.jpg')

    if generate_structure_episode(episode_dir, episode_number):
        print("Already present episode: "+episode_number)
        exit()

    posts_creation(episode_dir, episode_number, episode_name, post_facebook_linkedin_instagram, post_twitter, mentions)

    #if not custom_cover_path:
    generate_cover(episode_dir, episode_number, episode_name, cover_file)

    tokens = access_tokens(password)
    social_instances = {}

    print("\n" + bcolors.HEADER + " Veryfing tokens..." + bcolors.ENDC )
    for social in socialToClass.keys():
        instance = socialToClass[social](tokens[social])
        social_instances[social] = instance

    tokens = {}

    print(bcolors.OKGREEN + "Posting..." + bcolors.ENDC)
    for social in social_instances.keys():
        post_file_data = episode_dir / 'post' / (social+".txt")
        post_text = post_file_data.read_text()
        social_instances[social].publish_post(post_text, str(cover_file.resolve()))


    
main() 
