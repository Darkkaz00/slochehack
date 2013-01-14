# Ce script lance tous les serveurs tout seul et vous
# dit à quelle addresse IP locale le site sera disponible.
# Testé sous Linux/gnome, Linux/mate et linux/ubuntu.

# Changer au besoin. seulement testé avec GNOME et MATE,
# j'espère que la syntaxte des paramètres sera la même avec
# d'autres environnements graphiques...
TERMINAL_GRAPHIQUE=mate-terminal

# Fichier client à utiliser.
CLIENT=fichiers-client/sloche2007.swf

# Attention de changer XMLSERV à xmlserv2003.py si on choisit
# le client 2003 !
XMLSERV=xmlserv.py

ifconfig | grep 192 | grep -v RX | sed 's/inet addr:\(.*\)\ Bcast:\(.*\)/\1/' | tr -d ' ' >localhost.txt
echo "IP: `cat localhost.txt`"
sh create-modded-swf.sh `cat localhost.txt` $CLIENT
cat server/sloche-data/config.default | sed s/SERVERADDR/`cat localhost.txt`/g > server/sloche-data/simpleChatConfig.xml
rm localhost.txt

$TERMINAL_GRAPHIQUE --working-directory="`pwd`" -x bash -c "cd server; ./run; bash" &
$TERMINAL_GRAPHIQUE --working-directory="`pwd`" -x bash -c "cd logiciels; cd flashpolicyd_v0.6; sudo python Standalone/flashpolicyd.py --file=../../custom-policy.xml; bash" &
$TERMINAL_GRAPHIQUE --working-directory="`pwd`" -x bash -c "cd xml-server; echo xmlserv; python $XMLSERV; bash" &
