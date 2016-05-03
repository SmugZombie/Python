#!/usr/bin/python

import pwd
import grp
import os

user = "www-data"

uid = pwd.getpwnam(user).pw_uid
gid = grp.getgrnam(user).gr_gid

print uid
print gid

path="test.text"

os.chown(path, uid, gid)
