import sys
import os.path

def liste_amis(nam):
	username = nam

	if not os.path.exists("amis/" + username):
		try:
			f = open("amis/" + username, "w")
			f.close()
		except IOError as e:
			return

	try:
		data = open("amis/" + username, "r")
		amis = []
		for line in data:
			amis.append(line.strip('\n'))	
		return amis
		data.close()
	except IOError as e:
		return


