echo "Compilation du serveur web"
rm -f ncweb ncweb.exe
if [ $(uname | grep MINGW) ];
then
	cc ncweb-win32.c -o ncweb
else
	make ncweb
fi

echo "Lancement du serveur web"
python net-interface.py
