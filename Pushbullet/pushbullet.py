import json
import datetime
import os
import requests

__bearer_token_override__ = True

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

class Config():
    API_ROOT = "https://api.pushbullet.com/v2/"
    CLIENT_ID = None
    CLIENT_SECRET = None
    AUTH_CODE = None
    ACCESS_TOKEN = None
    BEARER_TOKEN = None

    def __init__(self,__verbose__ = False):
        print('New Run:  {0}'.format(datetime.datetime.now()))
        if os.environ.get('CLIENT_ID'):
            self.CLIENT_ID = os.environ.get('CLIENT_ID')
        else:
            self.CLIENT_ID = 'CLIENT_ID_NOT_SPECIFIED'
            print('CLIENT_ID needs to be specified in a config.env file.')

        if os.environ.get('CLIENT_SECRET'):
            self.CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
        else:
            self.CLIENT_SECRET = 'CLIENT_SECRET_NOT_SPECIFIED'
            print('CLIENT_SECRET needs to be specified in a config.env file.')
        if os.environ.get('AUTH_CODE'):
            self.AUTH_CODE = os.environ.get('AUTH_CODE')
        else:
            self.AUTH_CODE = 'AUTH_CODE_NOT_SPECIFIED'
            print('AUTH_CODE needs to be specified in a config.env file.')

        if os.environ.get('PB_ACCESS_TOKEN'):
            self.ACCESS_TOKEN = os.environ.get('PB_ACCESS_TOKEN')
        else:
            self.ACCESS_TOKEN = 'ACCESS_TOKEN_NOT_SPECIFIED'
            print('ACCESS_TOKEN needs to be specified in a config.env file.')

        if (__bearer_token_override__):
            self.BEARER_TOKEN = os.environ.get('BEARER_TOKEN')

    def query_endpoint():
        print('query ep')

    def get_bearer_token(self):
        if(__bearer_token_override__ and self.BEARER_TOKEN):
            print("Bearer token override enabled and Bearer token already properly set.")
        else:
            endpoint = self.API_ROOT + pushbullet_endpoints['bearer token']
            headers = {}

            headers["Access-Token"] = self.ACCESS_TOKEN
            headers["Content-Type"] = "application/json"
            dataset = {}

            dataset['client_id'] = self.CLIENT_ID
            dataset['client_sercret'] = self.CLIENT_SECRET
            dataset['code'] = self.AUTH_CODE
            dataset['grant_type'] = 'authorization_code'

            response = requests.post(endpoint,headers=headers,data=dataset)
            if (response.status_code == 200):
                self.BEARER_TOKEN = response.content['Access-Token']
                print ("Bearer token successfully retrieved")
            else:
                print (response.content)
                self.BEARER_TOKEN = "BEARER_TOKEN_NOT_SET"
                if (__cmh__):
                    print("\n")
                    print(json.dumps(dataset))
                    print("\n")
                    print(json.dumps(headers))
                    print("\n")
                    print(endpoint)
                    print(response.status_code)

    def get_devices(query_endpoint):
        headers = {'Access-Token':"a"}
        response = requests.get(self.API_ROOT + pushbullet_endpoints['user info'])

test=Config().get_bearer_token()