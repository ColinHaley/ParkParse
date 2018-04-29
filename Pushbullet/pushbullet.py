import json
import datetime
import os
import requests

# Override and global variables
__bearer_token_override__ = True
__cmh__ = None
# End override and global variables

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
    "bearer token":"oauth2/token",
    "send message":"ephemerals"
}

class PushBullet(object):
    API_ROOT = "https://api.pushbullet.com/v2/"

    # These settings must be specified in the .env file.
    CLIENT_ID = None
    CLIENT_SECRET = None
    AUTH_CODE = None
    ACCESS_TOKEN = None

    # The Bearer Token should be retrieved live via the Config.update_bearer_token() call
    # if necessary, the BEARER_TOKEN config line can be written and a global override of
    # __bearer_token_override__ can be set to True to read from the config.
    BEARER_TOKEN = None

    # These objects will be set and referenced by other methods within the class
    PB_USER_IDEN = None
    PB_DEVICES = {}

    def __init__(self):
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

        self.update_bearer_token()
        self.update_user_iden()
        self.update_devices()

    def update_bearer_token(super):
        if(__bearer_token_override__ and super.BEARER_TOKEN):
            print("Bearer token override enabled and Bearer token already properly set.")
        else:
            endpoint = super.API_ROOT + pushbullet_endpoints['bearer token']
            headers = {}

            headers["Access-Token"] = super.ACCESS_TOKEN
            headers["Content-Type"] = "application/json"
            dataset = {}

            dataset['client_id'] = super.CLIENT_ID
            dataset['client_sercret'] = super.CLIENT_SECRET
            dataset['code'] = super.AUTH_CODE
            dataset['grant_type'] = 'authorization_code'

            response = requests.post(endpoint,headers=headers,data=dataset)
            if (response.status_code == 200):
                super.BEARER_TOKEN = response.content['Access-Token']
                print ("Bearer token successfully retrieved")
            else:
                print (response.content)
                super.BEARER_TOKEN = "BEARER_TOKEN_NOT_SET"
                if (__cmh__):
                    print("\n")
                    print(json.dumps(dataset))
                    print("\n")
                    print(json.dumps(headers))
                    print("\n")
                    print(endpoint)
                    print(response.status_code)

    def update_user_iden(self):
        headers = {'Access-Token':self.BEARER_TOKEN}
        response = requests.get(self.API_ROOT + pushbullet_endpoints['user info'],headers=headers)
        if (response.status_code == 200):
            self.PB_USER_IDEN = json.loads(response.content)['iden']
        else:
            print("Error acquiring user iden key from pushbullet")
            self.PB_USER_IDEN = "PB_USER_IDEN_NOT_SET"

    def get_user_iden(super):
        if (__cmh__):
            print super.PB_USER_IDEN
        return super.PB_USER_IDEN

    def update_devices(super):
        headers = {'Access-Token':super.BEARER_TOKEN}
        response = requests.get(super.API_ROOT + pushbullet_endpoints['list devices'],headers=headers)
        if (response.status_code == 200):
            for device in json.loads(response.content)['devices']:
                super.PB_DEVICES[device['type']] = {
                    "nickname": device['nickname'],
                    "iden" : device['iden']
                }
        else:
            print("Error acquiring user iden key from pushbullet")
            super.PB_DEVICES= "PB_USER_IDEN_NOT_SET"

    def get_devices(super):
        if(__cmh__):
            print super.PB_DEVICES
        return super.PB_DEVICES

    def send_message(super, message, phone_number):
        endpoint = super.API_ROOT + pushbullet_endpoints['send message']
        headers = {"Access-Token":super.BEARER_TOKEN,
                   "Content-Type":"application/json"}
        payload = {"push":{"conversation_iden": phone_number,"message": message,"package_name": "com.pushbullet.android",
                           "source_user_iden": super.PB_USER_IDEN,"target_device_iden": super.PB_DEVICES['android']['iden'],
                           "type": "messaging_extension_reply"}, "type": "push"}
        response = requests.post(endpoint, headers=headers, data=json.dumps(payload))
        if(__cmh__):
            print response.content

        print("message sent")

    #TODO: Write debug method for Config() class