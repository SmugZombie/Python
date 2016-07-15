# Script: fim.py
# Purpose: A tiny fim/rim agent for Windows using python
# Author: Ron Egli - github.com/smugzombie
version="0.6"

# Imports
import hashlib, json, os, time, sys, _winreg

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
            fimjson['files'][filename]['type'] = "fim"
            if DEBUG: print filename, json.dumps(fimjson['files'][filename])    

def getRegKey(path):
    path = path[19:]
    try:
        key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, path, 0, _winreg.KEY_READ)
        output = ""
        for i in xrange(0, _winreg.QueryInfoKey(key)[1]):
            output += str(_winreg.EnumValue(key, i))
    except:
            output = "null"
    return output

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
    fimjson['files'][filename]['type'] = "fim"
    if DEBUG: print filename, json.dumps(fimjson['files'][filename])

# Loop Through Specified Directories
directorycount = len(config['config']['directories'])
for x in xrange(directorycount):
    directoryname = config['config']['directories'][x]
    scanDirectory(directoryname)

# Setup Hashing for Values
md = hashlib.md5(); sh = hashlib.sha1()

# Loop Through Specified Registry Keys
registrycount = len(config['config']['registry'])
for x in xrange(registrycount):
    registryname = config['config']['registry'][x]
    registryValue = getRegKey(registryname)
    fimjson['files'][registryname] = {}
    if registryValue is not "null":
        md.update(registryValue); sh.update(registryValue)
        fimjson['files'][registryname]['md5'] = str(md.hexdigest())
        fimjson['files'][registryname]['sha1'] = str(sh.hexdigest())
    else:
        fimjson['files'][registryname]['md5'] = registryValue
        fimjson['files'][registryname]['sha1'] = registryValue
    fimjson['files'][registryname]['type'] = "rim"

# Compile JSON Stats
elapsedTime = time.time() - startTime
fimjson['stats']['start'] = round(startTime, 2)
fimjson['stats']['duration'] = round(elapsedTime, 2)
fimjson['stats']['version'] = version

# Write to file
with open("fim.json", 'w') as fimoutput:
    fimoutput.write(json.dumps(fimjson))
