# Ce script lance tous les serveurs tout seul et vous
# dit à quelle addresse IP locale le site sera disponible.
# Testé sous Linux/gnome, Linux/mate et linux/ubuntu.

# Ce script de lançage ne fonctionne pas avec le terminal
# graphique LXDE, désolé :( Ce script ne fonctionne pas non
# plus avec la version BSD de la commande ifconfig.
# Vous êtes pas obligé d'utiliser ce script, il est possible
# de lancer le serveur "manuellement", voir le fichier "README".

# Changer au besoin. seulement testé avec GNOME et MATE,
# j'espère que la syntaxte des paramètres sera la même avec
# d'autres environnements graphiques...
TERMINAL_GRAPHIQUE=mate-terminal

# Fichier client à utiliser.
CLIENT=fichiers-client/sloche2004.swf

# Attention de changer XMLSERV à xmlserv2003.py si on choisit
# le client 2003 !
XMLSERV=xmlserv.py

# Tuyeauterie assez compliquée pour extraire l'adresse IP LAN
ifconfig | grep 192 | grep -v RX | sed 's/inet addr:\(.*\)\ Bcast:\(.*\)/\1/' | tr -d ' ' | tail -1 >localhost.txt
echo "IP: `cat localhost.txt`"

# Modifier le SWF et les XML
python modification-swf.py `cat localhost.txt` $CLIENT
rm localhost.txt

# Lancer le serveur web et le serveur chat XML
# dans deux fenêtres terminal graphiques séparées
$TERMINAL_GRAPHIQUE --working-directory="`pwd`" -x sh -c "cd server; ./demarrage-unix; sh" &
$TERMINAL_GRAPHIQUE --working-directory="`pwd`" -x sh -c "cd xml-server; echo xmlserv; python $XMLSERV; sh" &
