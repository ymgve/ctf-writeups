
def xor(s1,s2):
    assert len(s1) == len(s2)
    return ''.join(chr(ord(a) ^ ord(b)) for a,b in zip(s1,s2))

data = open("encrypted", "rb").read().strip().decode("hex")

crib = "flag{"
firstkey = xor(data[0:len(crib)], crib)

firstkey = "A quart jar of oil mixed with zinc oxide makes a very bright paint"

for i in xrange(len(data) - len(firstkey)):
    print i, repr(xor(firstkey, data[i:i+len(firstkey)]))

