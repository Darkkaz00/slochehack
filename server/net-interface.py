# pseudo-netcat, mais qui gere automatiquement
# plusieures connections en parallele a l'aide
# de threads

# http://stackoverflow.com/questions/1020980/interacting-with-another-command-line-program-in-python

import socket
import thread
import urllib
import select
import random
from subprocess import Popen, PIPE
import subprocess

MAX_USERS = 1024

thread_free = [True for i in range(MAX_USERS)]

def find_free_id():
	for i in range(MAX_USERS):
		if thread_free[i] == True:
			return i
	return -1

def serve_client(conn, addr, id):
	thread_free[id] = False
	client_host, client_port = addr
	print "Connexion obtenue: %s:%s. - thread %d" % (client_host, client_port, id)

	req = conn.recv(5 * 1024 * 1024)
	serv = Popen('./ncweb', shell=False, stdout=PIPE, stdin=PIPE, stderr=PIPE)
	serv.stdin.write(req)
	output = serv.stdout.read()
	conn.sendall(output)
	serv.kill()
	print "Fermeture de la connexion %s:%s" % (client_host, client_port)
	conn.shutdown(socket.SHUT_RDWR)
	thread_free[id] = True

host = ''
port = 80	# web
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
		print "trop de connexions simultanees"

