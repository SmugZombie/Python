#/usr/bin/python
# ElasticStorage.py
# Purpose: Curls and parses current node sizes
# Author: Ron Egli (ron.egli@tvrms.com)
# Version: 1.0

# Imports
import requests, json, sys

# Static Variables
totalUsage=float(0)

try:
        cluster = sys.argv[1]
except:
        cluster = "<YOUR ES CLUSTER URL HERE NO TRAILING / >"

def queryES():
        url = cluster+"/_nodes/stats"
        querystring = {"v":""}
        payload = ""
        headers = {'cache-control': "no-cache"}
        response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
        return json.loads(response.text)

def upconvertbytestogigs(size):
        return round(size / 1000000000, 2)
        
# MAIN
response = queryES()

nodes = response['nodes']
count = 0
output = {}
for node in nodes:
        totalSize = upconvertbytestogigs(nodes[node]['fs']['total']['total_in_bytes'])
        availableSize = upconvertbytestogigs(nodes[node]['fs']['total']['free_in_bytes'])
        usedSize = totalSize - availableSize
        output[count] = {}
        output[count]['name'] = nodes[node]['name']
        output[count]['avail'] = availableSize
        output[count]['used'] = usedSize
        output[count]['total'] = totalSize
        #print nodes[node]['name'] + " - Free: " +  str(availableSize) + "GB - Used: " + str(usedSize) + "GB"
        count = count + 1

output['count'] = count
print json.dumps(output)
