# Python Imports
import json
import subprocess
import pprint
import argparse
import commands
import os
import textwrap

#counter = 0
#proceed = False
#while proceed is False:
#	if counter == 10:
#		proceed = True
#	else:
#		print counter
#		counter += 1
#print "Done"

#proceed = False
#while proceed is False:
#	print "Do you want to continue?"
#	answer = raw_input()
#	if answer == "y":
#		proceed = False
#	elif answer == "n":
#		proceed = True
#print "Done"

def addHost():
	proceed = False
	while proceed is False:
		print "Enter a valid hostname. (Valid resolvable hostname or IP)"
		hostname = raw_input()
		if hostname == "":
			proceed = False
		else:
			print "Do you wish to continue with", hostname,"? (Y/N)"
			answer = raw_input()
			if answer == "y" or answer == "Y":
				proceed = True

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

addHost()
