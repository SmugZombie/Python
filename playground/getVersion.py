import urllib2
import ssl
import re
rawfileurl = "https://raw.githubusercontent.com/SmugZombie/Stooge/master/stooge.py"
data = ""

def post(server, data):
        req = urllib2.Request(server)
        #req.add_header('Content-Type', 'application/json')

        # SSL
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        output = {}
        output['url'] = server
        output['data'] = data

        try:
                response = urllib2.urlopen(req, data, context=ctx)
        except urllib2.HTTPError, err:
                output['code'] = err.code
                output['response'] = ""
                return output
        else:
                output['code'] = response.getcode()
                output['response'] = response.read()
        return output

download = str(post(rawfileurl, data))

#import re
#p = re.compile(ur'(?P<title>Version\ )(?P<version>.{1,3}..{1,3}..{1,3})')
p = re.compile(ur'(?P<title>Version\ )(?P<version>.{1,3}..{1,3}..{1,3})(\\n)')
#test_str = u" Version 0.6.1"

print re.search(p, download).group(2)
