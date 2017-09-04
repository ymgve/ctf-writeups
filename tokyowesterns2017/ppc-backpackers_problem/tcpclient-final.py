import socket, struct, os, binascii, base64, random, itertools, time
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


# MT19937 implementation based on https://en.wikipedia.org/wiki/Mersenne_Twister#Python_implementation
def _int32(x):
    # Get the 32 least significant bits.
    return int(0xFFFFFFFF & x)

class MT19937:
    def __init__(self, seed, initial_array=624):
        # Initialize the index to 0
        self.index = 624
        self.mt = [0] * 624
        self.mt[0] = seed  # Initialize the initial state to the seed
        for i in range(1, initial_array):
            self.mt[i] = _int32(
                1812433253 * (self.mt[i - 1] ^ self.mt[i - 1] >> 30) + i)

    def extract_number(self, temper=True):
        if self.index >= 624:
            self.twist()

        y = self.mt[self.index]

        if temper:
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

# generate all subset sums of the given set
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
    
# solve subset sum with meet-in-the-middle
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

# untempering function from https://github.com/kmyk/mersenne-twister-predictor/blob/master/predict.py
def untempering(y):
    y ^= (y >> 18)
    y ^= (y << 15) & 0xefc60000
    y ^= ((y <<  7) & 0x9d2c5680) ^ ((y << 14) & 0x94284000) ^ ((y << 21) & 0x14200000) ^ ((y << 28) & 0x10000000)
    y ^= (y >> 11) ^ (y >> 22)
    return y
  
def get_seeds(m0, m227):
    seeds = []
    
    # original lower bit of y could have been either 0 or 1
    y_even = (m227 ^ m0) << 1
    y_odd = (((m227 ^ m0 ^ 0x9908b0df) << 1) & 0xffffffff) | 1
    
    for y in (y_even, y_odd):
        # original upper bit of mt227 and mt228 could have been either 0 or 1
        for oldm227_upperbit in (0, 0x80000000):
            for oldm228_upperbit in (0, 0x80000000):
                n = y ^ oldm227_upperbit ^ oldm228_upperbit
                
                # invert the initial MT array function
                for i in xrange(228, 0, -1):
                    n = ((n - i) * 2520285293) & 0xffffffff
                    n = n ^ (n >> 30)
                    
                seeds.append(n)
    return seeds

def find_valid_seed(pool1, pool3, fullpool):
    for i in xrange(len(pool1)):
        for j in xrange(len(pool3)):
            a = pool1[i]
            b = pool3[j]
            
            res = get_seeds(a, b)
            for seed in res:
                mt = MT19937(seed, 400)     # speed hack, only partially make initial array
                mt.twist_small()            # speed hack, don't do a full initial twist
                good = 0
                for k in xrange(3):
                    if mt.extract_number(False) in fullpool:    # speed hack, don't temper
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
        
    # since the server RNG initially fills all 128 bits and the following 28 bit shift
    # is arithmetic, not logical, we gotta ensure it has the right sign
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
        for n in n2, -n2:
            n = n >> 4

            # for each number, 3 complete PRNG output values are recovered
            a = (n >> 64) & 0xffffffff
            b = (n >> 32) & 0xffffffff
            c = (n >>  0) & 0xffffffff
            
            if i == 0:
                # mt0 must be the first PRNG value of some number in the first problem set
                pool1.append(untempering(a))
            
                # save all the others for later validation of the correct seed
                fullpool.add(untempering(a))
                fullpool.add(untempering(b))
                fullpool.add(untempering(c))
            
            elif i == 2:
                # mt227 must be the third PRNG value of some number in the third problem set
                pool3.append(untempering(c))
        
    # properly solve the three first challenges
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
    # generate all the problem sets we've already seen
    gen_problem(i, mt)

for i in xrange(4, 21):
    print read_until(sc, "Input: \n")
    line = readline(sc, False)
    
    # we totally solved the NP problem, guys
    ret, answer = gen_problem(i, mt)

    # sort and send
    res = " ".join(str(x) for x in sorted(answer))
    sc.send(str(len(answer)) + " " + res + "\n")

while True:
    data = sc.recv(16384)
    if len(data) == 0:
        break
    for line in data.split("\n"):
        print repr(line)
    