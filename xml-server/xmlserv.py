# TODO: eventify ? (instead of thread-per-client)

import socket
import thread
import urllib
import select
import random
from roommove import *
from getuserapi import *
import time
import amis_api
import stockage_messagiel_api

MAX_USERS = 1024

# tableaux et fonctions messagiel
unames_messagiel = ["" for i in range(MAX_USERS)]
queue_messagiel = [[] for i in range(MAX_USERS)]

def chiffre_dans_messagiel(unam):
	for i in range(MAX_USERS):
		if unames_messagiel[i] == unam:
			return i
	return None

def find_free_id_messagiel():
	for i in range(MAX_USERS):
		if unames_messagiel[i] == "":
			return i
	return -1

# salles prive'es ...
id_salle_libre = [True for i in range(1000)]
nom_salle = ["" for i in range(1000)]
prop_salle = ["" for i in range(1000)]
req_sp = [[] for i in range(MAX_USERS)]

def chiffre_salle():
	for i in range(1000):
		if id_salle_libre[i]:
			id_salle_libre[i] = False
			return i
	return None

def efr(n):
	if n >= 1000:
		return 1000 - n
	else:
		return n

# mouches, grenouille, barbu, rapitissateur, roi et reine
pouvoirs_attaques = [13, 14, 22, 25, 27]
# laser, pet, gzzzit
pouvoirs_attaques_2 = [12, 31, 40]

true = True
false = False

# pouvoirs actifs
pouvoirs = [[] for i in range(MAX_USERS)]

# mode ultra
ultra = [0 for i in range(MAX_USERS)]

# mode partie (pouvoir sans-membres)
partie = [0 for i in range(MAX_USERS)]

# king ?
king = [0 for i in range(MAX_USERS)]

chrono = [[0 for i in range(100)] for i in range(MAX_USERS)]

def reset_pouvoirs(id):
	pouvoirs[id] = []
	ultra[id] = 0
	partie[id] = 0
	king[id] = 0
	for i in range(100):
		chrono[id][i] = 0

def active_pouvoir(id, pv):
	if pv in pouvoirs_attaques_2:
		return

	if pv not in pouvoirs[id]:
		pouvoirs[id].append(pv)
		if pv in pouvoirs_attaques:
			
			#print "chrono start %d: %d" % (id, pv)
			chrono[id][pv] = time.time() + 30
			#print pouvoirs[id]

def desactive_pouvoir(id, pv):
	if pv in pouvoirs[id]:
		pouvoirs[id].remove(pv)

def chaine_pouvoirs(id):
	return ",".join([str(k) for k in pouvoirs[id]])

def chaine_ultra(id):
	if ultra[id] > 0:
		return str(ultra[id])
	else:
		return ""

def chaine_partie(id):
	if partie[id] > 0:
		return str(partie[id] - 1)
	else:
		return ""

def chaine_king(id):
	if king[id] > 0:
		return str(king[id])
	else:
		return ""

# people in a given room
rpeople = [[] for i in range(2000)]

# id -> username lookup
unames = ["" for i in range(MAX_USERS)]

# message queues
mq = [[] for i in range(MAX_USERS)]

user_x = [0 for i in range(MAX_USERS)]
user_y = [0 for i in range(MAX_USERS)]

# broadcast message to all message-queues
def broadcast(msg, room):
	for i in range(MAX_USERS):
		if unames[i] != "" and i in rpeople[room]:
			mq[i].append(msg)

def find_free_id():
	for i in range(MAX_USERS):
		if unames[i] == "":
			return i
	return -1

def nombre():
	n = 0
	for i in range(MAX_USERS):
		if unames[i] != "":
			n += 1
	return n

def chiffre_user(unam):
	for i in range(MAX_USERS):
		if unames[i] == unam:
			return i
	return None

def fix_real(room):
	broadcast('<MESSAGE TYPE="BE"><ETAT>1</ETAT><FROM>%s</FROM><TO>%s</TO><EFFET>%s</EFFET><PARAM>1</PARAM></MESSAGE>' % ("real", "real", "41"), room)

def docteur_liposuccion(room, who):
	broadcast('<MESSAGE TYPE="DL"><TARGET>%s</TARGET></MESSAGE>' % unames[who], room)

