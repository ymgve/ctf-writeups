from hashlib import md5

s = [59, 21, 25, 32, 30, 3, 63, 38, 5, 29, 40, 53, 17, 56, 58, 37, 45, 43, 52, 61, 7, 55, 57, 12, 26, 13, 49, 16, 36, 8, 31, 41, 20, 51, 33, 15, 1, 0, 23, 27, 35, 18, 47, 62, 14, 60, 10, 54, 46, 50, 9, 48, 24, 28, 44, 2, 6, 34, 19, 42, 11, 39, 22, 4]
p = [14, 7, 25, 2, 22, 32, 29, 0, 28, 31, 6, 18, 12, 27, 33, 9, 17, 21, 8, 26, 23, 35, 4, 5, 11, 20, 30, 24, 15, 1, 19, 16, 10, 13, 34, 3]

rounds = 3
nsbox = 6	# number of s-boxes
bsbox = 6	# input bits per s-box
ssize = 1 << bsbox
bits = nsbox * bsbox
insize = 1 << bits

#####################################################
import sys
sys.path.append('../stuff')
from secret import master_key as key
assert len(key) == 3
assert all(0 <= k < insize for k in key)
#####################################################

_s_inv = [0] * len(s)
for i in range(len(s)):
	_s_inv[s[i]] = i

_p_inv = [0] * len(p)
for i in range(len(p)):
	_p_inv[p[i]] = i


def sbox(x):
	return s[x]


def pbox(x):
	y = 0
	for i in range(len(p)):
		y |= ((x >> i) & 1) << p[i]
	return y


def inv_s(x):
	return _s_inv[x]


def inv_p(x):
	y = 0
	for i in range(len(p)):
		y |= ((x >> p[i]) & 1) << i
	return y


def split(x):
	y = [0] * nsbox
	for i in range(nsbox):
		y[i] = (x >> (i * bsbox)) & 0x3f
	return y


def merge(x):
	y = 0
	for i in range(nsbox):
		y |= x[i] << (i * bsbox)
	return y


def round(p, k):
	u = [0] * nsbox
	x = split(p)
	for i in range(nsbox):
		u[i] = sbox(x[i])
	v = pbox(merge(u))
	w = v ^ k
	return w


def encrypt(p, rounds):
	for i in range(rounds):
		p = round(p, key[i])
	return p


def make_flag(k):
	param = md5(b"%x%x%x" % (k[0], k[1], k[2])).hexdigest()
	return "SharifCTF{%s}" % param


if __name__ == '__main__':
	print(make_flag(key))