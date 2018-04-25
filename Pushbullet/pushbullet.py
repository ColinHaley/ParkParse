import os
import requests

API_ROOT="https://api.pushbullet.com/v2/"

for line in open('config.env'):
    if line[0] == '#':
        continue
    var = line.strip().split('=')
    if len(var) == 2:
        os.environ[var[0]] = var[1]

#/endpoint name : "description or link"
pushbullet_endpoints = {
    "list devices":"devices",
    "user info":"users/me"
}


class Config(object):
    if os.environ.get('CLIENT_ID'):
        CLIENT_ID = os.environ.get('CLIENT_ID')
    else:
        CLIENT_ID = 'CLIENT_ID_NOT_SPECIFIED'
        print('CLIENT_ID needs to be specified in a config.env file.')

    if os.environ.get('CLIENT_SECRET'):
        CLIENT_ID = os.environ.get('CLIENT_SECRET')
    else:
        CLIENT_ID = 'CLIENT_SECRET_NOT_SPECIFIED'
        print('CLIENT_SECRET needs to be specified in a config.env file.')

    def __init__(self,__verbose__ = False):
        print('init')

    