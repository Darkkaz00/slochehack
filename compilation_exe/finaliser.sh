cd ../xml-server/
rm *.py
mv README README.TXT
unix2dos README.TXT
cd ../compilation_exe

cd ../server/
rm *.py
#mv README README.TXT
#unix2dos README.TXT
rm README
rm passerelle1.bat passerelle2.bat
cc ncweb-windows.c -o ncweb.exe
rm *.sh *.c demarrage-unix
cd ../compilation_exe

cd ..
rm *.py
mv HISTORIQUE HISTORIQUE.TXT
unix2dos HISTORIQUE.TXT
mv FIXREAL FIXREAL.TXT
unix2dos FIXREAL.TXT
rm autorun-linux.sh LISEZMOI*
mv FICHIERS-EXTERNES-REQUIS FICHIERS-EXTERNES-REQUIS.TXT
unix2dos FICHIERS-EXTERNES-REQUIS.TXT
mv compilation_exe/LISEZMOI.TXT "`pwd`"
cd compilation_exe

cd gui
sh build.sh
cd ..
cp gui/slochehack.exe gui/*.bat ..
