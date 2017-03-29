# Password Gen
# Ron Egli github.com/smugzombie
# Allows simple generation of strong passwords provided by dinopass - Once created updates to latest clipboard entry

import requests, pyperclip, os

def generatePassword():
	url = "http://www.dinopass.com/password/strong"
	headers = { 'cache-control': "no-cache" }
	response = requests.request("GET", url, headers=headers)
	return response.text
	
try: password = generatePassword()
except: print "Unable to generate password."; exit()

try: pyperclip.copy(password); print str(password) + " (Copied!)"
except: print "Unable to copy password."
