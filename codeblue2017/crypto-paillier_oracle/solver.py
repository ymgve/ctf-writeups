import socket, struct, os, binascii, base64, gmpy2, random, hashlib, string
import telnetlib   

import psyco; psyco.full()

def readline(sc, show = True):
    res = ""
    while len(res) == 0 or res[-1] != "\n":
        data = sc.recv(1)
        if len(data) == 0:
            print repr(res)
            raise Exception("Server disconnected")
        res += data
        
    if show:
        print repr(res[:-1])
    return res[:-1]

def read_until(sc, s):
    res = ""
    while not res.endswith(s):
        data = sc.recv(1)
        if len(data) == 0:
            print repr(res)
            raise Exception("Server disconnected")
        res += data
        
    return res[:-(len(s))]
    
def read_all(sc, n):
    data = ""
    while len(data) < n:
        block = sc.recv(n - len(data))
        if len(block) == 0:
            print repr(data)
            raise Exception("Server disconnected")
        data += block

    return data

def encrypt(pk, m):
    assert m < pk[0]
    while True:
        r = random.randint(1, pk[0])
        if gmpy2.gcd(r, pk[0]) == 1:
            break
    c1 = pow(pk[1], m, pk[0]**2)
    c2 = pow(r, pk[0], pk[0]**2)
    return (c1*c2) % pk[0]**2

def do_proof_of_work(sc):
    read_until(sc, "SHA256(XXXX+")
    postfix = read_until(sc, ") == ")
    hash = read_until(sc, "\n")
    print postfix, hash
    for a in string.ascii_letters+string.digits:
     print a,
     for b in string.ascii_letters+string.digits:
      for c in string.ascii_letters+string.digits:
       for d in string.ascii_letters+string.digits:
        if hashlib.sha256(a+b+c+d + postfix).hexdigest() == hash:
            print "found POW", a+b+c+d
            sc.send(a+b+c+d)
            return
    
def oracle(sc, ct):
    sc.send(str(ct) + "\n")
    read_until(sc, "LSB is ")
    res = readline(sc, False)
    return res[0]

sc = socket.create_connection(("oracle.tasks.ctf.codeblue.jp", 7485))

do_proof_of_work(sc)

read_until(sc, "Public key is here: (")
n = int(read_until(sc, ", "))
g = int(read_until(sc, ")"))
pubkey = (n, g)

nbits = len(bin(n)[2:])

read_until(sc, "...and Encrypted Flag: ")
flagct = int(readline(sc, False))

cachedbit = "0"
bits = ""

# starting number found by experimenting, can start at 0 but uses more time
for i in xrange(1672, nbits+1):
    # shift plaintext left by i bits
    ct = pow(flagct, 1 << i, n**2)
    res = oracle(sc, ct)
    
    if res == "0":
        # shifted plaintext < n, so we know the shifted out bit is 0
        # but we might have a 1 bit that we haven't applied, so use the cached bit
        bits += cachedbit
        cachedbit = "0"
    else:
        # shifted plaintext >= n
        # need to test if bitlength of shifted plaintext is larger or equal
        mask = 1 << (nbits - i)
        tempval = flagct * encrypt(pubkey, n - mask) % n**2
        ct = (tempval ** 2) % n**2
        res = oracle(sc, ct)
        
        if res == "0":
            # shifted plaintext longer than n
            # we removed the MSB successfully, add bit 1 to result and continue
            bits += "1"
            cachedbit = "0"
            flagct = tempval
        else:
            # shifted plaintext equal in length to n
            # we remove the next largest MSB instead, but also have to remember
            # that we removed it, so set cached bit
            bits += cachedbit
            cachedbit = "1"
            mask = 1 << (nbits - i - 1)
            flagct = (flagct * encrypt(pubkey, n - mask)) % n**2
    
    x = "%x" % int(bits, 2)
    if len(x) % 2 == 1:
        x = "0" + x

    print repr(x.decode("hex"))

while True:
    data = sc.recv(16384)
    if len(data) == 0:
        break
    for line in data.split("\n"):
        print repr(line)