def leave_room(room, person):
	broadcast('<MESSAGE TYPE="BK"><USERNAME>%s</USERNAME></MESSAGE>"' % unames[person], room)

def description_salle(room, update=False, new_people=[]):
	if update:
		mes = '<MESSAGE TYPE="ER" VALUE="update"><RID VALUE="update">%d</RID>' % efr(room)
		who = new_people
	else:
		mes = '<MESSAGE TYPE="ER"><RID>%d</RID>' % efr(room)
		who = rpeople[room]
	
	realcheck = 0

	for person in who:
		t = c = p = "1"
		tc = cc = pc = "0"
		if unames[person] == "real":
			realcheck = 1

		if getuser(unames[person]):
			t, c, p, tc, cc, pc = getuser(unames[person])
		else:
			t, c, p, tc, cc, pc = getuser("guest")
		mes += '<CARAC VALUE="%s">' % unames[person]
		mes += '<TETE>%s</TETE>' % t
		mes += '<CORPS>%s</CORPS>' % c
		mes += '<PIED>%s</PIED>' % p
		mes += '<TETECOULEUR>%s</TETECOULEUR>' % tc
		mes += '<CORPSCOULEUR>%s</CORPSCOULEUR>' % cc
		mes += '<PIEDCOULEUR>%s</PIEDCOULEUR>' % pc
		mes += '<POUVOIR>%s</POUVOIR>' % chaine_pouvoirs(person)
		mes += '<PARTIE>%s</PARTIE>' % chaine_partie(person)
		mes += '<ULTRA>%s</ULTRA>' % chaine_ultra(person)
		mes += '<KING>%s</KING>' % chaine_king(person)
		mes += '<X>%d</X><Y>%d</Y><ID>%d</ID>' % (user_x[person], user_y[person], person)
		if getuser(unames[person]):
			mes += '<GUEST>false</GUEST>'
		else:
			mes += '<GUEST>true</GUEST>'
		mes += '</CARAC>'
	mes += '</MESSAGE>'


	if realcheck:
		fix_real(room)

	return mes

def update_room(room, person):
	print "Adding person %d to room %d" % (person, room)
	mes = description_salle(room, True, [person])

	# broadcast to all the people in the room
	broadcast(mes, room)

	if unames[person] == "real":
		fix_real(room)

