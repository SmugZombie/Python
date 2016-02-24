# sort.py
# Used to sort freshly downloaded files
# SmugZombie - github.com/Smugzombie

import argparse
import os;
import commands;

files = os.listdir("/home/Media")
ignored = ['Backups','Games','Movies','Music','P90X','Pictures','Programs','sort.py','Torrents','Tv Shows']

arguments = argparse.ArgumentParser()
arguments.add_argument('--type','-t', help="Type of Files in Batch", required=True)
args = arguments.parse_args()

type = args.type
count = 0
if type != "show" and type != "movie":
	print "Invalid file type!"
	exit()

elif type == "show":
	directory="Tv\ Shows"
else:
	directory="Movies"

print "Processing "+directory

for file in files:
	if file not in ignored:
		file = file.replace(' ', '\ ')
		count += 1
		print "Moving "+file+" to: "+directory
		output = commands.getstatusoutput('mv '+file+' '+directory)[0]
		if str(output) != 1:		
			print "File: "+file+" Failed To Transfer Properly."
print str(count)+" Files Processed"
