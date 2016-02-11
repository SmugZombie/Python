# Python Imports
import json
import subprocess
import pprint
import argparse
import commands
import os
import textwrap

def testPing(host):
        if OS == "CYGWIN":
                output = commands.getstatusoutput("timeout 1 ping " + host + " -n 1 | grep -E -o 'Received = [0-9]+' | awk {'print $3'}")[1]
        elif OS == "LINUX":
                output = commands.getstatusoutput("timeout 1 ping " + host + " -c 1 | grep -E -o '[0-9]+ received' | cut -f1 -d' '")[1]
        elif OS == "OSX":
                output = commands.getstatusoutput("timeout 1 ping " + host + " -c 1 | grep -E -o '[0-9]+ received' | cut -f1 -d' '")[1]
        else:
                output = commands.getstatusoutput("echo 0'")[1]
        if str(output) != "1":
                output = "0";
        return output

def getOS():
	global OS
        output = commands.getstatusoutput('uname')[1]
        if output.find("CYGWIN") != -1:
                output = "CYGWIN"
        elif output.find("Linux") != -1:
                output = "LINUX"
        elif output.find("Darwin") != -1:
                output = "OSX"
	OS = output
        return

def addHost():
	proceed = False
	while proceed is False:
		print "Enter a valid hostname. (Valid resolvable hostname or IP)"
		hostname = raw_input()
		if hostname == "":
			proceed = False
		else:
			online = testPing(hostname)
			if online == "1":
				print "Do you wish to continue with", hostname,"? (Y/N)"
				answer = raw_input()
				if answer == "y" or answer == "Y":
					proceed = True
			else:
				print "Unable to resolve",hostname,". Please enter a new hostname."
	proceed = False
	while proceed is False:
		print "Enter the standard username for ", hostname,". (Blank if none)"
		username = raw_input()
		if username == "":
			print "No standard username? (Y/N)"
		else:
			print "Is",username,"correct? (Y/N)"
		answer = raw_input()
		if answer == "y" or answer == "Y":
			proceed = True

	proceed = False
	while proceed is False:
        	print "Enter the sudo username for ", hostname,". (Blank if none)"
        	sudousername = raw_input()
		if sudousername == "":
			print "No sudo username? (Y/N)"
		else:
        		print "Is",sudousername,"correct? (Y/N)"
        	answer = raw_input()
        	if answer == "y" or answer == "Y":
                	proceed = True

	proceed = False
	while proceed is False:
        	print "Enter the group", hostname,"belongs to (Blank for Default)"
        	group = raw_input()
        	if group == "":
			print "No group? (Y/N)"
		else:	
			print "Is",group,"correct? (Y/N)"
        	answer = raw_input()
        	if answer == "y" or answer == "Y":
                	proceed = True

	proceed = False
	while proceed is False:
        	print "If required, provide the path to the non default SSH Key", hostname,"(Blank for Default)"
        	keyfile = raw_input()
		if keyfile == "":
			print "No special SSH Key? (Y/N)"
		else:
        		print "Is",keyfile,"correct? (Y/N)"
        	answer = raw_input()
        	if answer == "y" or answer == "Y":
                	proceed = True

	print "So far we have"
	print "Hostname:", hostname
	print "User    :", username
	print "SudoUser:", sudousername
	print "Group   :", group
	print "KeyFile :", keyfile
	return

getOS()
addHost()