def serve_client(conn, addr, id):
	# Ah, ce cher langage Python
	global nom_salle
	global prop_salle
	global acc_salle
	global id_salle_libre

	# Effacer messages laisses derriere par dernier
	# usager ayant eu ce chiffre de thread
	mq[id] = []

	client_host, client_port = addr
	print "xmlserv: branchement depuis. %s:%s. lancement du thread %d" % (client_host, client_port, id)

	init = time.time()
	ready = select.select([conn], [], [], 0.01)
	if ready[0]:
		req = conn.recv(1024)
		#print "r: %s" % req
		#print "policy-file-request" in req
		if "policy-file-request" in req:
			
			#print "policy file"
			conn.sendall("<?xml version=\"1.0\"?><cross-domain-policy><allow-access-from domain=\"*\" to-ports=\"9100,9200\" /></cross-domain-policy>" + '\0')
			conn.close()
			return

	conn.sendall("<MESSAGE TYPE=\"ACK\"></MESSAGE>" + '\0')
	#print "xmlserv: ACK %s:%s" % (client_host, client_port)

	# Initial room request
	# <MESSAGE TYPE="RR" FROM="laplante"><RID>23</RID><DI>droite</DI><NOM>laplante</NOM><GUEST>false</GUEST></MESSAGE>
	req = conn.recv(1024)
	if req.find('TYPE="RR"') < 0:
		print "xmlserv: expected room request from %s:%s; got %s. Closing connection." % (client_host, client_port, req)
		conn.close()
		return
	username = req[req.find("<NOM>")+5:req.find("</NOM>")]
	if username in unames:
		print "xmlserv: %s:%s: connection with already logged-in username %s refused" % (client_host, client_port, username)
		conn.close()
		return

	# Avertir entree aux amis sur messagiel
	for i in range(MAX_USERS):
		if i != id:
			relai = '<MESSAGE TYPE="enter"><USERNAME>%s</USERNAME></MESSAGE>' % username
			mq[i].append(relai)

	unames[id] = username
	room = int(req[req.find("<RID>")+5:req.find("</RID>")])
	rpeople[room].append(id)

	reset_pouvoirs(id)

	user_x[id] = random.randrange(300, 400)
	user_y[id] = random.randrange(300, 400)

	update_room(room, id)

	mes = description_salle(room)
	conn.sendall(mes.strip() + '\0')

	conn.setblocking(0)

	while 1:
		for pv in range(100):
			if chrono[id][pv] != 0 and chrono[id][pv] < time.time():
				
				#print "%s: %d expire" % (unames[id], pv)
				chrono[id][pv] = 0
				desactive_pouvoir(id, pv)
				# <MESSAGE TYPE="BE"><ETAT>123</ETAT><FROM>user</FROM><TO>user</TO>
				# <EFFET>123</EFFET><PARAM>blabla</PARAM></MESSAGE>

				stop_sortilege = '<MESSAGE TYPE="BE" FROM="SimpleChat"><ETAT>0</ETAT>'
				stop_sortilege += '<FROM>%s</FROM><TO>%s</TO>' % (username, username)
				stop_sortilege += '<EFFET>%d</EFFET><PARAM></PARAM></MESSAGE>' % pv
				broadcast(stop_sortilege, room)

		ready = select.select([conn], [], [], 0.01)
		if ready[0]:
			data = conn.recv(1024)
			if not data: break
			#print ("%s:%s: %s" % (client_host, client_port, data)).strip()
	
			# broadcast client's move and emotion messages as-is
			if data.find('TYPE="BST"') > 0 or data.find('TYPE="BM"') > 0 or data.find('TYPE="BE"') > 0:
				
				#print data

				# pouvoirs
				if data.find('<PV>') > 0:
					sta = int(data[data.find("<ETAT>")+6:data.find("</ETAT>")])
					pv = int(data[data.find("<PV>")+4:data.find("</PV>")])
					param_str = data[data.find("<PARAM>")+7:data.find("</PARAM>")]
					if not param_str.isdigit():
						param = 0
					else:
						param = int(param_str)
	
					if pv not in pouvoirs_attaques:
						if sta == 1:
							active_pouvoir(id, pv)			
						elif sta == 0:
							desactive_pouvoir(id, pv)

					# chrono attaques
					if pv in pouvoirs_attaques and sta == 1:
						to = data[data.find("<TO>")+4:data.find("</TO>")]
						targ = -1
						for i in range(len(unames)):
							if unames[i] == to:
								targ = i
						if targ >= 0:
							active_pouvoir(targ, pv)

					# la scie
					if pv == 21:
						if sta == 1:
							partie[id] = param + 1			
						else:
							partie[id] = 0
				
					# ultra
					if pv == 33:
						if sta == 1:
							ultra[id] = param
						else:
							ultra[id] = 0
				
				broadcast(data, room)

			# broadcast visibility
			if data.find('TYPE="BV"') > 0:
				sta = int(data[data.find("<ST>")+4:data.find("</ST>")])
				if sta == 0:
					broadcast('<MESSAGE TYPE="BV"><USERNAME>%s</USERNAME><ST>%d</ST></MESSAGE>' % (username, sta), room)
				elif sta == 1:
					# update avatar
					leave_room(room, id)
					update_room(room, id)

			# obtenir la liste des rooms prive'es.
			# De'clenche' en marchant sur la grosse bosse
			# ou en cliquant sur 'raifrai^chir'.
			if data.find('TYPE="LR"') > 0:
				rep = '<MESSAGE TYPE="LR">'
				effaces = 0
				for i in range(1000):
					if not id_salle_libre[i]:
						if len(rpeople[1000 + i]) == 0:
							id_salle_libre[i] = True
							#print "effacement de la salle %s (numero %d, tableau %d)" % (nom_salle[i], i, 1000 + i)
									
				for i in range(1000):
					if not id_salle_libre[i]:
						pop_salle = len(rpeople[1000 + i])

						# Les salles dont on est soi-meme proprietaire
						# doivent apparaitre en vert en ne demandent
						# pas de requete d'access.
						#
						# Remarque: devrait-on memoriser les autorisations
						# d'acces de telle sorte qu'une fois permis a entrer
						# dans une salle donnee, il ne faut plus demander
						# la permission au proprio ?
						if username == prop_salle[i]:
							acc_check = "ok"
						else:
							acc_check = "nok"

						rep += '<RP>'
						rep += '<ID>%d</ID>' % -i
						rep += '<NAME>%s</NAME>' % nom_salle[i]
						rep += '<UNAM>%s</UNAM>' % prop_salle[i]
						rep += '<NOMBRE>%d</NOMBRE>' % pop_salle
						rep += '<ACCESS>%s</ACCESS>' % acc_check
						rep += '</RP>'
				rep += '</MESSAGE>'
				conn.sendall(rep.strip() + '\0')
				#print 'reponse LR: %s' % rep

			# demander acces a aune room privee
			if data.find('TYPE="RP"') > 0:
				rp_id = int(data[data.find("<ID>")+4:data.find("</ID>")])
				rp_raison = data[data.find("<RAISON>")+8:data.find("</RAISON>")]
	
				relai = '<MESSAGE TYPE="RP">'
				relai += '<ID>%d</ID>' % rp_id
				relai += '<USERNAME>%s</USERNAME>' % username
				relai += '<RAISON>%s</RAISON>' % rp_raison
				relai += '</MESSAGE>'

				# je stocke les ID en nombres positifs dans mes tableaux...
				if rp_id < 0:
					rp_id = -rp_id
				id_prop = chiffre_user(prop_salle[int(rp_id)])
				if id_prop != None:
					req_sp[id_prop].append(username)
					mq[id_prop].append(relai)

			# autoriser / refuser acces a room privee
			if data.find('TYPE="AC"') > 0:
				ac_s = data[data.find("<S>")+3:data.find("</S>")]
				ac_id = data[data.find("<ID>")+4:data.find("</ID>")]
					
				relai = '<MESSAGE TYPE="AC">'
				relai += '<S>%s</S>' % ac_s
				relai += '<BOF>mettons</BOF>'
				relai += '<ID>%s</ID>' % ac_id
				relai += '</MESSAGE>'

				if len(req_sp[id]) > 0:
					id_dest = chiffre_user(req_sp[id].pop())
					#print "relai AC: %s" % relai
					mq[id_dest].append(relai)
				

			# cre'er room prive'e
			if data.find('TYPE="CR"') > 0:
				cr_ok = True
				ce_prop = data[data.find("<NOM>")+5:data.find("</NOM>")]
				cette_salle = data[data.find("<DESC>")+6:data.find("</DESC>")]
				rep = '<MESSAGE TYPE="CR">'

				# meme salle et meme proprietare existent deja ?
				for i in range(1000):
					if nom_salle[i] == cette_salle:
						if prop_salle[i] == ce_prop:
							if not id_salle_libre[i]:
								
								#print "conflit salle existante: %s" % cette_salle
								cr_ok = False

				if cr_ok:
					numero_rp = chiffre_salle()
					nom_salle[numero_rp] = cette_salle
					prop_salle[numero_rp] = ce_prop
					rep += '<STATUS>OK</STATUS>'
					rep += '<ID>%d</ID>' % -numero_rp
					rep += '<USERNAME>%s</USERNAME>' % ce_prop
					rep += '<ROOMNAME>%s</ROOMNAME>' % cette_salle
				else:
					rep += '<STATUS>NOK</STATUS>'

				rep += '</MESSAGE>'

				conn.sendall(rep.strip() + '\0')
				#print 'reponse CR: %s' % rep

			# SR -- requete entree room privee
			if data.find('TYPE="SR"') > 0:
				sr_ok = True
				id_salle = int(data[data.find("<ID>")+4:data.find("</ID>")])

				# la reponse serveur SR, ca ne fait qu'ajouter une
				# banderole dans le GUI du client, mais ca semble
				# necessaire.
				rep = '<MESSAGE TYPE="SR" FROM="SimpleChat">'
				rep += '<STATUS>OK</STATUS>'	# NOK pour refuser entree...
				rep += '</MESSAGE>'
				conn.sendall(rep.strip() + '\0')
				#print 'reponse SR: %s' % rep

				# maintenant, le changement de salle a proprement parler

				#print "%s entre dans la salle privee numero %d" % (username, id_salle)
				nr = 1000 - id_salle
				#print "chiffre tableau: %d" % nr
				rpeople[room].remove(id)
				rpeople[nr].append(id)
				leave_room(room, id)
				update_room(nr, id)
				room = nr

				mes = description_salle(room)
				conn.sendall(mes.strip() + '\0')

			# store coords
			if data.find('TYPE="BM"') > 0:
				user_x[id] = int(data[data.find("<X>")+3:data.find("</X>")])
				user_y[id] = int(data[data.find("<Y>")+3:data.find("</Y>")])

			# relay public messages, route private messages
			if data.find('TYPE="BT"') > 0:
				text = data[data.find("<TEXT>")+6:data.find("</TEXT>")]
				if data.find("PRIVATE") < 0:
					if text.strip() == "%2FNombre":
						broadcast('<MESSAGE TYPE="BT"><TEXT>Il y a %d slocheux sur le chat.</TEXT><USERNAME>%s</USERNAME></MESSAGE>' % (nombre(), username), room)
					else:
						broadcast('<MESSAGE TYPE="BT"><TEXT>%s</TEXT><USERNAME>%s</USERNAME></MESSAGE>' % (text, username), room)
				else:
					who = data[data.find("<ID>")+4:data.find("</ID>")]

					if username == "doclipo" and text.strip() == "l":
						docteur_liposuccion(room, int(who))
					elif username == "laplante" and text.strip() == "kick":
						mq[int(who)].append("kick")
					elif username == "pouvoirs":
						# <MESSAGE TYPE="BE"><ETAT>123</ETAT><FROM>user</FROM><TO>user</TO><EFFET>123</EFFET><PARAM>blabla</PARAM></MESSAGE>
						broadcast('<MESSAGE TYPE="BE"><ETAT>1</ETAT><FROM>%s</FROM><TO>%s</TO><EFFET>%s</EFFET><PARAM>1</PARAM></MESSAGE>' % (unames[int(who)], unames[int(who)], text.strip()), room)
					else:
						mq[int(who)].append('<MESSAGE TYPE="BT" PRIVATE="1"><TEXT PRIVATE="1">%s</TEXT><USERNAME>%s</USERNAME></MESSAGE>' % (text, username))
						mq[id].append('<MESSAGE TYPE="BT" PRIVATE="1"><TEXT PRIVATE="1">%s</TEXT><USERNAME>%s</USERNAME></MESSAGE>' % (text, username))

			# relai liposuccion
			if data.find('TYPE="DL"') > 0:
				docteur_liposuccion(room, id)

			# teleport
			if data.find('TYPE="RR"') > 0 and data.find('<RID>') > 0:
				# hack!
				ref_room = int(data[data.find("<RID>")+5:data.find("</RID>")])
				dir = data[data.find("<DI>")+4:data.find("</DI>")]

				user_x[id] = random.randrange(300, 400)
				user_y[id] = random.randrange(350, 450)

				nr = get_new_room(ref_room, dir, 2000, 2000)

				# entree gzzzit
				if room == 15 and nr == 65:
					user_x[id] = random.randrange(545, 621)
					user_y[id] = random.randrange(479, 512)

				# tuyeau
				if room == 11 and nr == 61:
					user_x[id] = random.randrange(277, 342)
					user_y[id] = random.randrange(407, 458)	

				# sortie salle swompe
				if room == 71 and nr == 61:
					user_x[id] = random.randrange(51, 154)
					user_y[id] = random.randrange(310, 331)

				# entree salle swompe
				if room == 61 and nr == 71:
					user_x[id] = random.randrange(270, 286)
					user_y[id] = random.randrange(320, 353)

				rpeople[room].remove(id)
				rpeople[nr].append(id)
				leave_room(room, id)
				update_room(nr, id)
				room = nr

				mes = description_salle(room)
				conn.sendall(mes.strip() + '\0')

			# room changes
			# <MESSAGE TYPE="RR" FROM="sloche8518"><DI>droite</DI><POS></POS><NOM>sloche8518</NOM><GUEST>true</GUEST></MESSAGE>
			elif data.find('TYPE="RR"') > 0 and data.find("<DI>") > 0:
				dir = data[data.find("<DI>")+4:data.find("</DI>")]
				nr = get_new_room(room, dir, user_x[id], user_y[id])

				if dir == "gauche" and user_x[id] > 100 and room == 15:
					nr = 65

				old_y = user_y[id]

				user_x[id] = random.randrange(300, 400)
				# preserver coordonne Y dans salles swompe
				if not (69 < room < 80):
					if room == 71 and nr == 72:
						user_x[id] = 591
					user_y[id] = random.randrange(350, 450)

				if dir == "droite":
					user_x[id] = random.randrange(56, 110)
				if dir == "gauche":
					user_x[id] = random.randrange(589, 645)
				if dir == "haut":
					user_y[id] = random.randrange(440, 470)
				if dir == "bas":
					user_y[id] = random.randrange(300, 350)

				# escaliers gzzit
				if room == 64 and nr == 63:
					user_x[id] = random.randrange(494, 559)
					user_y[id] = random.randrange(447, 448)

				if nr == 1 and user_y[id] < 349:
					user_y[id] = 349

				if nr == 64 and user_y[id] < 379: user_y[id] = 379
				if nr == 65 and user_y[id] < 339: user_y[id] = 339

				if nr == 61 and room == 11:
					user_x[id] = 282
					user_y[id] = 447

				if nr == 11 and room == 61:
					user_x[id] = 540
					user_y[id] = 322

				if nr == 62:
					
					#print "room 62, adjusting ycoord"
					user_y[id] = 360

				if nr > 71:
					
					#print "y coord club swompe ajust"
					user_y[id] = old_y

				if nr == 53 and user_y[id] < 360:
					user_y[id] = 360

				rpeople[room].remove(id)
				rpeople[nr].append(id)
				leave_room(room, id)
				update_room(nr, id)
				room = nr

				mes = description_salle(room)
				conn.sendall(mes.strip() + '\0')

		# send off queued messages
		while len(mq[id]):
			if mq[id][0].strip() == "kick":
				mq[id] = mq[id][1:]
				broadcast('<MESSAGE TYPE="BT"><TEXT>%s</TEXT><USERNAME>%s</USERNAME></MESSAGE>' % (("%s s'est fait kicker du chat" % username), username), room)
				conn.close()
				rpeople[room].remove(id)
				leave_room(room, id)
				unames[id] = ""
				return
			conn.sendall(mq[id][0].strip() + '\0')
			#print "xmlchat: %s: envoi depuis queue: %s" % (username, mq[id][0])
			mq[id] = mq[id][1:]

	#print "xmlserv: fermeture conn. %s:%s" % (client_host, client_port)
	conn.close()

	# Avertir sortie aux amis sur messagiel
	for i in range(MAX_USERS):
		relai = '<MESSAGE TYPE="quit"><USERNAME>%s</USERNAME></MESSAGE>' % username
		mq[i].append(relai)

	rpeople[room].remove(id)
	leave_room(room, id)
	unames[id] = ""

