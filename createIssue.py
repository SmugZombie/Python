#!/usr/bin/python
# A simple python script to create new issues in GIT for a specific repo
# Ron Egli
# github.com/smugzombie

import json
import urllib2
import argparse

repo_owner = 'SmugZombie'
repo_name = 'Python'
api_key = ''

arguments = argparse.ArgumentParser()
arguments.add_argument('--title','-t', help="Title of the issue being created", required=True, default='')
arguments.add_argument('--message','-m', help="Message body of the issue being created", required=True, default="")
args = arguments.parse_args()
title = args.title
message = args.message

url = "https://api.github.com/repos/%s/%s/issues" % (repo_owner, repo_name)

data = {}
data['title'] = "User Submitted - "+str(title)
data['body'] = str(message)
data['assignee'] = "Smugzombie"

def createIssue():
        global data;
        req = urllib2.Request(url)
	req.add_header('content-type', 'application/json')
	req.add_header('authorization', 'token %s' % (api_key))

        output = {};
        output['url'] = url

        try:
                response = urllib2.urlopen(req, json.dumps(data),timeout = 10)
        except urllib2.HTTPError, err:
                print err.code
        except:
                print "Timeout"
        else:
                response = json.loads(response.read())
		if response['title'] == data['title']:
			print "success"
		else:
			print "error"

createIssue()
