import sys
import md5
import os
import shutil

# les arguments !!!
if len(sys.argv) < 3:
	print "usage: %s IP fichier.swf" % sys.argv[0]
	sys.exit(1)

print "Modification du fichier SWF client ..."

# copie du SWF et dessasemblage
shutil.copyfile(sys.argv[2], "sloche_mod.swf")
if os.system("flasm -d sloche_mod.swf >sloche_mod.asm") != 0:
	print "foirage du dessassemblage !"
	sys.exit(1)

# check somme MD5 du SWF
f = open("sloche_mod.swf")
swf = f.read()
m = md5.new()
m.update(swf)
m.digest()

# lecture code desassemble
f = open("sloche_mod.asm")
client = f.read()
f.close()

# client 2003 detecte --
# Patch fix real 2003:
# Ligne 47813:
#      push 3
#      push -100
#
if m.hexdigest() == '4fd90f12605dae1248382fa9416a80b4':
	print "Client version 2003 detecte, tentative d'application du patch fixreal..."
	f = open("sloche_mod.asm")
	lignes = []
	for l in f:
		lignes.append(l)
	f.close()
	
	if "push 3" not in lignes[47813]:
		print "tentative foiree"
	else:
		s = lignes[47813]
		s = s.replace("push 3", "push -100")
		lignes[47813] = s
		client = '\n'.join(lignes)
		print "tentative reussie"

# remplacer les URLs serveurs par l'IP choisie
client = client.replace("www.sloche.com", sys.argv[1])
client = client.replace("admin.sloche.com", sys.argv[1])

# ecriture code modifie
out = open("sloche_mod.asm", "w")
out.write(client)
out.close()

# on re-assemble
if os.system("flasm -a sloche_mod.asm") != 0:
	print "foirage du reassemblage !"
	sys.exit(1)
shutil.move("sloche_mod.swf", "server/sloche-data/sloche.swf")

# on fait le menage
os.remove("sloche_mod.asm")
os.remove("sloche_mod.$wf")

#  
# creation des fichiers de configuration XML
#

print "Mise en place des fichiers de configuration XML..."

# lecture
f = open("server/sloche-data/config.default")
config = f.read()
f.close()
f = open("server/sloche-data/config_messagiel.default")
config1 = f.read()
f.close()

# modification
config = config.replace("SERVERADDR", sys.argv[1])
config1 = config1.replace("SERVERADDR", sys.argv[1])

# ecriture
f = open("server/sloche-data/simpleChatConfig.xml", "w")
f.write(config)
f.close()
f = open("server/sloche-data/simpleChatConfig1.xml", "w")
f.write(config1)
f.close()

print "C'est beau, ca peut rouler"
