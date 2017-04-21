from PIL import Image
import socket, struct, os, binascii, base64, hashlib, sys
import telnetlib   
import numpy as np

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

def solve_chall(sc):
    read_until(sc, "MD5(key+\"")
    salt = read_until(sc, "\")[:4]==")
    print "salt", salt
    lastbytes = readline(sc, False)
    print "lastbytes", lastbytes
    for a in "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz":
     for b in "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz":
      for c in "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz":
       for d in "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz":
        for e in "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz":
         res = hashlib.md5(a+b+c+d+e+salt).hexdigest()
         if res[0:4] == lastbytes:
            return a+b+c+d+e
            
    print "NO CHALL SOL FOUND"
    exit()
    
def check():
    global input_image_name
    try:
        input_image=Image.open(input_image_name)
        std_image=Image.open(std_image_name)
    except:
        print("[-]give me a real image!!")
        sys.stdout.flush()
        return False
    input_image_np=np.array(input_image)
    std_image_np=np.array(std_image)
    input_x=len(input_image_np)
    input_y=len(input_image_np[0])
    input_z=len(input_image_np[0][0])
    std_x=len(std_image_np)
    std_y=len(std_image_np[0])
    std_z=len(std_image_np[0][0])
    print input_x, input_y, input_z
    if std_x!=input_x or std_y!=input_y or std_z!=input_z:
        return False
    diff=0
    for i in range(input_x):
        for j in range(input_y):
            for k in range(input_z):
                if input_image_np[i][j][k]>std_image_np[i][j][k]:
                    diff+=input_image_np[i][j][k]-std_image_np[i][j][k]
                else:
                    diff+=std_image_np[i][j][k]-input_image_np[i][j][k]
    diff=diff/(input_x*input_y*input_z)
    print diff
    if diff>2:
        return False
    return True

std_image_name = "image_f3986b1bfdd95fb594eb059b3cdf1348.jpg"
input_image_name = "edited.jpg"

if not check():
    print "too different"
    exit()
    
sc = socket.create_connection(("202.112.51.176", 9999))

res = solve_chall(sc)
print "found", res
sc.send(res + "\n")
sc.send("team token goes here\n")
print read_until(sc, "[+]Can you fool me?")

img = open(input_image_name, "rb").read()

sc.send(base64.b64encode(img) + "\n")

while True:
    data = sc.recv(16384)
    if len(data) == 0:
        break
    for line in data.split("\n"):
        print repr(line)
    