echo "updating misc"

echo "recompiling server code"
rm ncweb html-newlines
make ncweb
make html-newlines

echo "running server"
python net-interface.py
