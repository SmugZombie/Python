#!/usr/bin/env python
## Tiny Python Syslog Server
## Version 0.13

## Ron Egli - github.com/smugzombie
import SocketServer, time, os, ConfigParser
import pythoncom
import win32serviceutil
import win32service
import win32event
import servicemanager
import socket

# User Definable Variables
CURRENT_PATH = str(os.path.dirname(os.path.realpath('__file__'))) + "/"
CONFIG_PATH = CURRENT_PATH+"syslog_server.ini"

# INI Defaults - Changes here will not take effect unless you remove the ini file
HOST, PORT = "0.0.0.0", 514           # Listener IP and Port
LOG_PATH = '../logs/'                 # Path to where you want the logs to go
LOG_FILE = 'syslog.log'      # Name of the log file to write to
OLD_LOG_FILE = 'syslog.yesterday.log' # Name of the log file to rotate to
MAX_LOG_SIZE = 50                      # Max log file size before rotation in Megabytes

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
readConfig()
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

class AppServerSvc (win32serviceutil.ServiceFramework):
    _svc_name_ = "SyslogServer"
    _svc_display_name_ = "SyslogServer"

    def __init__(self,args):
        win32serviceutil.ServiceFramework.__init__(self,args)
        self.hWaitStop = win32event.CreateEvent(None,0,0,None)
        socket.setdefaulttimeout(60)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_,''))
        self.main()

    def main(self):
        pass

# MAIN
if __name__ == "__main__":
	win32serviceutil.HandleCommandLine(AppServerSvc)
	try:
		server = SocketServer.UDPServer((HOST,PORT), SyslogUDPHandler)
		server.serve_forever(poll_interval=0.5)
	except (IOError, SystemExit):
		raise
	except KeyboardInterrupt:
		print ("Crtl+C Pressed. Shutting down.")
