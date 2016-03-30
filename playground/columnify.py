#!/usr/bin/python
# columnify.py
# Creates simple columns
# Ron Egli - github.com/smugzombie

def columnify(string, length):
        stringlen = len(string)
        
        if stringlen < length:
                while stringlen < length:
                        string += " "
                        stringlen = len(string)
        elif stringlen > length:
                while stringlen > length:
                        string = string[:-1]
                        stringlen = len(string)
        return string

print columnify("hello", 10), columnify("helloworldhowareyou", 10), columnify("Hello", 5)
