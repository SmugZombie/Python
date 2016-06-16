#!/usr/bin/env python
## Tiny Python Syslog Server
## Version 0.11.1

## Ron Egli - github.com/smugzombie
import SocketServer, time, os

# User Definable Variables
HOST, PORT = "0.0.0.0", 514           # Listener IP and Port
LOG_PATH = '../logs/'                 # Path to where you want the logs to go
LOG_FILE = LOG_PATH+'syslog.log'      # Name of the log file to write to
OLD_LOG_FILE = LOG_PATH+'syslog.yesterday.log' # Name of the log file to rotate to
MAX_LOG_SIZE = 50                     # Max log file size before rotation in Megabytes

# Dynamic Variables
statCount = 0                         # Incremental to be used by the script
sizeCheck = 250                       # Recheck log file size after every X logs written

def checkLogDir(LOG_PATH):
	# If the log directory doesn't exist, create it.
	if not os.path.exists(LOG_PATH):
		os.makedirs(LOG_PATH)

def Logger(message):
	print message # Debugging
	log = open(LOG_FILE,'a')  # Open file in append mode
	log.write(message+'\n')   # Write to file
	log.close()               # Close file

def checkRotate():
	# Check the size of the file, if above MAX_LOG_SIZE fire off logRotate, otherwise keep logging
	logSize = os.stat(LOG_FILE).st_size # filesize in bytes
	megaBytes = logSize / 1048576       # convert to megabytes
	if megaBytes >= MAX_LOG_SIZE:
		logRotate()

def logRotate():
	# Delete OLD_LOG_FILE and move LOG_FILE to its place.
	os.remove(OLD_LOG_FILE)
	os.rename(LOG_FILE, OLD_LOG_FILE)

# Ensure Log directory exists
checkLogDir(LOG_PATH)

class SyslogUDPHandler(SocketServer.BaseRequestHandler):
	def handle(self):
		global statCount
		now = time.strftime("%b %d %H:%I:%S")
		data = bytes.decode(self.request[0].strip())
		socket = self.request[1]
		message = str(now)+" "+str(self.client_address[0])+" "+str(data)
		Logger(message)
		statCount += 1
		if statCount >= 250:
			checkRotate()
			statcount = 0

# MAIN
if __name__ == "__main__":
	try:
		server = SocketServer.UDPServer((HOST,PORT), SyslogUDPHandler)
		server.serve_forever(poll_interval=0.5)
	except (IOError, SystemExit):
		raise
	except KeyboardInterrupt:
		print ("Crtl+C Pressed. Shutting down.")
