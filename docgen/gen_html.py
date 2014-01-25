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
			ok  =0
		elif t == '.UNLIT':
			lit = 0
			ok = 0
		if lit == 0:
			t = cgi.escape(t.decode('utf-8')).encode("ascii", "xmlcharrefreplace") 
			for x in htmlentitydefs.codepoint2name:
				t = t.replace("&#" + str(x) + ";", "&" + htmlentitydefs.codepoint2name[x] + ";")
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
			if dac == 0:
				body += "<PRE>"
			dac = 1
		elif comm == '.NO':	# normal
			if dac == 1:
				body += "</PRE>"
			dac = 0
		elif comm == '.TI':
			title = line[4:].strip('\n')
			body += ("<H3>%s</H3>" % encode_to_html(title))
		elif comm == '.SEC':
			sec = line[5:].strip('\n')
			if dac:
				body += "</PRE>"
			body += ("<A NAME=\"ancre%d\"></A><U>%s</U>" % (anch, encode_to_html(sec)))
			head += "<A HREF=\"#ancre%d\"><U>%s</U></A><BR>\n" % (anch, encode_to_html(sec)) 
			anch += 1
			if dac:
				body += "<PRE>"
		elif comm == '.TAB':
			body += ".TAB\n"
		elif comm == '.HL':
			body += "<HR>\n"
	else:
		if not dac:
			body += "<BR>"

		line = encode_to_html(line)
		body += line.strip('\n')
	body += "\n"

if dac:
	body += "</PRE>"

for x in body.split('\n'):
	if x == '.TAB':
		print "<P>"
		print head
		print "</P>"
	else:
		print x

f.close()
