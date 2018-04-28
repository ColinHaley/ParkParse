import json
import datetime
import os
import requests

API_ROOT="https://api.pushbullet.com/v2/"
CLIENT_ID = None
CLIENT_SECRET = None
AUTH_CODE = None
ACCESS_TOKEN = None

for line in open('config.env'):
    if line[0] == '#':
        continue
    var = line.strip().split('=')
    if len(var) == 2:
        os.environ[var[0]] = var[1]

#/endpoint name : "description or link"
pushbullet_endpoints = {
    "list devices":"devices",
    "user info":"users/me",
    "bearer token":"oauth2/token"
}

class Config(object):
    if os.environ.get('CLIENT_ID'):
        CLIENT_ID = os.environ.get('CLIENT_ID')
        print(CLIENT_ID)
    else:
        CLIENT_ID = 'CLIENT_ID_NOT_SPECIFIED'
        print('CLIENT_ID needs to be specified in a config.env file.')

    if os.environ.get('CLIENT_SECRET'):
        CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
        print(CLIENT_SECRET)
    else:
        CLIENT_SECRET = 'CLIENT_SECRET_NOT_SPECIFIED'
        print('CLIENT_SECRET needs to be specified in a config.env file.')

    if os.environ.get('AUTH_CODE'):
        AUTH_CODE = os.environ.get('AUTH_CODE')
        print(AUTH_CODE)
    else:
        AUTH_CODE = 'AUTH_CODE_NOT_SPECIFIED'
        print('AUTH_CODE needs to be specified in a config.env file.')

    if os.environ.get('PB_ACCESS_TOKEN'):
        ACCESS_TOKEN = os.environ.get('PB_ACCESS_TOKEN')
        print(ACCESS_TOKEN)
    else:
        ACCESS_TOKEN = 'ACCESS_TOKEN_NOT_SPECIFIED'
        print('ACCESS_TOKEN needs to be specified in a config.env file.')

    def __init__(self,__verbose__ = False):
        print('New Run:  {0}'.format(datetime.datetime.now()))

    def query_endpoint(sel  f):
        print('query ep')

    def get_bearer_token(query_endpoint):
        endpoint = API_ROOT + pushbullet_endpoints['bearer token']
        headers = {
            "Access-Token":ACCESS_TOKEN,
            "Content-Type":"application/json"
        }
        dataset = {
            'client_id' : CLIENT_ID,
            'client_sercret' : CLIENT_SECRET,
            'code' : AUTH_CODE,
            'grant_type' : 'authorization_code'
        }
        response = requests.post(endpoint,headers=headers,data=dataset)
        print (response.content)
        print("\n")
        print (endpoint)
        print('\n')
        print(json.dumps(dataset))


    @staticmethod
    def get_devices(query_endpoint):
        headers = {'Access-Token':"a"}
        response = requests.get(API_ROOT + pushbullet_endpoints['user info'])

test=Config().get_bearer_token()