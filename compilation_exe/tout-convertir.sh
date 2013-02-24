cp conversion_exe.sh ../xml-server/
cp conversion_exe.sh ..
cp conversion_exe.sh ../server/

cd ../xml-server/; sh conversion_exe.sh; rm conversion_exe.sh; cd ../compilation_exe

cd ../server/; sh conversion_exe.sh; rm conversion_exe.sh; cd ../compilation_exe

cd ..; sh conversion_exe.sh; rm conversion_exe.sh; cd compilation_exe

