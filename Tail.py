# Tail.py
# A simple file tailer
# Ron Egli - github.com/smugzombie
# 0.1

import sys

try:
	file = sys.argv[1]
except:
	print "Invalid File Provided"
	hello = raw_input()
	exit()

try:
	f = open(file)
except:
	print "Unable to open provided file: " + str(file)
	hello = raw_input()
	exit()

p = 0
while True:
    f.seek(p)
    latest_data = f.read()
    p = f.tell()
    if latest_data:
        print latest_data
        #print str(p).center(10).center(80, '=')
