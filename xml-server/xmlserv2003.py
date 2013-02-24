# XML server for 2003 client.
# All the message names are explicit and casedLikeThis,
# their parameters are also very explicit. (in 2004 and later
# servers, acronyms and shorthands are used).
# All the swompe special stuff, as well as doclipo, 
# is of course missing.

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

true = True
false = False

# people in a given room
rpeople = [[] for i in range(100)]

# id -> username lookup
unames = ["" for i in range(MAX_USERS)]

# message queues
mq = [[] for i in range(MAX_USERS)]

def chiffre_user(unam):
	for i in range(MAX_USERS):
		if unames[i] == unam:
			return i
	return None

user_x = [0 for i in range(MAX_USERS)]
user_y = [0 for i in range(MAX_USERS)]

# broadcast message to all message-queues
def broadcast(msg, room):
	print "broadcasting %s to %d" % (msg, room)
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


def leave_room(room, person):
	broadcast('<MESSAGE TYPE="broadcastKill"><USERNAME>%s</USERNAME></MESSAGE>"' % unames[person], room)

def bogue_des_nains_rouges(room):
	mes = '<MESSAGE TYPE="enterRoom" VALUE="update"><ROOMID VALUE="update">%d</ROOMID>' % room
	for i in range(10):
		mes += '<CARAC />'
	mes += '</MESSAGE>'
	broadcast(mes, room)

def update_room(room, person):
	print "Adding person %d to room %d" % (person, room)
	mes = '<MESSAGE TYPE="enterRoom" VALUE="update"><ROOMID VALUE="update">%d</ROOMID>' % room
	if 1:
		t = c = p = "1"
		tc = cc = pc = "0"
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
		mes += '<X>%d</X><Y>%d</Y><ID>%d</ID><GUEST>false</GUEST>' % (user_x[person], user_y[person], person)
		mes += '</CARAC>'
	mes += '</MESSAGE>'

	# broadcast to all the people in the room
	broadcast(mes, room)


