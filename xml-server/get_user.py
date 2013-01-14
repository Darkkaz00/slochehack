# /inscriptions

import sys
import urlparse
import os

dat = sys.argv[1]

fields = urlparse.parse_qs(dat)

# sloche 2003, 2004 utilise /inscriptions et un champ
# special pour mapage
if 'formsname' in fields and fields['formsname'][0] == "affiche":
	os.system("python update_user.py '%s'" % dat)

# sloche 2003, 2004 utilise /inscriptions et un champ
# special pour les inscriptions
if 'op' in fields and fields['op'][0] == "save":
	os.system("python new_user.py '%s'" % dat)
	sys.exit(0)

username = fields['username'][0]
passwd = fields['password'][0]

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

	if passwd == correct_passwd:
		fiche = '&status=admin& &sn=UmFuZG9tSVZv7UmKg3plxW97fXdAeZiw3t3DBMwCeRYE%2Fc0QoiDUgEjFkv%2F7N%2BvEu41%2B8oYWUI43ttaJUBNak5wL%2FpB8cXKWL1gz6O%2BPJyotoWCA24VTymBMRieZhNnKZiddF92HmBx663m5FJ%2B5VKYHmwwTavn%2BuJrm83B5iBL2QNEfEDPDUP7VXIrQRe%2FFMHyzJmEmYEY7ap4gt01%2FIDfxvtNhAtiS&'
		fiche += '&piedcouleur=%s& &blocked=no&' % pc
		fiche += ' &tetecouleur=%s& &uid=926674& &description=%s& &username=%s&' % (tc, desc, username)
		fiche += '&commentaire=%s&&corpscouleur=%s&' % (comm, cc)
		fiche += '&hcorps=2& &corps='+c+'& &sn_mdate=2006-05-20%2017%3A28%3A51& &htete=57&'
		fiche += '&nblogin=15& &lastlogindate=2006%2F05%2F28%2011%3A18%3A52& &xml=true& &ageok=false& &tete='+t+'& &pied='+p+'&'
		fiche += ' &status=actif& &hpied=2& &lastlogintime=1148829532& &sn_cdate=2006-05-20%2009%3A29%3A28& &boqakiri=givonefe& &kickout=0& &nbami=1& &ami0=narrateur&'
		fiche += ' &resultat=ok& '
		fiche += ' &guest=false& '
		#fiche += ' &pouvoir=11,13,41& '
	else:
		fiche = "&erreur=Mauvais mot de passe&"	
	
	print(fiche)

	data.close()
except IOError as e:
	# no such user
	print "&erreur=Cet usager n'existe pas& &resultat=false&"
	x = 0	

