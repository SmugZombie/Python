#!/usr/bin/python
# Script: fim.py
# Purpose: A tiny fim agent using python
# Author: Ron Egli - github.com/smugzombie
version="0.3"

# Imports
import threading, time, json, sys, os, hashlib

# Define variables
fimjson = {}
fimjson['stats'] = {}
fimjson['files'] = {}
rootdir = 'C:\Windows\System32'

# Compute MD5 Hash
def md5(fileName):
    try:
        fileHandle = open(fileName, "rb")
    except IOError:
        return
    m5Hash = hashlib.md5()
    while True:
        data = fileHandle.read(8192)
        if not data:
            break
        m5Hash.update(data)
    fileHandle.close()
    return str(m5Hash.hexdigest())

# Compute SHA1 hash
def sha1(fileName):
    try:
        fileHandle = open(fileName, "rb")
    except IOError:
        return
    sha1hash = hashlib.sha1()
    while True:
        data = fileHandle.read(8192)
        if not data:
            break
        sha1hash.update(data)
    fileHandle.close()
    return str(sha1hash.hexdigest())

class myThread (threading.Thread):
    def __init__(self, threadID, filename):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.filename = filename
    def run(self):
 		getHashes(self.filename)

def getHashes(filename):
	if filename is not "None":
		fimjson['files'][filename] = {}
		fimjson['files'][filename]['md5'] = md5(filename)
		fimjson['files'][filename]['sha1'] = sha1(filename)

# Set Start Time
startTime = time.time()

count = 0
for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        filename = os.path.join(subdir, file)
        count += 1
        thisThread = myThread(count, filename)
        thisThread.start()

elapsedTime = time.time() - startTime

fimjson['stats']['start'] = startTime
fimjson['stats']['duration'] = elapsedTime
fimjson['stats']['version'] = version

with open("fim.json", 'w') as fimoutput:
    fimoutput.write(json.dumps(fimjson))

