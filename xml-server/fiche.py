# /inscriptions

import sys
import urlparse
import os

dat = sys.argv[1]

fields = urlparse.parse_qs(dat)

if fields['type'][0] == 'usagers':
	username = fields['valeur'][0]

	try:
		data = open("users/" + username, "r")
		correct_passwd = data.readline().strip()
		tc = data.readline().strip()
		cc = data.readline().strip()
		pc = data.readline().strip()
		desc = data.readline().strip()
		comm = data.readline().strip()
		c = data.readline().strip()
		t = data.readline().strip()
		p = data.readline().strip()	

		print "&username1=%s& " % username
		print "&description1=%s& " % desc
		print "&commentaire1=%s& " % comm
	
		data.close()
	except IOError as e:
		x = 123



		
