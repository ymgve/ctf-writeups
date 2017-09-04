import socket, struct, os, binascii, base64, random, itertools, time
import telnetlib   

def _int32(x):
    # Get the 32 least significant bits.
    return int(0xFFFFFFFF & x)

class MT19937:
    def __init__(self, seed):
        # Initialize the index to 0
        self.index = 624
        self.mt = [0] * 624
        self.mt[0] = seed  # Initialize the initial state to the seed
        for i in range(1, 624):
            self.mt[i] = _int32(
                1812433253 * (self.mt[i - 1] ^ self.mt[i - 1] >> 30) + i)

    def extract_number(self):
        if self.index >= 624:
            self.twist()

        y = self.mt[self.index]

        # Right shift by 11 bits
        y = y ^ y >> 11
        # Shift y left by 7 and take the bitwise and of 2636928640
        y = y ^ y << 7 & 2636928640
        # Shift y left by 15 and take the bitwise and of y and 4022730752
        y = y ^ y << 15 & 4022730752
        # Right shift by 18 bits
        y = y ^ y >> 18

        self.index = self.index + 1

        return _int32(y)

    def twist(self):
        for i in range(624):
            # Get the most significant bit and add it to the less significant
            # bits of the next number
            y = _int32((self.mt[i] & 0x80000000) +
                       (self.mt[(i + 1) % 624] & 0x7fffffff))
            self.mt[i] = self.mt[(i + 397) % 624] ^ y >> 1

            if y % 2 != 0:
                self.mt[i] = self.mt[i] ^ 0x9908b0df
        self.index = 0

    def twist_small(self):
        for i in range(3):
            # Get the most significant bit and add it to the less significant
            # bits of the next number
            y = _int32((self.mt[i] & 0x80000000) +
                       (self.mt[(i + 1) % 624] & 0x7fffffff))
            self.mt[i] = self.mt[(i + 397) % 624] ^ y >> 1

            if y % 2 != 0:
                self.mt[i] = self.mt[i] ^ 0x9908b0df
        self.index = 0
        
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

def gen_subsets(input):
    half = len(input)
    res = []
    bits = {}
    
    for i in xrange(1, 1 << half):
        total = 0
        for j in xrange(half):
            if i & (1 << j) != 0:
                total = (total + input[j])
        res.append(total)
        bits[total] = i
        
    return res, bits
    
def solve(numbers):
    half = len(numbers)/ 2
    
    input1 = numbers[:half]
    res1, bits1 = gen_subsets(input1)
    set1 = set(res1)
    
    input2 = [-x for x in numbers[half:]]
    res2, bits2 = gen_subsets(input2)
    set2 = set(res2)
    
    common = list(set1.intersection(set2))[0]
    
    answer = []
    
    for i in xrange(half):
        if bits1[common] & (1 << i) != 0:
            answer.append(numbers[i])
    
    for i in xrange(half):
        if bits2[common] & (1 << i) != 0:
            answer.append(numbers[half+i])
            
    return answer

def untempering(y):
    y ^= (y >> 18)
    y ^= (y << 15) & 0xefc60000
    y ^= ((y <<  7) & 0x9d2c5680) ^ ((y << 14) & 0x94284000) ^ ((y << 21) & 0x14200000) ^ ((y << 28) & 0x10000000)
    y ^= (y >> 11) ^ (y >> 22)
    return y
  
def get_seeds(m227, m0):
    m227 = untempering(m227)
    m0 = untempering(m0)
    res = []
    y1 = (m227 ^ m0) << 1
    y2 = (((m227 ^ m0 ^ 0x9908b0df) << 1) & 0xffffffff) | 1
    for y0 in (y1, y2):
        for extrabit in (0, 0x80000000):
            y = y0 ^ extrabit
            for i in xrange(228, 0, -1):
                y = ((y - i) * 2520285293) & 0xffffffff
                y = y ^ (y >> 30)
                
            res.append(y)
        
    return res

def find_valid_seed(pool1, pool3, fullpool):
    for i in xrange(len(pool1)):
        for j in xrange(len(pool3)):
            a = pool1[i]
            b = pool3[j]
            
            res = get_seeds(a, b)
            for seed in res:
                mt = MT19937(seed)
                mt.twist_small()
                good = 0
                for k in xrange(3):
                    if mt.extract_number() in fullpool:
                        good += 1
                    else:
                        break
                        
                if good == 3:
                    return seed
            
    return None

def rand(mt):
    r = 0
    for i in xrange(4):
        r = (r << 32) | mt.extract_number()
        
    if (r >> 127) == 1:
        r = r - (1 << 128)
        
    r = r >> 28
    
    if mt.extract_number() & 1 == 1:
        r = -r

    return r
        
def gen_problem(problem_no, mt):
    n = problem_no * 10
    m = n / 2
    while True:
        ret = []
        tmp = 0
        for i in xrange(m - 1):
            ret.append(rand(mt))
            tmp = (tmp - ret[-1]) & 0xffffffffffffffffffffffffffffffff
            if (tmp >> 127) == 1:
                tmp = tmp - (1 << 128)

        if tmp < 0 and ((-tmp) >> 100) > 0:
            continue
        if tmp > 0 and (tmp >> 100) > 0:
            continue
            
        ret.append(tmp)
        answer = list(ret)
        
        for i in xrange(m):
            ret.append(rand(mt))

        return sorted(ret), sorted(answer)
    
sc = socket.create_connection(("backpacker.chal.ctf.westerns.tokyo", 39581))
# sc = socket.create_connection(("10.0.0.97", 12345))

fullpool = set()
pool1 = []
pool3 = []
for i in xrange(3):
    print read_until(sc, "Input: \n")
    line = readline(sc, False)

    numbers = [int(x) for x in line.split()[1:]]

    for n2 in numbers:
        n2 = int(n2)
        for n in n2, -n2:
            n = n >> 4
            
            a = (n >> 64) & 0xffffffff
            b = (n >> 32) & 0xffffffff
            c = (n >>  0) & 0xffffffff
            
            fullpool.add(a)
            fullpool.add(b)
            fullpool.add(c)
            
            if i == 0:
                pool1.append(a)
            
            elif i == 2:
                pool3.append(c)
        
    answer = solve(numbers)

    res = " ".join(str(x) for x in sorted(answer))

    sc.send(str(len(answer)) + " " + res + "\n")
    
seed = find_valid_seed(pool1, pool3, fullpool)
if seed is None:
    print "NO SEED FOUND"
    exit()
    
print "seed", seed
mt = MT19937(seed)
for i in (1,2,3):
    gen_problem(i, mt)

for i in xrange(4, 21):
    print read_until(sc, "Input: \n")
    line = readline(sc, False)
    
    ret, answer = gen_problem(i, mt)

    res = " ".join(str(x) for x in sorted(answer))
    sc.send(str(len(answer)) + " " + res + "\n")

while True:
    data = sc.recv(16384)
    if len(data) == 0:
        break
    for line in data.split("\n"):
        print repr(line)
    