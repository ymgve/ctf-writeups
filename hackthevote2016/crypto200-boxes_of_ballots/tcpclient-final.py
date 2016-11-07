import socket, struct, binascii, random, json
import telnetlib   
from Crypto.Cipher import AES

def readline(sc, show = True):
    res = ""
    while len(res) == 0 or res[-1] != "\n":
        data = sc.recv(1)
        if len(data) == 0:
            print repr(res)
            print "Server disconnected"
            exit()
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
            print "Server disconnected"
            exit()
        res += data
        
    return res[:-(len(s))]
    
def x(n):
    return struct.pack("<Q", n)

def xor(a, b):
    assert len(a) == len(b)
    res = ""
    for i in xrange(len(a)):
        res += chr(ord(a[i]) ^ ord(b[i]))
        
    return res
    
def do_call(pt):
    sc = socket.create_connection(("boxesofballots.pwn.republican", 9001))
    cmd = '{"debug": false, "data": "' + pt + '", "op": "enc"}'
    sc.send(cmd)
    readline(sc, False)
    j = json.loads(read_until(sc, "}") + "}")
    ct = []
    for i in xrange(0, len(j["data"]), 32):
        ct.append(binascii.a2b_hex(j["data"][i:i+32]))

    return ct

IV = '\xf7\xb2d\x8e`\x8aT\x02\xf3\xe3m\xe1\x1c\xc0\x19\xfd'

cands = "_abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ{}"
for i in xrange(32, 127):
    if chr(i) not in cands:
        cands += chr(i)
        
sofar = ""
while True:
    ct1 = do_call("aaaaaaaaaa" + "a" * len(sofar))

    for c in cands:
        pt = c + sofar + "                "
        pt = pt[0:16]
        pt = xor(pt, IV)
        pt = xor(pt, ct1[1])

        pt2 = ""
        for cc in pt:
            pt2 += "\\u%04x" % ord(cc)

        ct2 = do_call(pt2)
        print c, ct2
        if ct2[0] == ct1[2]:
            sofar = c + sofar
            print "FOUND", sofar
            break
