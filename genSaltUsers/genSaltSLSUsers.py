#!/usr/bin/python
# genUsers.py
# Creates a salt .sls file for adding users to remote machines
# ron.egli@tvrms.com

version="0.0.6"

import commands, json, datetime, crypt, os.path
from os import urandom

### Global Variables ###

users = {} # Create a JSON Object for users
outfile="users_"+str(datetime.date.today())+".sls"
output = "" # Create a placeholder for generated output
passwordHash = ""
template = """XXXUSERXXX:
 user.present:
  - fullname: XXXNAMEXXX
  - home: /home/XXXUSERXXX
  - password: XXXPASSXXX
  - groups:
    - sudo

"""

#### Functions ####
# Check to make sure the required PHP file is present
def checkRequirements():
        return os.path.isfile('ldap.php')

# Run the php file and try to parse the json that should be returned
def getUsers():
        global users;
        # Get the users json from the ldap.php script
        output = commands.getstatusoutput('/usr/bin/php ldap.php')[1]
        # Try to parse the output, If cannot kill the script
        try: users = json.loads(output);
        except: print "Uhoh, Unable to parse output."; exit();

# Scan all users
def searchGroup():
        global output
        # Loop through all users
        for x in xrange(len(users)):
                # Get all users that are a "security_engineer" or "manager"
                if users[x]['gidnumber'] == "500" or users[x]['gidnumber'] == "506":
                        # Fetch User Information
                        username = users[x]['uid'];  fullname = users[x]['cn']
                        # Pull a fresh copy of the template and modify it, then add it to the output
                        output += template.replace("XXXUSERXXX",username).replace("XXXNAMEXXX",fullname).replace("XXXPASSXXX
",passwordHash)

def saveOutput():
        # Try to write output to file
        try: file = open(outfile, 'w'); file.write(output);
        # If cannot, alert the user and provide the output anyway
        except:
                print "Unable to write to file!"
                print "Here is the file anyway..."
                print output
        # If success, tell the user which file to look for
        else:
                print "File "+outfile+" written successfully."

# Generate a Temporary Password
def generatePassword():
        length = 8
        chars = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
        return "".join([chars[ord(c) % len(chars)] for c in urandom(length)])

# Generate a Random hash to create a password hash against
def generateRandomHash():
        length = 5
        chars = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
        return "".join([chars[ord(c) % len(chars)] for c in urandom(length)])

# Generate a password hash to be placed in the sls file
def hashPassword(password, randomhash):
        global passwordHash, output
        # Has the password
        passwordHash = crypt.crypt(password, "$1$"+randomhash)
        # Print out the Temporary Password for the user running the script
        print "Temporary Password:", password
        # Place the Temporary Password as a comment on the top line of the sls fiel
        output += "# "+str(password)
        output += """
""" # New Line

### Main ###
# If requirements exist, run script
if checkRequirements() is True:
        hashPassword(generatePassword(),generateRandomHash())
        getUsers()
        searchGroup()
        saveOutput()
# Otherwise ask for requirements
else:
        print "Missing Requirements: Please ensure ldap.php is in the same directory and named properly."