def serve_client(conn, addr, id):
	client_host, client_port = addr
	print "Got connection from %s:%s. Starting thread %d" % (client_host, client_port, id)

	# Effacer vieux messages
	mq[id] = []

	init = time.time()
	ready = select.select([conn], [], [], 0.2)
	if ready[0]:
		req = conn.recv(1024)
		print "r: %s" % req
		print "policy-file-request" in req
		if "policy-file-request" in req:
			print "policy file"
			conn.sendall("<?xml version=\"1.0\"?><cross-domain-policy><allow-access-from domain=\"*\" to-ports=\"9100,9200\" /></cross-domain-policy>" + '\0')
			conn.close()
			return

	conn.sendall("<MESSAGE TYPE=\"set\" FROM=\"server\"><HR>jhdgkdsfjsdk</HR></MESSAGE>" + '\0')
	print "Acknowledged connection to %s:%s" % (client_host, client_port)

	# enterChat garbage
	req = conn.recv(1024)
	print "got %s; skipping it" % req

	# Initial room request
	req = conn.recv(1024)
	if req.find('TYPE="requestRoom"') < 0:
		print "Expected room request from %s:%s; got %s. Closing connection." % (client_host, client_port, req)
		conn.close()
		return
	print "got room request as expected: %s" % req
	username = req[req.find("<NOM>")+5:req.find("</NOM>")]
	if username in unames:
		print "%s:%s: connection with already logged-in username %s refused" % (client_host, client_port, username)
		conn.close()
		return

	# Avertir entree aux amis sur messagiel
	for i in range(MAX_USERS):
		if i != id:
			relai = '<MESSAGE TYPE="enter"><USERNAME>%s</USERNAME></MESSAGE>' % username
			mq[i].append(relai)

	unames[id] = username
	room = int(req[req.find("<ROOMID>")+8:req.find("</ROOMID>")])

	user_x[id] = random.randrange(300, 400)
	user_y[id] = random.randrange(300, 400)

	update_room(room, id)
	rpeople[room].append(id)

	visi = 1

	mes = '<MESSAGE TYPE="enterRoom"><ROOMID>%d</ROOMID>' % room

	for person in rpeople[room]:
		t = c = p = "1"
		tc = cc = pc = "0"

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
		mes += '<X>%d</X><Y>%d</Y><ID>%d</ID><GUEST>false</GUEST>' % (user_x[person], user_y[person], person)
		mes += '</CARAC>'

	# nains rouges
	#mes += '<CARAC /><CARAC />'
	mes += '</MESSAGE>'
	conn.sendall(mes.strip() + '\0')

	conn.setblocking(0)

	while 1:
		ready = select.select([conn], [], [], 0.01)
		if ready[0]:
			data = conn.recv(1024)
			if not data: break
			print ("%s: %s" % (username, data)).strip()
	
			# broadcast client's move and gzzzit messages as-is
			if data.find('TYPE="broadcastMove"') > 0 or data.find('TYPE="broadcastGzit"') > 0:
				# pour re'al, utiliser broadcastMoveb, sinon son avatar sera glitche'.
				if username == "real":
					broadcast(data.replace("broadcastMove", "broadcastMoveb"), room)
				else:
					broadcast(data, room)
			
			# broadcast visibility
			if data.find('TYPE="broadcastVisibility"') > 0:
				sta = int(data[data.find("<STATUS>")+8:data.find("</STATUS>")])
				#broadcast('<MESSAGE TYPE="broadcastVisibility"><USERNAME>%s</USERNAME><STATUS>%d</STATUS></MESSAGE>' % (username, sta), room)

				sta = int(data[data.find("<STATUS>")+8:data.find("</STATUS>")])

				if sta==visi:
					print "BV redondant"

				if sta == 0 and sta != visi:
					broadcast('<MESSAGE TYPE="broadcastVisibility"><USERNAME>%s</USERNAME><STATUS>%d</STATUS></MESSAGE>' % (username, sta), room)
				elif sta == 1 and sta != visi:
					# update avatar
					leave_room(room, id)
					update_room(room, id)
				visi = sta

			# store coords
			if data.find('TYPE="broadcastMove"') > 0 or data.find('TYPE="broadcastMoveb"') > 0:
				user_x[id] = int(data[data.find("<X>")+3:data.find("</X>")])
				user_y[id] = int(data[data.find("<Y>")+3:data.find("</Y>")])

			# relay public messages, route private messages
			if data.find('TYPE="broadcastText"') > 0:
				text = data[data.find("<TEXT>")+6:data.find("</TEXT>")]
				if data.find("PRIVATE") < 0:
					if text.strip() == "%2FNombre" or text.strip() == "%2Fnombre":
						broadcast('<MESSAGE TYPE="broadcastText"><TEXT>Il y a %d slocheux sur le chat.</TEXT><USERNAME>%s</USERNAME></MESSAGE>' % (nombre(), username), room)
					elif text.strip() == "%2FNains" or text.strip() == "%2Fnains":
						bogue_des_nains_rouges(room)
					else:
						broadcast('<MESSAGE TYPE="broadcastText"><TEXT>%s</TEXT><USERNAME>%s</USERNAME></MESSAGE>' % (text, username), room)
				else:
					who = data[data.find("<ID>")+4:data.find("</ID>")]
					mq[int(who)].append('<MESSAGE TYPE="broadcastText" PRIVATE="1"><TEXT PRIVATE="1">%s</TEXT><USERNAME>%s</USERNAME></MESSAGE>' % (text, username))
					mq[id].append('<MESSAGE TYPE="broadcastText" PRIVATE="1"><TEXT PRIVATE="1">%s</TEXT><USERNAME>%s</USERNAME></MESSAGE>' % (text, username))


			# room changes
			# <MESSAGE TYPE="RR" FROM="sloche8518"><DI>droite</DI><POS></POS><NOM>sloche8518</NOM><GUEST>false</GUEST></MESSAGE>
			
			# Subtilite:
			# les request room pour real sont envoyees par
			# *tous* les clients Flash presents, mais ne sont
			# bonnes que pour le bon compte.
			#
			# Raison historique possible: Real etait un bot
			# qui n'utilisait probablement pas un client Flash.
			move_boucher = 0
			if data.find('TYPE="requestRoomB"') > 0:
				if data.find('<CIBLE>%s</CIBLE>' % username) > 0:
					move_boucher = 1

			if (data.find('TYPE="requestRoom"') > 0 or move_boucher == 1) and data.find("<DIRECTION>") > 0:
				dir = data[data.find("<DIRECTION>")+11:data.find("</DIRECTION>")]
				nr = get_new_room(room, dir, user_x[id], user_y[id])

				if dir == "gauche" and user_x[id] > 100 and room == 15:
					nr = 65

				user_x[id] = random.randrange(300, 400)
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

				# tuyeau
				if room == 11 and nr == 61:
					user_x[id] = random.randrange(277, 342)
					user_y[id] = random.randrange(407, 458)

				# entree gzzzit
				if room == 15 and nr == 65:
					user_x[id] = random.randrange(545, 621)
					user_y[id] = random.randrange(479, 512)

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
					print "room 62, adjusting ycoord"
					user_y[id] = 360

				# partir de la vieille salle,
				# en avertir les gens encore la
				rpeople[room].remove(id)
				leave_room(room, id)

				# avertir les gens de la nouvelle
				# salle de notre arivee
				update_room(nr, id)

				# s'ajouter aux membres de la
				# nouvelle salle
				rpeople[nr].append(id)

				room = nr

				# on obtient le portrait de la salle
				mes = '<MESSAGE TYPE="enterRoom"><ROOMID>%d</ROOMID>' % room
				for person in rpeople[room]:
					t = c = p = 1
					tc = cc = pc = "0"
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
					mes += '<X>%d</X><Y>%d</Y><ID>%d</ID><GUEST>false</GUEST>' % (user_x[person], user_y[person], person)
					mes += '</CARAC>'
				# nains rouges
				# mes += '<CARAC /><CARAC />'
				mes += '</MESSAGE>'
				conn.sendall(mes.strip() + '\0')

				print "envoi %s -> %s" % (mes, username)


		# send off queued messages
		while len(mq[id]):
			if mq[id][0].strip() == "kick":
				mq[id] = mq[id][1:]
				broadcast('<MESSAGE TYPE="broadcastText"><TEXT>%s</TEXT><USERNAME>%s</USERNAME></MESSAGE>' % (("%s s'est fait kicker du chat" % username), username), room)
				conn.close()
				rpeople[room].remove(id)
				leave_room(room, id)
				unames[id] = ""
				return
			conn.sendall(mq[id][0].strip() + '\0')
			mq[id] = mq[id][1:]

	print "closed connection to %s:%s" % (client_host, client_port)
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
		print "messagiel: envoi direct a %s de '%s'" % (to, relai)
		queue_messagiel[chiffre_dans_messagiel(to)].append(relai)
	else:
		# Stocker le message et l'envoyer lorsque l'usager
		# se branchera au slochepop
		print "messagiel: stockage pour %s de '%s'" % (to, relai)
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
	print "messagiel: %s:%s -> usager %s" % (client_host, client_port, username)
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
				print "messagiel: %s: %s" % (username, data)

			# Requete ami
			if data.find('<OPTION>request</OPTION>') > 0:
				to = data[data.find("<TO>")+4:data.find("</TO>")]
				text = data[data.find("<TEXT>")+6:data.find("</TEXT>")]
				print "messagiel: %s req ami %s: '%s'" % (username, to, text)

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
				print "%s autorise %s a etre son ami" % (nom, to)

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
				print "%s refuse a %s le droit d'etre son ami" % (nom, to)			

				# Envoyer la bulle "ami refuse"
				relai = '<MESSAGE TYPE="send">'
				relai += '<TEXT OPTION="refus">%s</TEXT>' % nom
				relai += '<FROM>%s</FROM>' % nom
				relai += '</MESSAGE>'
				envoi_ou_stockage(to, relai)

			# Relai ami
			# <MESSAGE TYPE="ami" FROM="Client"><NOM>donald</NOM><AMI>laplante</AMI></MESSAGE>
			if data.find('TYPE="ami"') > 0:
				print "relai ami..."
				nom = data[data.find("<NOM>")+5:data.find("</NOM>")]
				ami = data[data.find("<AMI>")+5:data.find("</AMI>")]

				relai = '<MESSAGE TYPE="ami">'
				relai += '<AMI STATUS="1">%s</AMI>' % ami
				relai += '</MESSAGE>'
				envoi_ou_stockage(nom, relai)

			# Supprimer ami
			if data.find('<OPTION>supprimer</OPTION>') > 0:
				to = data[data.find("<TO>")+4:data.find("</TO>")]
				print "messagiel: %s supprime ami %s" % (username, to)

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
				print "messagiel: %s message a %s: '%s'" % (username, to, text)

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
			print "messagiel: %s: envoi depuis queue: %s" % (username, queue_messagiel[id][0])
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

