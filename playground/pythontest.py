#!/usr/bin/python
import json
import urllib2
import argparse
import os
import ssl
import subprocess
import socket

arguments = argparse.ArgumentParser()
arguments.add_argument('--code','-c', required=False, default="200")
arguments.add_argument('--url','-u', required=False, default='https://cronwtf.com/python/?code=')
arguments.add_argument('--verbose','-v', help="Prints to screen the activity / response of the script", required=False, action='store_true')
args = arguments.parse_args()
verbosity = args.verbose
incode = args.code
url = args.url

def post(server, data):
        req = urllib2.Request(server)
        req.add_header('Content-Type', 'application/json')

        # SSL
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        response = urllib2.urlopen(req, data, context=ctx)
        if verbosity is True:
                print "[-] Response code: ", response.getcode()
                print "[-] Returned content:\n", response.read()
        return response.getcode()

def post2(server, data):
        req = urllib2.Request(server)
        req.add_header('Content-Type', 'application/json')

        # SSL
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        try:
                response = urllib2.urlopen(req, data, context=ctx)
        except urllib2.HTTPError, err:
                #if err.code == 404:
                #        print "Page not found!"
                #elif err.code == 403:
                #        print "Access denied!"
                #elif err.code == 500:
                #        print "Server error!"
                #else:
                #        print "Something happened! Error code", err.code 
                print "[-] Response code: ", err.code              
                return 0
        print "[-] Response code: ", response.getcode()
        print "[-] Returned content:\n", response.read()
        return 1

def post3(server, data):
        req = urllib2.Request(server)
        #req.add_header('Content-Type', 'application/json')

        # SSL
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        output = {}
        output['url'] = server
        output['data'] = data

        try:
                response = urllib2.urlopen(req, data, context=ctx)
        except urllib2.HTTPError, err:
                output['code'] = err.code
                output['response'] = ""           
                return output
        else:
                output['code'] = response.getcode()
                output['response'] = response.read()
        return output


###########################################################################
#
# MAIN PROGRAM STARTS HERE!
#
###########################################################################

if url == "":
        server = "https://cronwtf.com/python/?code="
else:
        server = url

#server = "https://cronwtf.com/python/?code="
#hostname = socket.gethostname()
#post(server, json)

#responseCode = post(server, "")

#if responseCode == 200:
#        print "YEY"
#else:
#        print "BOO"

#myip = subprocess.check_output("ifconfig | grep 192", shell=True)
#print "My Internal Ip(s): ", myip

output = post3(server, "")
print output

#if output['code'] == 200:
#        print "Yey"
#else:
#        print "Boo"
#        print output
