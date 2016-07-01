# Script: fim.py
# Purpose: A tiny fim agent using python
# Author: Ron Egli - github.com/smugzombie
# Version: 0.1

# Imports
import hashlib, json, os

# Define variables
fimjson = {}
rootdir = 'C:/cygwin64/'

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

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        filename = os.path.join(subdir, file)
        #print md5(filename), sha1(filename), filename
        fimjson[filename] = {}
        fimjson[filename]['md5'] = md5(filename)
        fimjson[filename]['sha1'] = sha1(filename)
        print filename, json.dumps(fimjson[filename])
