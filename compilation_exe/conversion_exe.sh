# MINGW + Python + Py2exe

echo -n "from distutils.core import setup
import py2exe

setup(console="[ >conversion_exe.py

ls *.py | grep '\.py$' | sed 's/\.\///g' | grep -v exe | sed s/^/\'/ | sed s/$/\'/ | tr '\n' ',' | sed 's/,$//g' | sed 's/,/, /g' >>conversion_exe.py

echo -n "])" >>conversion_exe.py

python conversion_exe.py py2exe
rm conversion_exe.py*

rm -rf build
mv dist/* "`pwd`"
rm -rf dist