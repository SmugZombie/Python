#counter = 0
#proceed = False
#while proceed is False:
#	if counter == 10:
#		proceed = True
#	else:
#		print counter
#		counter += 1
#print "Done"

#proceed = False
#while proceed is False:
#	print "Do you want to continue?"
#	answer = raw_input()
#	if answer == "y":
#		proceed = False
#	elif answer == "n":
#		proceed = True
#print "Done"

proceed = False
while proceed is False:
	print "Enter a valid hostname:"
	hostname = raw_input()
	print "Do you wish to continue with", hostname,"? (Y/N)"
	answer = raw_input()
	if answer == "y" or answer == "Y":
		proceed = True

proceed = False
while proceed is False:
	print "Enter the standard username for ", hostname
	username = raw_input()
	print "Is",username,"correct? (Y/N)"
	answer = raw_input()
	if answer == "y" or answer == "Y":
		proceed = True

proceed = False
while proceed is False:
        print "Enter the sudo username for ", hostname
        sudousername = raw_input()
        print "Is",sudousername,"correct? (Y/N)"
        answer = raw_input()
        if answer == "y" or answer == "Y":
                proceed = True


print "So far we have"
print "Hostname:", hostname
print "User    :", username
print "SudoUser:", sudousername
