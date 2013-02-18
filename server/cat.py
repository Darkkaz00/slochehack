from __future__ import print_function
import sys

# behaves same as the real unix/gnu/whatever cat.
# why this ? because things get ugly on MinGW
# otherwise.

if len(sys.argv) < 2:
	sys.exit(1)

f = open(sys.argv[1])
cont = f.read()
print(cont, end='')
f.close()
