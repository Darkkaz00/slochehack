import sys
import os.path

# import amis_api
# >>> amis_api.liste_amis("donald")
# ['bob', 'carl']1
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

# import amis_api
# amis_api.stocker_liste_amis("donald", ["bob", "carl"])
def stocker_liste_amis(nam, liste):
		try:
			f = open("amis/" + nam, "w")
			for n in liste:
				f.write(n + '\n')
			f.close()
		except IOError as e:
			return


