import sys
import os

if len(sys.argv) < 3:
	sys.exit(1)

prog = sys.argv[1].replace(".py", ".exe")

os.system('%s "%s"' % (prog, sys.argv[2]))
