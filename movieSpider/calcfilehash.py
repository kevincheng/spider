def b(j):
	g = str()
	jlen = len(j)
	for f in xrange(jlen):
		h = j[f]
		if ord(h)+47 >= 126:
			g += chr(ord(" ")+(ord(h)+47)%126)
		else:
			g += chr(ord(h)+47)
	return g

def d(g):
	return ''.join(reversed(g))

def c(j,h,g,f):
	jlen = len(j)
	retvalue = j[jlen-f+g-h:jlen-f+g]+j[jlen-f:jlen-f+g-h]+\
			j[jlen-f+g:jlen]+j[0:jlen-f]
	return retvalue

def shtg_calcfilehash(a):
	if len(a) > 32:
		if a[0] == 'o':
			return b(c(a[1:],8,17,27))
		if a[0] == 'n':
			return b(d(c(a[1:],6,15,17)))
		if a[0] == 'm':
			return d(c(a[1:],6,11,17))
		if a[0] == 'l':
			return d(b(c(a[1:],6,12,17)))
		if a[0] == 'k':
			return c(a[1:], 14,17,24)
		if a[0] == 'j':
			return c(b(d(a[1:])), 11,17,27)
		if a[0] == 'i':
			return c(d(b(a[1:])),5,7,24)
		if a[0] == 'h':
			return c(b(a[1:]),12,22,30)
		if a[0] == 'g':
			return c(d(a[1:]),11,15,21)
		if a[0] == 'f':
			return c(a[1:],14,17,24)
		if a[0] == 'e':
			return c(a[1:],4,7,22)
		if a[0] == 'd':
			return d(b(a[1:]))
		if a[0] == 'c':
			return b(d(a[1:]))
		if a[0] == 'b':
			return d(a[1:])
		if a[0] == 'a':
			return b(a[1:])
	return a
