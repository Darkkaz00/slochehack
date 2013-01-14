import sys

def getuser(nam):

	username = nam

	try:
		data = open("users/" + username, "r")
		passwd = data.readline().strip()
		tc = data.readline().strip()
		cc = data.readline().strip()
		pc = data.readline().strip()
		desc = data.readline().strip()
		comm = data.readline().strip()
		c = data.readline().strip()
		t = data.readline().strip()
		p = data.readline().strip()
		
		return (t, c, p, tc, cc, pc)
		data.close()
	except IOError as e:
		return


