import socket, struct
import telnetlib   

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
    
def pad(s):
    if len(s)%9 == 0:
        return s
    for i in xrange((9-(len(s)%9))):
        s.append(0)
    return s

def printmat(matrix):
    for row in matrix:
        for value in row:
            print value,
        print ""
    print ""

def flip(matrix):
    out = [[0 for x in xrange(3)] for x in xrange(3)]   
    for rn in xrange(3):
        for cn in xrange(3):
            out[cn][rn] = matrix[rn][cn]
            
    return out

def genBlockMatrix(s):
    outm = [[[7 for x in xrange(3)] for x in xrange(3)] for x in xrange(len(s)/9)]
    for matnum in xrange(0,len(s)/9):
        for y in xrange(0,3):
            for x in xrange(0,3):
                outm[matnum][y][x] = s[(matnum*9)+x+(y*3)]
    return outm

def fixmatrix(matrixa, matrixb):
    out = [[0 for x in xrange(3)] for x in xrange(3)]   
    for rn in xrange(3):
        for cn in xrange(3):
            out[cn][rn] = (int(matrixa[rn][cn])|int(matrixb[cn][rn]))&~(int(matrixa[rn][cn])&int(matrixb[cn][rn]))
    return out

def invertfix(matrixa, matrixb):
    out = [[0 for x in xrange(3)] for x in xrange(3)]   
    for rn in xrange(3):
        for cn in xrange(3):
            out[cn][rn] = (int(matrixa[rn][cn])^int(matrixb[rn][cn]))
    return out

    
sc = socket.create_connection(("vermatrix.pwn.democrat", 4201))

read_until(sc, "SEED: ")
seed = read_until(sc, "\n")

seedmatrix = genBlockMatrix(pad([ord(c) for c in seed]))

matrix = readline(sc) + " " + readline(sc) + " " + readline(sc)
res = genBlockMatrix(matrix.split())[0]

for block in seedmatrix[::-1]:
    res = invertfix(res, block)

s = []
for rn in xrange(3):
    for cn in xrange(3):
        s.append(str(res[rn][cn]))
        
sc.send(",".join(s) + "\n")

while True:
    data = sc.recv(16384)
    if len(data) == 0:
        break
    for line in data.split("\n"):
        print repr(line)
    
# flag{IV_wh4t_y0u_DiD_Th3r3}
