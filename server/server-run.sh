echo "updating misc"

echo "recompiling server code"
rm ncweb html-newlines
if [ $(uname | grep MINGW) ];
then
	cc ncweb-win32.c -o ncweb
else
	make ncweb
fi
make html-newlines

echo "running server"
python net-interface.py
