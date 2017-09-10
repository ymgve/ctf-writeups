import socket, struct, os, binascii, base64, subprocess
import telnetlib   

import base58 # https://raw.githubusercontent.com/keis/base58/master/base58.py

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

def I(n):
    return struct.pack("<I", n)
    
def Q(n):
    return struct.pack("<Q", n)

def gen_addr(prefix):
    for a in '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz':
        for b in '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz':
            res = base58.b58decode((prefix+a+b).ljust(33, "1"))
            res = base58.b58encode_check(res[0:21])
            if res.startswith(prefix):
                return res
                
    return None

sc = socket.create_connection(("66.172.27.77", 11019))

read_until(sc, "Are you ready? [Y]es or [N]o:")
sc.send("Y\n")
read_until(sc, "Send a BTC valid address that starts with ")
prefix = read_until(sc, ":")
print prefix
res = gen_addr(prefix)
print res
if res == None:
    print "No valid BTC addr"
    exit()
    
sc.send(res + "\n")

read_until(sc, "[Q]uit")
sc.send("S\n")

read_until(sc, "send the first string:")
sc.send("\x00" * 504 + "\x00" + "\n")

read_until(sc, "send the second string:")
sc.send("\x00" * 504 + "\x01" + "\n")

while True:
    data = sc.recv(16384)
    if len(data) == 0:
        break
    for line in data.split("\n"):
        print repr(line)
    
