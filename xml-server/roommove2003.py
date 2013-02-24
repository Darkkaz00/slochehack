def get_new_room(rid, move, x, y):
	nr = rid

	if (rid / 10) == 1:
		# rid=11, 591, 287 to 692, 316 ---> 61
		if rid == 11 and x >= 591 and x <= 692 and y >= 287 and y <= 316:
			return 61
		if move == "gauche":
			nr -= 1
			if nr < 11: nr = 15
		if move == "droite":
			nr += 1
			if nr > 15: nr = 11
		if move == "haut":
			nr = 40 + (nr % 10)
		if move == "bas":
			nr = 20 + (nr % 10)

	if (rid / 10) == 2:
		if move == "gauche":
			nr -= 1
			if nr < 21: nr = 25
		if move == "droite":
			nr += 1
			if nr > 25: nr = 21
		if move == "haut":
			nr = 10 + (nr % 10)
		if move == "bas":
			nr = 30 + (nr % 10)

	if (rid / 10) == 3:
		if move == "gauche":
			nr -= 1
			if nr < 31: nr = 35
		if move == "droite":
			nr += 1
			if nr > 35: nr = 31
		if move == "haut":
			nr = 20 + (nr % 10)
		if move == "bas":
			nr = 40 + (nr % 10)

	if (rid / 10) == 4:
		if move == "gauche":
			nr -= 1
			if nr < 41: nr = 45
		if move == "droite":
			nr += 1
			if nr > 45: nr = 41
		if move == "haut":
			nr = 30 + (nr % 10)
		if move == "bas":
			nr = 10 + (nr % 10)

	if (rid / 10) == 6:
		if rid == 61 and move == "bas":
			return 11
		if rid == 65 and move == "bas":
			return 15
		if move == "gauche":
			nr -= 1
			if nr < 61: nr = 65
		if move == "droite":
			nr += 1
			if nr > 65: nr = 61

	print "%d %s -> %d" % (rid, move, nr)
	return nr
