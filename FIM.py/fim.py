# Script: fim.py
# Purpose: A tiny fim agent using python
# Author: Ron Egli - github.com/smugzombie
version="0.4"

# Imports
import hashlib, json, os, time, sys

# Arguments for Debugging
try: ARGS = sys.argv; 
except: ARGS = "";
DEBUG = False
if "-d" in ARGS: DEBUG = True

# User Definable Variables
configFile = "fim.conf"
WINDIR = "C:\\\Windows"

# Predefined Variables
fimjson = {}
fimjson['stats'] = {}
fimjson['files'] = {}
config = {}


### FUNCTIONS ###
def loadConfig():
    global config
    try:
        with open ("fim.conf", "r") as myfile:
            data=myfile.read()
        data = data.replace("%WINDIR%", WINDIR)
        #print data
        config = json.loads(data) 
    except:
        print "Cannot Read Config - Exiting..."
        exit()

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

# Scan full directory and subdirectories
def scanDirectory(directory):
    global fimjson
    for subdir, dirs, files in os.walk(directory):
        for file in files:
            filename = os.path.join(subdir, file)
            fimjson['files'][filename] = {}
            fimjson['files'][filename]['md5'] = md5(filename)
            fimjson['files'][filename]['sha1'] = sha1(filename)
            if DEBUG: print filename, json.dumps(fimjson['files'][filename])    

### Main ###
# Start the Clock
startTime = time.time()

# Load the Configuration File
loadConfig()

# Loop Through Specified Files
filecount = len(config['config']['files'])
for x in xrange(filecount):
    filename = config['config']['files'][x]
    fimjson['files'][filename] = {}
    fimjson['files'][filename]['md5'] = md5(filename)
    fimjson['files'][filename]['sha1'] = sha1(filename)
    if DEBUG: print filename, json.dumps(fimjson['files'][filename])

# Loop Through Specified Directories
directorycount = len(config['config']['directories'])
for x in xrange(directorycount):
    directoryname = config['config']['directories'][x]
    scanDirectory(directoryname)

# Compile JSON Stats
elapsedTime = time.time() - startTime
fimjson['stats']['start'] = startTime
fimjson['stats']['duration'] = elapsedTime
fimjson['stats']['version'] = version

# Write to file
with open("fim.json", 'w') as fimoutput:
    fimoutput.write(json.dumps(fimjson))
