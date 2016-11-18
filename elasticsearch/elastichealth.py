#/usr/bin/python
# ElasticHealth.py
# Purpose: Curls and parses the shard sizes for
# an elasticsearch cluster, then calculates how much space is used
# Author: Ron Egli (ron.egli@tvrms.com)
# Version: 1.1

# Imports
import requests, json, sys

# User Defined Variables
totalHosts=3
totalStorage="100gb"

# Static Variables
totalUsage=float(0)

try:
        cluster = sys.argv[1]
except:
        cluster = "<Insert your es url here with no trailing / >"

def queryES():
        url = cluster+"/_cat/shards"
        querystring = {"v":""}
        payload = ""
        headers = {'cache-control': "no-cache"}
        response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
        return response.text

def parseES(data):
        global totalUsage
        for line in data.splitlines():
                awk = line.split()
                size = downconvertSize(awk[5])
                totalUsage += float(size)

def downconvertSize(size):
        if "kb" in size:
                return float(size[:-2]) * 1000
        elif "mb" in size:
                return float(size[:-2]) * 1000000
        elif "gb" in size:
                return float(size[:-2]) * 1000000000
        elif "b" in size:
                return float(size[:-1])
        else:
                return 0

def calculateUsage():
        return str(round(totalUsage / totalHosts / 1000000000, 2))+"gb", str(totalUsage / totalHosts)

def calculateFree():
        return str(round((downconvertSize(totalStorage) - float(calculateUsage()[1])) / 1000000000))+"gb"

# MAIN
parseES(queryES())

# Output
usage = {}
usage['used'] = calculateUsage()[0]
usage['free'] = calculateFree()

print json.dumps(usage)
