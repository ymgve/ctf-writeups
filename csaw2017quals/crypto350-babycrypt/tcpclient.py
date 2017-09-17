import socket, struct, os, binascii, base64

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
    
sc = socket.create_connection(("crypto.chal.csaw.io", 1578))

#known = "flag{Crypt0_is_s0_h@rd_t0_d0...}"
known = ""

while True:
    read_until(sc, "Enter your username (no whitespace): ")
    test = "a" * (15 - (len(known) % 16))
    sc.send(test + "\n")
    read_until(sc, "Your Cookie is: ")
    res = readline(sc)
    block = (len(known) / 16) * 32
    target = res[block:block+32]
    
    for i in xrange(126, 33, -1):
        test = ("a" * 16 + known)[-15:] + chr(i)
        sc.send(test + "\n")
        read_until(sc, "Your Cookie is: ")
        res = readline(sc)
        cand = res[0:32]
        if cand == target:
            known += chr(i)
            print "FOUND!!", repr(known)
            break
        
