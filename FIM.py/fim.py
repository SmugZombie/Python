# Script: fim.py
# Purpose: A tiny fim agent using python
# Author: Ron Egli - github.com/smugzombie
version="0.2"

# Imports
import hashlib, json, os, time, sys

try: ARGS = sys.argv;
except: ARGS = "";

if "-d" in ARGS:
        DEBUG = True

# Define variables
fimjson = {}
fimjson['stats'] = {}
fimjson['files'] = {}
rootdir = 'C:\Windows\System32'

# Non Definable Variables
DEBUG = False

### FUNCTIONS ###

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

### Main ###

# Set Start Time
startTime = time.time()

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        filename = os.path.join(subdir, file)
        #print md5(filename), sha1(filename), filename
        fimjson['files'][filename] = {}
        fimjson['files'][filename]['md5'] = md5(filename)
        fimjson['files'][filename]['sha1'] = sha1(filename)
        if DEBUG: print filename, json.dumps(fimjson['files'][filename])

elapsedTime = time.time() - startTime

fimjson['stats']['start'] = startTime
fimjson['stats']['duration'] = elapsedTime
fimjson['stats']['version'] = version

with open("fim.json", 'w') as fimoutput:
    fimoutput.write(json.dumps(fimjson))
