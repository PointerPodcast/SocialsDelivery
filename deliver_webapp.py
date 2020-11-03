#!/usr/bin/env python

import sys
import json
import glob
import sched
import base64
import os.path
import shutil
import logging
from datetime import date
import time as time_module
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
from PPSocials.PPtelegram import PP_telegram


logging.basicConfig(filename='socialDelivery.log', filemode='a', format='%(name)s - %(asctime)s - %(levelname)s - %(message)s')

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
    'telegram' : PP_telegram
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
            raise Exception("Twitter post exceeds maximum length")
        if n_chars >= MAX_POST_CHARS:
            print("Linkedin/Facebook/Instagram/Telegram post exceeds maximum length ("+str(n_chars - MAX_POST_CHARS)+")")
            raise Exception("Linkedin/Facebook/Instagram post exceeds maximum length")
    print(" >> "+social+" Post length is OK!")


def _mentions_remapper(mentions, post_facebook_linkedin_instagram, post_twitter):
    socialToPost = {}
    for social in socialToClass.keys():
        if social == 'twitter':
            socialToPost[social] = post_twitter
        else:
            socialToPost[social] = post_facebook_linkedin_instagram
    mentions_dict = json.loads(mentions)
    print(mentions_dict)
    for guestId in mentions_dict.keys():
        print(guestId)
        userToSocial = {}
        real_name = mentions_dict[guestId]['real_name']
        userToSocial['facebook'] = mentions_dict[guestId]['facebook']
        userToSocial['instagram'] = mentions_dict[guestId]['instagram']
        userToSocial['twitter'] = mentions_dict[guestId]['twitter']
        userToSocial['linkedin'] = mentions_dict[guestId]['linkedin']
        userToSocial['telegram'] = mentions_dict[guestId]['telegram']
        for social in socialToPost.keys():
            if(userToSocial[social] == '#'):
                continue
            socialToPost[social] = socialToPost[social].replace(real_name, '@'+userToSocial[social]) 
    return socialToPost
        


def posts_creation(episode_dir, episode_number, episode_name, post_facebook_linkedin_instagram, post_twitter, mentions):
    socialToPost = _mentions_remapper(mentions, post_facebook_linkedin_instagram, post_twitter)
    for social in socialToClass.keys():
        post_file_data = episode_dir / 'post' / (social+".txt")
        if social == "instagram" or social == "twitter":
            post_file_data.write_text('Pointer['+episode_number+'] '+episode_name+' \n'+pointing_hand_short_code+pointing_hand_short_code+'[LINK in BIO]\n')
            with open(post_file_data, 'a+', encoding='utf-8') as file:
                file.write('\n'+socialToPost[social]+'\n')
        else:
            post_file_data.write_text('Pointer['+episode_number+'] '+episode_name+'\n')
            with open(post_file_data, 'a+', encoding='utf-8') as file:
                file.write('\n'+socialToPost[social]+'\n')
            _append_podcasting_platforms_link(episode_dir, social, post_file_data) #Appending only to facebook, linkedin and twitter
        _check_max_chars_post(social, post_file_data)



def generate_cover(episode_dir, episode_number, episode_name, cover_file):
    print("\n" + bcolors.HEADER + " Autogenerating Cover..." + bcolors.ENDC )
    logging.info("Autogenerating Cover Episode: "+episode_number)
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
    img.save(cover_file)
    return cover_file



def access_tokens(password):
    print(bcolors.OKGREEN + "\n Access tokens found:" + bcolors.ENDC)
    tokens = {}
    dir_access_tokens = Path(ACCESS_TOKEN_PATH)
    for file_access_tokens in dir_access_tokens.iterdir():
        social = file_access_tokens.stem
        print("  - "+social)
        tokens[social] = crypto_utility.decrypt_file(file_access_tokens.resolve(), password)
    return tokens

def get_cover_of_episode(episode_number):
    matches = glob.glob(EPISODES_PATH + "/" + episode_number + "/cover_"+episode_number+'.*')
    print(matches[0])
    with open(matches[0], "rb") as image:
        f = image.read()
        data = bytearray(f)
    return data 


def delete_episode(episode_number):
    try:
        episode_delete = Path(EPISODES_PATH + "/" +episode_number)
        shutil.rmtree(episode_delete)
    except Exception as err:
        logging.error(err)
        return False, err
    print("Removed Episode: "+episode_number)
    logging.info("Removed Episode: "+episode_number)
    return True, 'OK'


def authenticate(password):
    logging.info('Authenticating...')
    try:
        access_tokens(password)
    except Exception:
        logging.error('Failed auth!')
        return False, 'Failed auth'
    return True, 'OK'


#prima genera cover
def publish(episode_number, episode_dir,  cover_file, social_instances):
    print(bcolors.OKGREEN + "Posting..." + bcolors.ENDC)
    logging.info("Posting Episode "+episode_number)
    for social in social_instances.keys():
        post_file_data = episode_dir / 'post' / (social+".txt")
        post_text = post_file_data.read_text()
        social_instances[social].publish_post(post_text, cover_file)


def deploy_episode(episode_number,
                   episode_name,
                   post_facebook_linkedin_instagram,
                   post_twitter, password, guests_number,
                   mentions=None,
                   custom_cover_data=None,
                   custom_cover_name=None,
                   time=None,
                   date=None):

    if not episode_number or not episode_number or not post_facebook_linkedin_instagram or not post_twitter or not password:
        print("A value is empty")
        logging.warning("A values is empty")
        return False

    episode_dir = Path(EPISODES_PATH+'/'+episode_number+'/')

    try:
        if generate_structure_episode(episode_dir, episode_number):
            print("Already present episode: "+episode_number)
            logging.error("Already present episode: "+episode_number)
            return False

        #Create posts
        posts_creation(episode_dir, episode_number, episode_name, post_facebook_linkedin_instagram, post_twitter, mentions)

        #if not custom_cover_path:
        cover_file = None
        if custom_cover_name is None: #No custom_cover has been uploaded. Thus Autogenerate it
            cover_file = str(Path(EPISODES_PATH+'/'+episode_number+'/cover_'+episode_number+'.jpg').resolve())
            generate_cover(episode_dir, episode_number, episode_name, cover_file)
        else:
            extension = custom_cover_name.split('.')[1]
            cover_file = str(Path(EPISODES_PATH+'/'+episode_number+'/cover_'+episode_number+'.'+extension).resolve())
            f = open(cover_file, 'wb')
            f.write(bytearray(custom_cover_data))
            f.close()

        if(cover_file is None):
            return False

        tokens = access_tokens(password)
        social_instances = {}

        print("\n" + bcolors.HEADER + " Veryfing tokens..." + bcolors.ENDC )
        for social in socialToClass.keys():
            instance = socialToClass[social](tokens[social])
            social_instances[social] = instance

        tokens = {}

        '''

        scheduler = sched.scheduler(time_module.time, time_module.sleep)
        t = time_module.strptime(date+' '+time, '%d-%m-%Y %H:%M')
        t = time_module.mktime(t)

        scheduler.enterabs(t,
                             1,
                             publish,
                             argument = (episode_number,
                                         episode_dir,
                                         cover_file,
                                         social_instances
                                         )
         )

        scheduler.run()
        logging.info("Episode Scheduled on: "+date+' '+time)
        '''

        publish(episode_number, episode_dir, cover_file, social_instances)

    except Exception as err:
        print("Some exception has occurred. ", err)
        logging.error("Some exception has occurred. "+ str(err))
        return False

    return True

