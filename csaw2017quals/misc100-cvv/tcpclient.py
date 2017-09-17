import socket, struct, os, binascii, base64, random
import telnetlib   

from ccn import *

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

def validate_number(ccnumber):
    sum = 0
    pos = 0
    length = len(ccnumber)
    
    reversedCCnumber = []
    reversedCCnumber.extend(list(ccnumber[:-1]))
    reversedCCnumber.reverse()

    while pos < length - 1:

        odd = int(reversedCCnumber[pos]) * 2
        if odd > 9:
            odd -= 9

        sum += odd

        if pos != (length - 2):

            sum += int(reversedCCnumber[pos + 1])

        pos += 2

    checkdigit = ((sum / 10 + 1) * 10 - sum) % 10
    
    return ccnumber[-1] == str(checkdigit)

    
sc = socket.create_connection(("misc.chal.csaw.io", 8308))

generator = Random()
generator.seed()        # Seed from current time

while True:
    line = readline(sc)
    if "MasterCard" in line:
        res = credit_card_number(generator, mastercardPrefixList, 16, 1)[0]
    elif "Visa" in line:
        res = credit_card_number(generator, visaPrefixList, 16, 1)[0]
    elif "American Express" in line:
        res = credit_card_number(generator, amexPrefixList, 15, 1)[0]
    elif "Discover" in line:
        res = credit_card_number(generator, discoverPrefixList, 16, 1)[0]
    elif "I need a new card that starts with" in line:
        prefix = line.split("I need a new card that starts with ")[1].split("!")[0]
        res = credit_card_number(generator, [list(prefix)], 16, 1)[0]
    elif "I need a new card which ends with" in line:
        postfix = line.split("I need a new card which ends with ")[1].split("!")[0]
        while True:
            res = credit_card_number(generator, mastercardPrefixList, 16, 1)[0]
            if res.endswith(postfix):
                break
    elif "I need to know if" in line:
        cc = line.split("I need to know if ")[1].split(" is valid!")[0]
        if validate_number(cc):
            res = "1"
        else:
            res = "0"
    else:
        res = "BAD"
    print repr(res)
    
    sc.send(res + "\n")
    while line != "Thanks!":
        line = readline(sc)
        
        
# t = telnetlib.Telnet()                                                  
# t.sock = sc
# t.interact()  

while True:
    data = sc.recv(16384)
    if len(data) == 0:
        break
    for line in data.split("\n"):
        print repr(line)
    
    
# flag{ch3ck-exp3rian-dat3-b3for3-us3}