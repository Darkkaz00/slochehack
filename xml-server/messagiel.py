# TODO: eventify ? (instead of thread-per-client)

import socket
import thread
import urllib
import select
import random
from roommove import *
from getuserapi import *
import time

MAX_USERS = 1024

# id -> username lookup
unames = ["" for i in range(MAX_USERS)]

def find_free_id():
	for i in range(MAX_USERS):
		if unames[i] == "":
			return i
	return -1

MAX_USERS = 1024

def serve_client(conn, addr, id):
	client_host, client_port = addr
	print "Nouvelle conn. %s:%s, lancement thread %d" % (client_host, client_port, id)

	# Note: ACK c'est seulement pour le serveur de chat !
	#conn.sendall("<MESSAGE TYPE=\"ACK\"></MESSAGE>" + '\0')
	#print "Acknowledged connection to %s:%s" % (client_host, client_port)

	while True:
		ready = select.select([conn], [], [], 0.01)
		if ready[0]:
			data = conn.recv(1024)
			print "%d: %s" % (id, data)
			if not data:
				break

	unames[id] = ""
	print "Fermeture de la connection %s:%s" % (client_host, client_port)
	conn.close()

host = ''
port = 9200
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
id = 0

s.listen(5)

while 1:
	conn, addr = s.accept()
	id = find_free_id()
	if id >= 0:
		thread.start_new_thread(serve_client, (conn, addr, id))
	else:
		print "plus de place !!!"

