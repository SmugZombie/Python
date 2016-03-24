#!/usr/bin/python
# A simple python script to view zones in cloudflare
# Ron Egli
# github.com/smugzombie

import json
import urllib2
import requests

auth_email = ''
auth_key = ''
endpoint = "https://api.cloudflare.com/client/v4/"

headers = {'x-auth-email': auth_email, 'x-auth-key': auth_key}

def apiGet(apiMethod):
        url = endpoint + apiMethod

        response = requests.request("GET", url, headers=headers)
        response = json.loads(response.text);

        print len(response['result'])

        for x in xrange(len(response['result'])):
                print response['result'][x]['id'],response['result'][x]['name']
                apiGetDns(response['result'][x]['id'])

def apiGetDns(domain_id):
        url = endpoint + "zones/" + domain_id + "/dns_records?per_page=100"

        response = requests.request("GET", url, headers=headers)
        response = json.loads(response.text);

        print len(response['result'])

        for x in xrange(len(response['result'])):
                print response['result'][x]['id'],response['result'][x]['name'],response['result'][x]['type'],response['result'][x]['content']
                
apiGet("zones?per_page=50")
