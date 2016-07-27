import requests, json, argparse

auth_email = ""
auth_key = ""

def createDNSRecord(domain, record, host, content):
	zone_id = getZoneId(domain)
	url = "https://api.cloudflare.com/client/v4/zones/" + str(zone_id) + "/dns_records"
	payload = "{\"type\":\"" + str(record) + "\",\"name\":\"" + str(host) + "." + str(domain) + "\",\"content\":\"" + str(content) + "\",\"ttl\":120}"
	headers = { 'x-auth-email': auth_email, 'x-auth-key': auth_key, 'content-type': "application/json", 'cache-control': "no-cache" }
	response = requests.request("POST", url, data=payload, headers=headers)
	print(response.text)

def listDNSRecords(domain):
	zone_id = getZoneId(domain)
	url = "https://api.cloudflare.com/client/v4/zones/" + str(zone_id) + "/dns_records" 
	headers = { 'x-auth-email': auth_email, 'x-auth-key': auth_key, 'content-type': "application/json", 'cache-control': "no-cache" }
	response = requests.request("GET", url, headers=headers)
	
	try:
		data = json.loads(response.text)
	except:
		print "Uhoh - List DNS Records"

	dns_records = {}
	for x in xrange(len(data['result'])):
		record = data['result'][x]
		record_id = len(dns_records)
		dns_records[record_id] = {}
		dns_records[record_id]['type'] = record['type']
		dns_records[record_id]['name'] = record['name']
		dns_records[record_id]['content'] = record['content']

	return json.dumps(dns_records, sort_keys=True, indent=4, separators=(',', ': '))


def getZoneId(domain):
	url = "https://api.cloudflare.com/client/v4/zones/?name=" + str(domain)
	headers = { 'x-auth-email': auth_email, 'x-auth-key': auth_key, 'content-type': "application/json", 'cache-control': "no-cache" }
	response = requests.request("GET", url, headers=headers)

	try:
		data = json.loads(response.text)
	except:
		print "Uhoh"

	return data['result'][0]['id']

########### MAIN ###########

arguments = argparse.ArgumentParser()
arguments.add_argument('--domain','-d', help="Domain name to perform an action on", required=True)
arguments.add_argument('--action','-a', help="Domain name to perform an action on", required=False, default="list")
arguments.add_argument('--content','-c', help="Domain name to perform an action on", required=False, default="")
arguments.add_argument('--record','-r', help="Domain name to perform an action on", required=False, default="")
arguments.add_argument('--host','-H', help="Domain name to perform an action on", required=False, default="")
args = arguments.parse_args()
domain = args.domain
action = args.action
record = args.record
content = args.content
host = args.host

if action == "list":
	print listDNSRecords(domain)

if action == "add":
	if record == "" or content == "" or host == "":
		print "Missing Arguments. Required: -r RECORD -H HOST -c CONTENT"
		exit()
	else:
		print createDNSRecord(domain, record, host, content)
