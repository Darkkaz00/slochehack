# (mapage.sn)

import os.path
import os
import sys
import urlparse

dat = sys.argv[1]

fields = urlparse.parse_qs(dat)

username = fields['username'][0]
t = fields['tete'][0]
c = fields['corps'][0]
p = fields['pied'][0]
tc = fields['tetecouleur'][0]
cc = fields['corpscouleur'][0]
pc = fields['piedcouleur'][0]
try:
	desc = fields['description'][0]
except KeyError:
	desc = ""

try:
	comm = fields['commentaire'][0]
except KeyError:
	comm = ""

if 1:
	data = open("users/" + username, "r")
	passwd = data.readline().strip()
	data.close()

	os.remove("users/" + username)

	data = open("users/" + username, "w")
	data.write(passwd + '\n')
	data.write(tc + '\n')
	data.write(cc + '\n')
	data.write(pc + '\n')
	data.write(desc + '\n')
	data.write(comm + '\n')
	data.write(c + '\n')
	data.write(t + '\n')
	data.write(p + '\n')
	data.close()

	print " "
	print dat+" &resultat=1& &success=1&"
	print ""
