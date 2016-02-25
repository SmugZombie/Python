#!/usr/bin/env python
import os
process_name= "foobot.py" # change this to the name of your process

tmp = os.popen("ps -Af").read()

if process_name not in tmp[:]:
    print "The process is not running. Let's restart."
    """"Use nohup to make sure it runs like a daemon"""
    newprocess="nohup python %s &amp;" % (process_name)
    os.system(newprocess)  
else:
    print "The process is running."
