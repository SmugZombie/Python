import subprocess, re, time, ConfigParser, os

SERVICES = ['TaskFetcher','Syslog','ossecsvc'];
INTERVAL = 3000 # 5 Minutes

config = ConfigParser.RawConfigParser()

def getServiceStatus(service):
	regex = r"STATE\s*:\ \d{1,3}\s*(?P<status>\S*)"

	try:
		output = subprocess.check_output("sc query " + service)
	except:
		output = ""

	matches = re.search(regex, output, re.MULTILINE)

	try:
		status = matches.group("status")
	except:
		status = ""

	if status == "RUNNING":
		return 1
	elif status == "STOPPED":
		return 2
	elif status == "PAUSED":
		return 3
	elif status == "START_PENDING" or status == "STOP_PENDING":
		return 3
	else:
		return 0

def stopService(service):
	try:
		subprocess.check_output("sc stop " + service)
		return 1
	except:
		return 0

def startService(service):
	try:
		subprocess.check_output("sc start " + service)
		return 1
	except:
		return 0
				
def restartService(service):
	stopService(service)
	startService(service)

# Run Forever
while True:
	for SERVICE in SERVICES:
		STATUS = getServiceStatus(SERVICE)
		# If service not found, no biggie
		if STATUS == 0:
			print "Service: " + str(SERVICE) + " is not installed."
		# If service found and running, way to go
		elif STATUS == 1:
			print "Service: " + str(SERVICE) + " is already running."
		# If service found but not running, kick it
		elif STATUS == 2:
			print "Service: " + str(SERVICE) + " is stopped."
			restartService(SERVICE)
			print "Service: " + str(SERVICE) + " is starting."
		# If service found, but is pending state, check again next time
		else:
			print "Service: " + str(SERVICE) + " status is pending."
	# Sleep
	time.sleep(INTERVAL)	
