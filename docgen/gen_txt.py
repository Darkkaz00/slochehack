from sys import argv, exit
import htmlentitydefs
import cgi

# fix < > , unicode french chars (accented e, etc.)
def encode_to_html(strg):
	lit = 0
	toks = strg.split(" ")
	toks_ed = []
	for t in toks:
		if t == '.LIT':
			lit = 1
		elif t == '.UNLIT':
			lit = 0
		if lit == 0:
			toks_ed.append(t)

	harp = " ".join(toks_ed)
	harp = harp.replace(" .UNLIT ", "")
	harp = harp.replace(" .LIT ", "")
	return harp

body = ""
head = ""
anch = 0

if len(argv) < 2:
	print "need argument"
	exit(1)

dac = 0
f = open(argv[1])

for line in f:
	if len(line) > 2 and line[0] == '.':
		comm = line.split(' ')[0].strip('\n')
		if comm == '.DAC':	# monospace
			dac = 1
		elif comm == '.NO':	# normal
			dac = 0
		elif comm == '.TI':
			title = line[4:].strip('\n')
			body += ("Titre: %s" % encode_to_html(title))
		elif comm == '.SEC':
			sec = line[5:].strip('\n')
			titl = ("Section %d: %s" % (anch, encode_to_html(sec)))
			body += "*" * len(titl) + "\n"
			body += titl + "\n"
			body += "*" * len(titl)
			head += "%d. %s\n" % (anch, encode_to_html(sec)) 
			anch += 1
		elif comm == '.TAB':
			body += ".TAB"
		elif comm == '.HL':
			body += "-----------------------------------------------------------------"
	else:
		line = encode_to_html(line)
		body += line.strip('\n')
	body += "\n"

for x in body.split('\n'):
	if x == '.TAB':
		print ""
		print head
		print ""
	else:
		print x

f.close()
