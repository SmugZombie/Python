#!/usr/bin/python
import json
import urllib2
import argparse
import os
import ssl
from subprocess import call

arguments = argparse.ArgumentParser()
arguments.add_argument('--verbose','-v', help="Prints to screen the activity / response of the script", required=False, action='store_true')
args = arguments.parse_args()
verbosity = args.verbose

#if verbosity is True:
#	print verbosity
#else:
#	print "QuietMode"

def sendAlert(server, data):
        req = urllib2.Request(server)
        req.add_header('Content-Type', 'application/json')

        # SSL
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        # response = urllib2.urlopen(req, data)
        response = urllib2.urlopen(req, data, context=ctx)
        if verbosity is True:
                print "[-] Response code: ", response.getcode()
                print "[-] Returned content:\n", response.read()
        return response


###########################################################################
#
# MAIN PROGRAM STARTS HERE!
#
###########################################################################

json = '{"message":"hello world"}'
server = "https://cronwtf.com/python/"

sendAlert(server, json)

#print call(["ls", "-larth"])
#print call(["ifconfig", "| grep 192"])
#subprocess.call("ifconfig", shell=True)
