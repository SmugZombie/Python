#!/usr/bin/env python
## Tiny Python Syslog Server
## Version 0.12.9

## Ron Egli - github.com/smugzombie
import SocketServer, time, os, ConfigParser, sys

# User Definable Variables
CURRENT_PATH = str(os.path.dirname(os.path.realpath('__file__'))) + "/"
CONFIG_PATH = CURRENT_PATH+"syslog_server.ini"

# INI Defaults - Changes here will not take effect unless you remove the ini file
HOST, PORT = "0.0.0.0", 514           # Listener IP and Port
LOG_PATH = '../logs/'                 # Path to where you want the logs to go
LOG_FILE = 'syslog.log'      # Name of the log file to write to
OLD_LOG_FILE = 'syslog.yesterday.log' # Name of the log file to rotate to
MAX_LOG_SIZE = 1024                     # Max log file size before rotation in Megabytes
DEBUG = False

try: ARGS = sys.argv; 
except: ARGS = "";

if "-d" in ARGS:
	DEBUG = True

# Dynamic Variables
statCount = 0                         # Incremental to be used by the script
sizeCheck = 2500                      # Recheck log file size after every X logs written
config = ConfigParser.RawConfigParser()

def readConfig():
	# Read configuration from ini file
	global HOST, PORT, LOG_PATH, LOG_FILE, OLD_LOG_FILE, MAX_LOG_SIZE
	if not os.path.exists(CONFIG_PATH):
		writeConfig()
		return
	config.read(CONFIG_PATH)
	HOST = config.get('Settings', 'HOST')
	PORT = config.getint('Settings', 'PORT')
	LOG_PATH = config.get('Settings', 'LOG_PATH')
	LOG_FILE = str(LOG_PATH + config.get('Settings', 'LOG_FILE'))
	OLD_LOG_FILE = str(LOG_PATH + config.get('Settings', 'OLD_LOG_FILE'))
	MAX_LOG_SIZE = config.getint('Settings', 'MAX_LOG_SIZE')

def writeConfig():
	# Write new configuration to ini file
	config.add_section('Settings')
	config.set('Settings','HOST',HOST)
	config.set('Settings','PORT',PORT)
	config.set('Settings','LOG_PATH',LOG_PATH)
	config.set('Settings','LOG_FILE',LOG_FILE)
	config.set('Settings','OLD_LOG_FILE',OLD_LOG_FILE)
	config.set('Settings','MAX_LOG_SIZE',MAX_LOG_SIZE)

	with open(CONFIG_PATH, 'wb') as configfile:
		config.write(configfile)
	readConfig()

def checkLogDir(LOG_PATH):
	# If the log directory doesn't exist, create it.
	if not os.path.exists(LOG_PATH):
		os.makedirs(LOG_PATH)
	# Create Syslog File if not exist
	if not os.path.isfile(LOG_FILE):
		open(LOG_FILE, 'a').close()

def Logger(message):
	now = time.strftime("%b %d %H:%M:%S")
	if DEBUG:
		print message # Debugging
	log = open(LOG_FILE,'a')  # Open file in append mode
	log.write(now + " " + message + '\n')   # Write to file
	log.close()               # Close file

def checkRotate():
	# Check the size of the file, if above MAX_LOG_SIZE fire off logRotate, otherwise keep logging
	logSize = os.stat(LOG_FILE).st_size # filesize in bytes
	megaBytes = logSize / 1048576       # convert to megabytes
	#Logger("DEBUG - Filesize "+str(megaBytes))
	if megaBytes >= MAX_LOG_SIZE:
		logRotate()

def logRotate():
	# Delete OLD_LOG_FILE and move LOG_FILE to its place.
	if os.path.isfile(OLD_LOG_FILE):
		os.remove(OLD_LOG_FILE)
	os.rename(LOG_FILE, OLD_LOG_FILE)

# Ensure Log directory exists
readConfig()
checkLogDir(LOG_PATH)

class SyslogUDPHandler(SocketServer.BaseRequestHandler):
	def handle(self):
		global statCount
		data = bytes.decode(self.request[0].strip())
		socket = self.request[1]
		message = str(self.client_address[0])+" "+str(data)
		Logger(message)

		if statCount >= 250:
			statCount = 0
			checkRotate()
		else:
			statCount += 1

# MAIN
if __name__ == "__main__":
	Logger('127.0.0.1 msg="Syslog Server Started"')
	try:
		server = SocketServer.UDPServer((HOST,PORT), SyslogUDPHandler)
		server.serve_forever(poll_interval=0.5)
	except (IOError, SystemExit):
		raise
	except KeyboardInterrupt:
		Logger('127.0.0.1 msg="Syslog Server Shutting Down"')
		print ("Crtl+C Pressed. Shutting down.")
