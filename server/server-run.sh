echo "Compilation du serveur web"
rm -f ncweb
make ncweb

echo "Lancement du serveur web"
python net-interface.py
