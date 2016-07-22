# Tail.py
# A simple file tailer
# Ron Egli - github.com/smugzombie
# 0.3

import sys

def tail( f, lines=20 ):
    total_lines_wanted = lines

    BLOCK_SIZE = 1024
    f.seek(0, 2)
    block_end_byte = f.tell()
    lines_to_go = total_lines_wanted
    block_number = -1
    blocks = [] # blocks of size BLOCK_SIZE, in reverse order starting
                # from the end of the file
    while lines_to_go > 0 and block_end_byte > 0:
        if (block_end_byte - BLOCK_SIZE > 0):
            # read the last block we haven't yet read
            f.seek(block_number*BLOCK_SIZE, 2)
            blocks.append(f.read(BLOCK_SIZE))
        else:
            # file too small, start from begining
            f.seek(0,0)
            # only read what was not read
            blocks.append(f.read(block_end_byte))
        lines_found = blocks[-1].count('\n')
        lines_to_go -= lines_found
        block_end_byte -= BLOCK_SIZE
        block_number -= 1
    all_read_text = ''.join(reversed(blocks))
    return '\n'.join(all_read_text.splitlines()[-total_lines_wanted:])

try:
	file = sys.argv[1]
except:
	print "Invalid File Provided"
	hello = raw_input()
	exit()

try:
	num_lines = sum(1 for line in open(file))
	f = open(file)
except:
	print "Unable to open provided file: " + str(file)
	hello = raw_input()
	exit()


lastline = ""

print tail(f,20)
lastline = tail(f,1)
while True:
    newline = tail(f, 1)
    if newline != lastline:
        print newline
        lastline = newline