#####################################################################################

def envoi_ou_stockage(to, relai):
	if chiffre_dans_messagiel(to) != None:
		# Envoyer le message directement
		
		#print "messagiel: envoi direct a %s de '%s'" % (to, relai)
		queue_messagiel[chiffre_dans_messagiel(to)].append(relai)
	else:
		# Stocker le message et l'envoyer lorsque l'usager
		# se branchera au slochepop
		
		#print "messagiel: stockage pour %s de '%s'" % (to, relai)
		stockage_messagiel_api.ajouter(to, relai)

def serve_client_messagiel(conn, addr, id):
	client_host, client_port = addr
	print "messagiel: conn. %s:%s, lancement thread %d" % (client_host, client_port, id)

	queue_messagiel[id] = []

	# Demander au client sloche quel est le nom de l'utilisateur
	# qui vient de se brancher au messagiel.
	conn.sendall('<MESSAGE TYPE="set"><HR FROM="messagiel">abcdef</HR></MESSAGE>' + '\0')

	# S'attendre a une reponse dans le genre de:
	# <MESSAGE TYPE="enter" FROM="Client"><NOM>laplante</NOM><HR>24248</HR></MESSAGE>
	rep = conn.recv(1024)
	if rep.find('TYPE="enter"') < 0:
		print "Expected enter message from %s:%s; got %s. Closing connection." % (client_host, client_port, rep)
		conn.close()
		return
	username = rep[rep.find("<NOM>")+5:rep.find("</NOM>")]
	#print "messagiel: %s:%s -> usager %s" % (client_host, client_port, username)
	for i in range(MAX_USERS):
		if unames_messagiel[id] == username:
			print "deja branche !!!! fermeture de la connection"
			conn.close()
			return

	# Aller chercher la liste d'amis de l'usager
	mes_amis = amis_api.liste_amis(username)
	rep_liste = '<MESSAGE TYPE="ami">'
	for ami in mes_amis:
		# L'ami est-il en ligne ?
		if chiffre_user(ami) != None:
			sta = 1		# oui
		else:
			sta = 0		# non
		rep_liste += '<AMI STATUS="%d">%s</AMI>' % (sta, ami)
	rep_liste += '</MESSAGE>'
	conn.sendall(rep_liste + '\0')

	# S'occuper des vieux messages...
	# Par "messages", j'entends messages XML qui peuvent avoir
	# plusieurs fonctions.
	vieux_messages = stockage_messagiel_api.obtenir_vider_stockage(username)
	for m in vieux_messages:
		conn.sendall(m + '\0')

	unames_messagiel[id] = username

	while True:
		ready = select.select([conn], [], [], 0.01)
		if ready[0]:
			data = conn.recv(1024)

			# Connection morte
			if not data:
				break
			else:
				pass
				#print "messagiel: %s: %s" % (username, data)

			# Requete ami
			if data.find('<OPTION>request</OPTION>') > 0:
				to = data[data.find("<TO>")+4:data.find("</TO>")]
				text = data[data.find("<TEXT>")+6:data.find("</TEXT>")]
				#print "messagiel: %s req ami %s: '%s'" % (username, to, text)

				# relai. marche sur 2007.
				relai = '<MESSAGE TYPE="send">'
				relai += '<TEXT OPTION="request">%s</TEXT>' % text
				relai += '<FROM>%s</FROM>' % username
				relai += '</MESSAGE>'
				id_dest = chiffre_user(to)
				envoi_ou_stockage(to, relai)

			# Ami autorise.
			# <MESSAGE TYPE="send"><NOM>donald</NOM><TO>laplante</TO><TEXT></TEXT>
			# <OPTION>autoriser</OPTION></MESSAGE>
			if data.find('<OPTION>autoriser</OPTION>') > 0:
				nom = data[data.find("<NOM>")+5:data.find("</NOM>")]
				to = data[data.find("<TO>")+4:data.find("</TO>")]
				#print "%s autorise %s a etre son ami" % (nom, to)

				# Stocker nouvel ami dans la BDD
				if nom == username:
					mes_amis = amis_api.liste_amis(nom)
					mes_amis.append(to)
					amis_api.stocker_liste_amis(nom, mes_amis)

					ses_amis = amis_api.liste_amis(to)
					ses_amis.append(nom)
					amis_api.stocker_liste_amis(to, ses_amis)						

				# Envoie la bulle "ami accepte" mais n'ajoute pas
				# l'ami a la liste...
				relai = '<MESSAGE TYPE="send">'
				relai += '<TEXT OPTION="autoriser">%s</TEXT>' % nom
				relai += '<FROM>%s</FROM>' % nom
				relai += '</MESSAGE>'
				envoi_ou_stockage(to, relai)

			# Ami refuse
			if data.find('<OPTION>refus</OPTION>') > 0:
				nom = data[data.find("<NOM>")+5:data.find("</NOM>")]
				to = data[data.find("<TO>")+4:data.find("</TO>")]
				#print "%s refuse a %s le droit d'etre son ami" % (nom, to)			

				# Envoyer la bulle "ami refuse"
				relai = '<MESSAGE TYPE="send">'
				relai += '<TEXT OPTION="refus">%s</TEXT>' % nom
				relai += '<FROM>%s</FROM>' % nom
				relai += '</MESSAGE>'
				envoi_ou_stockage(to, relai)

			# Relai ami
			# <MESSAGE TYPE="ami" FROM="Client"><NOM>donald</NOM><AMI>laplante</AMI></MESSAGE>
			if data.find('TYPE="ami"') > 0:
				#print "relai ami..."
				nom = data[data.find("<NOM>")+5:data.find("</NOM>")]
				ami = data[data.find("<AMI>")+5:data.find("</AMI>")]

				relai = '<MESSAGE TYPE="ami">'
				relai += '<AMI STATUS="1">%s</AMI>' % ami
				relai += '</MESSAGE>'
				envoi_ou_stockage(nom, relai)

			# Supprimer ami
			if data.find('<OPTION>supprimer</OPTION>') > 0:
				to = data[data.find("<TO>")+4:data.find("</TO>")]
				#print "messagiel: %s supprime ami %s" % (username, to)

				# Ce relai marche sur le client 2007
				relai = '<MESSAGE TYPE="send">'
				relai += '<TEXT OPTION="supprimer">%s</TEXT>' % username
				relai += '<FROM>%s</FROM>' % username
				relai += '</MESSAGE>'
				envoi_ou_stockage(to, relai)

				# (de-)stocker cela dans la BDD
				mes_amis = amis_api.liste_amis(username)
				mes_amis.remove(to)
				amis_api.stocker_liste_amis(username, mes_amis)

				ses_amis = amis_api.liste_amis(to)
				ses_amis.remove(username)
				amis_api.stocker_liste_amis(to, ses_amis)		

			# Message slochepop
			if not (data.find('<OPTION>') > 0) and data.find('TYPE="send"') > 0:
				to = data[data.find("<TO>")+4:data.find("</TO>")]
				text = data[data.find("<TEXT>")+6:data.find("</TEXT>")]
				#print "messagiel: %s message a %s: '%s'" % (username, to, text)

				# Ajoute un nouveau message slochepop avec une
				# petite bulle qu'il faut cliquer pour le lire.
				relai = '<MESSAGE TYPE="send">'
				relai += '<TEXT>%s</TEXT>' % text
				relai += '<FROM>%s</FROM>' % username
				relai += '</MESSAGE>'
				envoi_ou_stockage(to, relai)

		# Messages en file (recus d'un autre module ou thread etc.)
		while len(queue_messagiel[id]):
			conn.sendall(queue_messagiel[id][0].strip() + '\0')
			#print "messagiel: %s: envoi depuis queue: %s" % (username, queue_messagiel[id][0])
			queue_messagiel[id] = queue_messagiel[id][1:]

	unames_messagiel[id] = ""
	print "messagiel: fermeture conn. %s:%s" % (client_host, client_port)
	conn.close()

