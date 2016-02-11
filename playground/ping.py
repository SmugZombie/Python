import commands

def testPing(host,os):
        if os == "CYGWIN":
                output = commands.getstatusoutput("timeout 1 ping " + host + " -n 1 | grep -E -o 'Received = [0-9]+' | awk {'print $3'}")[1]
        elif os == "LINUX":
                output = commands.getstatusoutput("timeout 1 ping " + host + " -c 1 | grep -E -o '[0-9]+ received' | cut -f1 -d' '")[1]
        elif os == "OSX":
                output = commands.getstatusoutput("timeout 1 ping " + host + " -c 1 | grep -E -o '[0-9]+ received' | cut -f1 -d' '")[1]
        else:
                output = commands.getstatusoutput("echo 0'")[1]
        #output = commands.getstatusoutput('ping '+host)
        if str(output) != "1":
                output = "0";
        return output

def getOS():
        output = commands.getstatusoutput('uname')[1]
        if output.find("CYGWIN") != -1:
                output = "CYGWIN"
        elif output.find("Linux") != -1:
                output = "LINUX"
        elif output.find("Darwin") != -1:
                output = "OSX"
        return output

print testPing("soc4", getOS())
