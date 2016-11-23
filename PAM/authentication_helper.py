#!/usr/bin/python
# authentication_helper.py
# Allows easy authentication to a unix based system via anything that can call this script
# github.com/smugzombie

import pam,sys,json

# Create JSON Object
response = {}

# Create PAM
p = pam.pam()

# Because we are lazy, we simply expect the proper data via sys.argv otherwise break
try:
        response['authenticated'] = p.authenticate(sys.argv[1], sys.argv[2])
        response['user'] = sys.argv[1]
        if response['authenticated']:
                response['message'] = "Authorized User"
        else:
                response['message'] = "Unauthorized User"
except:
        response['authenticated'] = False
        response['result'] = "fail"
        response['message'] = "Invalid Input Provided"

# Print response
print json.dumps(response)
