import subprocess, re, time

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

	#print status

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

#print startService("taskfetcher")
print getServiceStatus("taskfetcher")
#time.sleep(1)
#print getServiceStatus("taskfetcher")
#print stopService("taskfetcher")
#print getServiceStatus("taskfetcher")
