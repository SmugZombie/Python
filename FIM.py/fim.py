# Script: fim.py
# Purpose: A tiny fim/rim agent for Windows using python
# Author: Ron Egli - github.com/smugzombie
version="0.5.1"

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

def regkey_value(path, name="", start_key = None):
    try:
        if isinstance(path, str):
            path = path.split("\\")
        if start_key is None:
            start_key = getattr(_winreg, path[0])
            return regkey_value(path[1:], name, start_key)
        else:
            subkey = path.pop(0)
        with _winreg.OpenKey(start_key, subkey) as handle:
            assert handle
            if path:
                return regkey_value(path, name, handle)
            else:
                desc, i = None, 0
                while not desc or desc[0] != name:
                    desc = _winreg.EnumValue(handle, i)
                    i += 1
                return desc[1]
    except:
        return "null"

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
    registryValue = regkey_value(str(registryname),"")
    fimjson['files'][registryname] = {}
    md.update(registryValue); sh.update(registryValue)
    fimjson['files'][registryname]['md5'] = str(md.hexdigest())
    fimjson['files'][registryname]['sha1'] = str(sh.hexdigest())
    fimjson['files'][registryname]['type'] = "rim"

# Compile JSON Stats
elapsedTime = time.time() - startTime
fimjson['stats']['start'] = round(startTime, 2)
fimjson['stats']['duration'] = round(elapsedTime, 2)
fimjson['stats']['version'] = version

# Write to file
with open("fim.json", 'w') as fimoutput:
    fimoutput.write(json.dumps(fimjson))