#####################################################################################

# brancher serveur chat et serveur messagiel

host = ''
port = 9100
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
id = 0

host_m = ''
port_m = 9200
s_m = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_m.bind((host_m, port_m))
id_m = 0

check = 0

# on gere les deux sous-serveurs en parallele

def thread_chat(s, derp):
	global check
	print "chat ok"
	check += 1
	s.listen(5)
	while 1:
		conn, addr = s.accept()
		id = find_free_id()
		if id >= 0:
			print "New thread with id %d" % id
			thread.start_new_thread(serve_client, (conn, addr, id))

def thread_messagiel(s_m, derp):
	global check
	print "messagiel ok"
	check += 1
	s_m.listen(5)
	while 1:
		conn, addr = s_m.accept()
		id_m = find_free_id_messagiel()
		if id_m >= 0:
			thread.start_new_thread(serve_client_messagiel, (conn, addr, id_m))
		else:
			print "plus de place !!!"

print "SVP ATTENDRE UN INSTANT AVANT D'UTILISER LE CHAT..."
thread.start_new_thread(thread_chat, (s, 0))
time.sleep(1)
thread.start_new_thread(thread_messagiel, (s_m, 0))
while check != 2:
	pass
print "checks ok"
print "SERVEUR PRET !"

while True:
	pass

