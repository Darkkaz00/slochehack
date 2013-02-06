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

MAX_USERS = 1024

true = True
false = False

# people in a given room
rpeople = [[] for i in range(100)]

# id -> username lookup
unames = ["" for i in range(MAX_USERS)]

# message queues
mq = [[] for i in range(MAX_USERS)]

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
					user_x[id] = random.randrange(80, 200)
				if dir == "gauche":
					user_x[id] = random.randrange(500, 600)
				if dir == "haut":
					user_y[id] = random.randrange(400, 500)
				if dir == "bas":
					user_y[id] = random.randrange(300, 350)

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

	rpeople[room].remove(id)
	leave_room(room, id)
	unames[id] = ""

host = ''
port = 9100
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
id = 0

s.listen(5)

while 1:
	conn, addr = s.accept()
	id = find_free_id()
	if id >= 0:
		print "New thread with id %d" % id
		thread.start_new_thread(serve_client, (conn, addr, id))
