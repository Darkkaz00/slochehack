# sloche 2007
# (inscriptions.sn)

import os.path
import sys
import urlparse

def do_new_user(dat):
	fields = urlparse.parse_qs(dat)

	username = fields['username'][0]
	passwd = fields['password'][0]
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
	
	if not os.path.isfile("users/" + username):
		# user not registed yet; good !
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

		# pas trouve mieux pour que ca
		# marche sur presque toutes les versions :(
		print " &erreur=Inscription reussie& &resultat=0& "
	else:
		print " &erreur=Usager existe deja& &resultat=0& "

# fichier seul
if __name__ == "__main__":	
	do_new_user(sys.argv[1])
