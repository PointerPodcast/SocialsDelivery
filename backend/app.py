#!/usr/bin/env python

import os
import json
import sched
import time as time_module
import numpy as np
from PIL import Image
from datetime import date
from threading import Thread
from config_file import IP, PORT

from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS, cross_origin
from deliver_webapp import deploy_episode
from deliver_webapp import authenticate
from deliver_webapp import delete_episode
from deliver_webapp import get_cover_of_episode

app = Flask(__name__)
CORS(app)

#TODO: avoid to pass psw in clear

@app.route('/')
def index():
    return "Welcome!"


@app.route('/socialdelivery/api/v1.0/deleteepisode', methods=['POST'])
def delete_episode_by_number():
    episode_number = request.json['episode_number']
    password = request.json['password']
    res, status = authenticate(password)
    if res : 
        res, status = delete_episode(episode_number)
    message = {
        'result' : res,
        'status' : status,
    }
    response = jsonify({'message':message})

    if res == True:
        return response, 200
    else:
        return response, 400


@app.route('/socialdelivery/api/v1.0/getcover/<episode_number>', methods=['GET'])
def get_cover(episode_number):
    print("Get Cover")
    _, data = get_cover_of_episode(episode_number)
    return data

@app.route('/socialdelivery/api/v1.0/authenticate', methods=['POST'])
def auth():
    password = request.json['password'] 
    res, status = authenticate(password)
    message = {
        'result' : res,
        'status' : status,
    }
    response = jsonify({'message':message})
    if res == True:
        return response, 200
    else:
        return response, 400
    pass

@app.route('/socialdelivery/api/v1.0/deliverepisode', methods=['POST'])
def deliver_episode():
    episode_number = request.json['episode_number']
    episode_name = request.json['title']
    post_facebook_linkedin_instagram = request.json['fli_post']
    post_twitter = request.json['twitter_post']
    guests_number = request.json['guests_number'] #vedere di rimuoverlo
    mentions = request.json['guests']
    password = request.json['password'] 
    date = request.json['date']
    time = request.json['time']
    custom_cover_data = request.json.get('custom_cover_data', None)
    custom_cover_name = request.json.get('custom_cover_name', None)

    res, status = deploy_episode(episode_number,
                         episode_name,
                         post_facebook_linkedin_instagram,
                         post_twitter,
                         password,
                         guests_number,
                         mentions,
                         custom_cover_data,
                         custom_cover_name,
                         time,
                         date
                         )

    episode = {
        'result' : res,
        'status' : status
    }
    response = jsonify({'message':episode})
    if res == True:
        return response, 200
    else:
        return response, 400



if __name__ == '__main__':
    app.run(host=IP, port=PORT)

