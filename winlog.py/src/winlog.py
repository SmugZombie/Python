# winlog.py
# A standalone Winlog executable for ease of test logging
# Ron Egli - github.com/smugzombie
# Version 0.1

# Imports
import win32api, win32con, win32evtlog
import win32security, win32evtlogutil, argparse
 
# Setup Logging
currentProcess = win32api.GetCurrentProcess()
processToken = win32security.OpenProcessToken(currentProcess, win32con.TOKEN_READ)
mySid = win32security.GetTokenInformation(processToken, win32security.TokenUser)[0]

# Get arguments from user
arguments = argparse.ArgumentParser()
arguments.add_argument('--application','-a', help="Name of the application to be logged as", required=True)
arguments.add_argument('--eventid','-e', help="Specific Event Id for forwarded log (Default 1)", required=False, default=1)
arguments.add_argument('--category','-c', help="Specific Event Category for forwarded log (Default 5)", required=False, default=5)
arguments.add_argument('--type','-t', help="Type of Log (Information / Error / Warning) (Default Information)", required=False, default="info")
arguments.add_argument('--logtitle','-lt', help="Title of forwarded log", required=False, default="")
arguments.add_argument('--rawlog','-r', help="Raw contents of forwarded log", required=True)
args = arguments.parse_args()

# Detect event type or default to informational
eventtype = args.type
if eventtype == "info": eventtype = win32evtlog.EVENTLOG_INFORMATION_TYPE
elif eventtype == "error": eventtype = win32evtlog.EVENTLOG_ERROR_TYPE
elif eventtype == "warning": eventtype = win32evtlog.EVENTLOG_WARNING_TYPE
else: eventtype = win32evtlog.EVENTLOG_INFORMATION_TYPE

# Setup log
applicationName = args.application # "EventForwarder"
eventID = args.eventid #1
category = args.category #5	# Shell
myType = eventtype #win32evtlog.EVENTLOG_INFORMATION_TYPE
descr = [args.logtitle, args.rawlog] #["Raw Log", "HERE IS MY RAW LOG HERE IS MY RAW LOG HERE IS MY RAW LOG HERE IS MY RAW LOG HERE IS MY RAW LOG HERE IS MY RAW LOG HERE IS MY RAW LOG HERE IS MY RAW LOG HERE IS MY RAW LOG "]
data =  str(descr).encode("ascii") #"Application\0Data".encode("ascii")

# Log event
win32evtlogutil.ReportEvent(applicationName, eventID, eventCategory=category, eventType=myType, strings=descr, data=data, sid=mySid)
