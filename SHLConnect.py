import datetime
import requests
import json


class SHLConnect:

    def __init__(self):
        self.username = '503c29078c5f95d87be8ffd218c72b30'
        self.password = 'bbec67659209479c030f3793f9f5228f7aa50c172bdc5bf0d1445abf791a14da'
        self.response = None
        self.access_token = ''
        self.baseUrl = 'https://openapi.shl.se'
        self.expires = datetime.datetime.now()

    def do_connection(self):
        header = {'Content-Type': 'application/x-www-form-urlencoded'}
        param = {
            'grant_type': 'client_credentials',
            'client_id': self.username,
            'client_secret': self.password,
        }
        self.response = requests.post('https://openapi.shl.se/oauth2/token', headers=header, data=param)
        j = self.response.json()
        j2 = json.dumps(j)
        self.access_token = json.loads(j2)
        self.access_token = self.access_token["access_token"]
        self.expires = json.loads(j2)
        self.expires = datetime.datetime.now() + datetime.timedelta(seconds=self.expires["expires_in"])

    def do_get(self, query):
        if datetime.datetime.now() >= self.expires:
            self.do_connection()
        header = {'Authorization': 'Bearer ' + self.access_token}
        r = requests.get(self.baseUrl + query, headers=header)
        return r
