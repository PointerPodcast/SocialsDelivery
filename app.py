#!/usr/bin/env python

import sched
from threading import Thread
from datetime import date
import time as time_module

from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS, cross_origin
from deliver_webapp import deploy_episode
from deliver_webapp import authenticate
from deliver_webapp import delete_episode

app = Flask(__name__)
CORS(app)

#TODO: avoid to pass psw in clear

@app.route('/', methods=['GET'])
def index():
    return "Hello, SocialDelivery!"


@app.route('/socialdelivery/api/v1.0/deleteepisode', methods=['PUT'])
def delete_episode_by_number():
    episode_number = request.json['episode_number']
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

@app.route('/socialdelivery/api/v1.0/getcover', methods=['GET'])
def get_cover():
    episode_number = request.args.get('episode_number')
    print(episode_number)
    return episode_number

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
    #custom_cover_path = request.json['custom_cover']
    print(request.json)

    '''
    #schedule job
    scheduler = sched.scheduler(time_module.time, time_module.sleep)
    t = time_module.strptime(date+' '+time, '%d-%m-%Y %H:%M')
    t = time_module.mktime(t)
    deploy_episode(episode_number,
                         episode_name,
                         post_facebook_linkedin_instagram,
                         post_twitter,
                         password,
                         guests_number,
                         mentions)

    scheduler_e = scheduler.enterabs(t,
                                     1,
                                     deploy_episode,
                                     argument = (episode_number,
                                         episode_name,
                                         post_facebook_linkedin_instagram,
                                         post_twitter,
                                         password,
                                         guests_number,
                                         mentions)
                                     )

    scheduler_e.run()
    print("Scheduled")
    return 200
'''
    res = deploy_episode(episode_number,
                         episode_name,
                         post_facebook_linkedin_instagram,
                         post_twitter,
                         password,
                         guests_number,
                         mentions)

    episode = {
        'episode_number' : episode_number,
        'title' : episode_name,
        'result' : res
    }
    response = jsonify({'response':episode})
    if res == True:
        return response, 200
    else:
        return response, 400



if __name__ == '__main__':
    app.run(debug=True, port=5000)

