import sys
import os.path

# import stockage_messagiel_api
# stockage_messagiel_api.obtenir_vider_stockage("donald")
def obtenir_vider_stockage(nam):
	username = nam

	if not os.path.exists("stockage_messagiel/" + username):
		try:
			f = open("stockage_messagiel/" + username, "w")
			f.close()
			return []
		except IOError as e:
			return []

	try:
		data = open("stockage_messagiel/" + username, "r")
		# obtenir
		messages = []
		for line in data:
			messages.append(line.strip('\n'))	
		data.close()
		# vider et retourner
		f = open("stockage_messagiel/" + username, "w")
		f.close()
		return messages
	except IOError as e:
		return

# import stockage_messagiel_api
# stockage_messagiel_api.ajouter("donald", '<MESSAGE TYPE="beurre"></MESSAGE>')
def ajouter(username, msg):
	try:
		f = open("stockage_messagiel/" + username, "a")
		f.write(msg + '\n')
		f.close()
		return True
	except IOError as e:
		return False


