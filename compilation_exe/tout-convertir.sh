cp conversion_exe.sh ../xml-server/
cp conversion_exe.sh ..
cp conversion_exe.sh ../server/

cd ../xml-server/; sh conversion_exe.sh; rm conversion_exe.sh; cd ../compilation_exe

cd ../server/; sh conversion_exe.sh; rm conversion_exe.sh; cd ../compilation_exe

cd ..; sh conversion_exe.sh; rm conversion_exe.sh; cd compilation_exe


cd gui
sh build.sh
cd ..
# Dans le merveilleux monde de Microsoft, il faut copier
# le fichier .exe et son .manifest de la meme commande,
# pas avec deux commandes separees, sinon ca marche pas,
# demandez-moi pas pourquoi !!!!!!!!!!!! >:(
cp gui/slochehack.exe gui/slochehack.exe.manifest gui/*.bat ..

cd ../server/
cc ncweb-windows.c -o ncweb.exe
cd ../compilation_exe