#!/usr/bin/env python
# file: grep.py
import re, sys

def grep(s,pattern):
    return '\n'.join(re.findall(r'^.*%s.*?$'%pattern,s,flags=re.M))

if __name__ == '__main__':
    print (grep(sys.stdin.read(),sys.argv[1]))
