cp nettoyage.sh ../xml-server/
cp nettoyage.sh ..
cp nettoyage.sh ../server/

cd ../xml-server/; sh nettoyage.sh; rm nettoyage.sh; cd ../compilation_exe

cd ../server/; sh nettoyage.sh; rm nettoyage.sh; cd ../compilation_exe

cd ..; sh nettoyage.sh; rm nettoyage.sh; cd compilation_exe

cp ../server/passerelle1.bat ../server/passerelle.bat