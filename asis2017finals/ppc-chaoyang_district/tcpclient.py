import socket, struct, os, binascii, base64, random
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

def analyze_position(grid):
    bestscore = 0
    best = None
    
    cands = []
    for y in xrange(1, 9):
        for x in range(1, 9):
            if grid[x+y*10] == ".":
                score = 0
                for dx, dy in ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)):
                    subscore = 0
                    tx = x
                    ty = y
                    while True:
                        tx += dx
                        ty += dy
                        if grid[tx+ty*10] == "B":
                            subscore += 1
                        else:
                            break
                            
                    if grid[tx+ty*10] == "W":
                        score += subscore
                
                if score > 0:
                    cand = "abcdefgh"[x-1] + str(y)
                    if score > bestscore:
                        best = cand
                        bestscore = score
                        
    print "best candidate", bestscore, best
    return best
                
            
sc = socket.create_connection(("178.62.22.245", 32145))

while True:
    print read_until(sc, "Turn: Player")
    print read_until(sc, "  a b c d e f g h \n")
    
    grid = ["X"] * 100
    for y in xrange(1, 9):
        line = readline(sc)
        for x in xrange(1, 9):
            c = line[x*2]
            if c in "M.":
                grid[x+y*10] = "."
            else:
                grid[x+y*10] = c
                
    print grid
    res = analyze_position(grid)
    
    sc.send(res + "\n")

while True:
    data = sc.recv(16384)
    if len(data) == 0:
        break
    for line in data.split("\n"):
        print repr(line)
    