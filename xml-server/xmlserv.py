# TODO: eventify ? (instead of thread-per-client)

import socket
import thread
import urllib
import select
import random
from roommove import *
from getuserapi import *
import time

# mouches, grenouille, barbu, rapitissateur, roi et reine
pouvoirs_attaques = [13, 14, 22, 25, 27]
# laser, pet, gzzzit
pouvoirs_attaques_2 = [12, 31, 40]

MAX_USERS = 1024

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
			print "chrono start %d: %d" % (id, pv)
			chrono[id][pv] = time.time() + 30
			print pouvoirs[id]

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
rpeople = [[] for i in range(100)]

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

def fix_real(room):
	broadcast('<MESSAGE TYPE="BE"><ETAT>1</ETAT><FROM>%s</FROM><TO>%s</TO><EFFET>%s</EFFET><PARAM>1</PARAM></MESSAGE>' % ("real", "real", "41"), room)

def docteur_liposuccion(room, who):
	broadcast('<MESSAGE TYPE="DL"><TARGET>%s</TARGET></MESSAGE>' % unames[who], room)

def leave_room(room, person):
	broadcast('<MESSAGE TYPE="BK"><USERNAME>%s</USERNAME></MESSAGE>"' % unames[person], room)

def description_salle(room, update=False, new_people=[]):
	if update:
		mes = '<MESSAGE TYPE="ER" VALUE="update"><RID VALUE="update">%d</RID>' % room
		who = new_people
	else:
		mes = '<MESSAGE TYPE="ER"><RID>%d</RID>' % room
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
	client_host, client_port = addr
	print "Got connection from %s:%s. Starting thread %d" % (client_host, client_port, id)

	conn.sendall("<MESSAGE TYPE=\"ACK\"></MESSAGE>" + '\0')
	print "Acknowledged connection to %s:%s" % (client_host, client_port)

	# Initial room request
	# <MESSAGE TYPE="RR" FROM="laplante"><RID>23</RID><DI>droite</DI><NOM>laplante</NOM><GUEST>false</GUEST></MESSAGE>
	req = conn.recv(1024)
	if req.find('TYPE="RR"') < 0:
		print "Expected room request from %s:%s; got %s. Closing connection." % (client_host, client_port, req)
		conn.close()
		return
	username = req[req.find("<NOM>")+5:req.find("</NOM>")]
	if username in unames:
		print "%s:%s: connection with already logged-in username %s refused" % (client_host, client_port, username)
		conn.close()
		return
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
				print "%s: %d expire" % (unames[id], pv)
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
			print ("%s:%s: %s" % (client_host, client_port, data)).strip()
	
			# broadcast client's move and emotion messages as-is
			if data.find('TYPE="BST"') > 0 or data.find('TYPE="BM"') > 0 or data.find('TYPE="BE"') > 0:
				print data

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

			# teleport
			if data.find('TYPE="RR"') > 0 and data.find('<RID>') > 0:
				# hack!

				ref_room = int(data[data.find("<RID>")+5:data.find("</RID>")])
				dir = data[data.find("<DI>")+4:data.find("</DI>")]

				user_x[id] = random.randrange(300, 400)
				user_y[id] = random.randrange(350, 450)

				nr = get_new_room(ref_room, dir, 2000, 2000)

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

				if nr > 71:
					print "y coord club swompe ajust"
					user_y[id] = old_y

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
