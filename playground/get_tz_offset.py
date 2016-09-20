def get_timezone_offset():
	offset = time.timezone if (time.localtime().tm_isdst == 0) else time.altzone
	return offset / 60 / 60 * -1
