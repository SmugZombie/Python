#!/usr/bin/env python
## Tiny Python Syslog Server
## Version 0.10

## Ron Egli - github.com/smugzombie

HOST, PORT = "0.0.0.0", 514
LOG_PATH = '../logs/'
LOG_FILE = LOG_PATH+'syslog.log'
OLD_LOG_FILE = LOG_PATH+'syslog.yesterday.log'

import SocketServer
import time
import os

def checkLogDir(LOG_PATH):
	if not os.path.exists(LOG_PATH):
		os.makedirs(LOG_PATH)

def Logger(message):
	print message # Debugging
	log = open(LOG_FILE,'a')  # Open file in append mode
	log.write(message+'\n')   # Write to file
	log.close()               # Close file

# Ensure Log directory exists
checkLogDir(LOG_PATH)

class SyslogUDPHandler(SocketServer.BaseRequestHandler):
	def handle(self):
		now = time.strftime("%b %d %H:%I:%S")
		data = bytes.decode(self.request[0].strip())
		socket = self.request[1]
		message = str(now)+" "+str(self.client_address[0])+" "+str(data)
		Logger(message)

if __name__ == "__main__":
	try:
		server = SocketServer.UDPServer((HOST,PORT), SyslogUDPHandler)
		server.serve_forever(poll_interval=0.5)
	except (IOError, SystemExit):
		raise
	except KeyboardInterrupt:
		print ("Crtl+C Pressed. Shutting down.")
