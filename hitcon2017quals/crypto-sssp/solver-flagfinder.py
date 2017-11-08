import socket, struct, os, binascii, base64, random, time
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

def _int32(x):
    # Get the 32 least significant bits.
    return int(0xFFFFFFFF & x)

def untempering(y):
    y ^= (y >> 18)
    y ^= (y << 15) & 0xefc60000
    y ^= ((y <<  7) & 0x9d2c5680) ^ ((y << 14) & 0x94284000) ^ ((y << 21) & 0x14200000) ^ ((y << 28) & 0x10000000)
    y ^= (y >> 11) ^ (y >> 22)
    return y

def tempering(y):
    y ^= (y >> 11)
    y ^= (y << 7) & 2636928640
    y ^= (y << 15) & 4022730752
    y ^= (y >> 18)
    return y

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
        #test
        
class MT19937_2:
    def __init__(self, seed):
        self.index = 624
        self.mt = [0] * 624
        self.mt[0] = seed  # Initialize the initial state to the seed
        for i in range(1, 624):
            self.mt[i] = _int32(
                1812433253 * (self.mt[i - 1] ^ self.mt[i - 1] >> 30) + i)

    def extract_number(self):
        y = _int32((self.mt[self.index - 624] & 0x80000000) +
                   (self.mt[self.index - 623] & 0x7fffffff))
        x = self.mt[self.index - 227] ^ (y >> 1)

        if y % 2 != 0:
            x ^= 0x9908b0df
            
        self.mt.append(x)
        self.index = self.index + 1
        
        return tempering(x)

        
def gen_cand(v, bits):
    cand = []
    if bits == 32:
        cand.append(untempering(v))
    elif bits == 28:
        for i in xrange(16):
            cand.append(untempering(v | (i << 28)))
    elif bits == 24:
        for i in xrange(256):
            cand.append(untempering(v | (i << 24)))
    elif bits == 20:
        for i in xrange(4096):
            cand.append(untempering(v | (i << 20)))
    elif bits == 16:
        for i in xrange(65536):
            cand.append(untempering(v | (i << 16)))
    
    return cand
    
            
class MTpred(object):
    def __init__(self):
        self.mt = [None] * 624
        self.index = 0
        
    def get_value(self):
        v1 = self.mt[(self.index + 1) % 624]
        v397 = self.mt[(self.index + 397) % 624]
        #if v1 is not None and v397 is not None and len(v1) <= 512 and len(v397) <= 512:
        if v1 is not None and v397 is not None and len(v1) * len(v397) <= 2048*2048:
            #print "xxxxx", self.index
            #print "CAN POSSIBLY EXTRACT VALUE", len(v1), len(v397)
            if self.mt[self.index] is None:
                v0 = (0, 0x80000000)
            else:
                v0 = set()
                for v0t in self.mt[self.index]:
                    v0.add(v0t & 0x80000000)
                
            cands = set()
            for v0t in v0:
                for v1t in v1:
                    for v397t in v397:
                        #print hex(v0t), hex(v1t), hex(v397t)
                        y = _int32((v0t & 0x80000000) +
                                   (v1t & 0x7fffffff))
                        res = v397t ^ y >> 1

                        if y % 2 != 0:
                            res ^= 0x9908b0df
                        
                        cands.add(res)

                        
            return list(cands)
        else:
            return None
            
            #exit()
                    
                    
            # if v0 is not None:
                # print "EVEN BETTER - GUARANTEED", v0
                #exit()

            # y = _int32((v0 & 0x80000000) +
                       # (v1 & 0x7fffffff))
            # res = v397 ^ y >> 1

            # if y % 2 != 0:
                # res ^= 0x9908b0df
               
            # self.mt[self.index] = res
            # print "CORRECT VALUE %08x" % tempering(res)
            # return tempering(res)
            
        # else:
            # return None
                    
                # print "CAN POSSIBLY EXTRACT VALUE", self.mt[(self.index + 1) % 624], self.mt[(self.index + 397) % 624]
                # if self.mt[self.index] is not None:
                    # print "EVEN BETTER - GUARANTEED"
    
    def set_value(self, value, bits):
        #print "setting %08x %d index %d" % (value, bits, self.index)
        if bits >= 24:
            cc = gen_cand(value, bits)
            v1 = self.mt[(self.index + 1) % 624]
            v397 = self.mt[(self.index + 397) % 624]
            if v1 != None:
                if len(v1) <= 4096:
                    print "BACKPROP"
                    
                    if self.mt[self.index] is None:
                        v0 = (0, 0x80000000)
                    else:
                        v0 = set()
                        for v0t in self.mt[self.index]:
                            v0.add(v0t & 0x80000000)
                    
                    cands = set()
                    for v0t in v0:
                        for v1t in v1:
                            for t in cc:
                                y = _int32((v0t & 0x80000000) +
                                           (v1t & 0x7fffffff))
                                
                                if y % 2 != 0:
                                    t ^= 0x9908b0df
                                v397t = t ^ (y >> 1)
                                
                                cands.add(v397t)
                            
                    if v397 == None:
                        res = list(cands)
                    else:
                        res = []
                        for cand in cands:
                            if cand in v397:
                                res.append(cand)
                                
                    self.mt[(self.index + 397) % 624] = res
                
            elif v397 != None:
                if len(v397) <= 4096:
                    print "BACKPROP 2"
                    if self.mt[self.index] is None:
                        v0 = (0, 0x80000000)
                    else:
                        v0 = set()
                        for v0t in self.mt[self.index]:
                            v0.add(v0t & 0x80000000)
                    
                    cands = set()
                    for v397t in v397:
                        for extrabit in (0, 1):
                            for upperbit in (0, 0x80000000):
                                for t in cc:
                                    if extrabit == 1:
                                        t ^= 0x9908b0df
                                        
                                    t ^= v397t
                                    if t & 0x80000000:
                                        continue
                                        
                                    t = ((t << 1) | extrabit) ^ upperbit
                                    
                                    cands.add(t)
                                
                    if v1 == None:
                        res = list(cands)
                    else:
                        res = []
                        for cand in cands:
                            if cand in v1:
                                res.append(cand)
                                
                    self.mt[(self.index + 1) % 624] = res
                
            # foo2 = self.mt[(self.index) % 624]
            # if foo2 != None and len(foo2) == 1:
                # print "CERTAIN BACKPROP"
                # exit()
            
        cands = self.get_value()
        if cands is None:
            if bits < 20:
                self.mt[self.index] = None
            else:
                self.mt[self.index] = gen_cand(value, bits)
        else:
            if bits == 0:
                self.mt[self.index] = cands
            else:
                mask = (1 << bits) - 1
                cands2 = set()
                for cand in cands:
                    if (tempering(cand) & mask) == (value & mask):
                        cands2.add(cand)

                        
                # print "filtered from %d to %d with %d bits" % (len(cands), len(cands2), bits)
                # for x in cands:
                    # print "%08x " % tempering(x),
                # print
                # print "--"
                self.mt[self.index] = list(cands2)
                if bits == 32:
                    assert tempering(self.mt[self.index][0]) == value
                
                if len(cands2) == 0:
                    exit()
                    
    def advance(self, n):
        self.index = (self.index + n) % 624
        
        # if bits == 32:
            # self.mt[self.index] = [untempering(value)]
            
class MTpred2(object):
    def __init__(self):
        self.mt = [None] * 624
        self.queue = []
        self.comblimit = 16384
        
    def gen_a624(self, idx):
        a624 = self.mt[idx - 624]
        if a624 is None:
            return (0, 0x80000000)
        else:
            a624temp = set()
            for v624 in a624:
                a624temp.add(v624 & 0x80000000)

            return a624temp

    def calc_value0(self, idx):
        a623 = self.mt[idx - 623]
        a227 = self.mt[idx - 227]
        
        a624 = self.gen_a624(idx)
            
        if a623 != None and a227 != None:
            #print idx, len(a623), len(a227)
            if len(a623) * len(a227) <= self.comblimit:
                cands = set()
                for v624 in a624:
                    for v623 in a623:
                        for v227 in a227:
                            y = (v624 & 0x80000000) | (v623 & 0x7fffffff)
                            x = v227 ^ y >> 1
                            if y & 1 == 1:
                                x ^= 0x9908b0df
                            
                            cands.add(x)
        
                return cands
            # else:
                # print "TOO BIG"
            
        return None
    
    def set_value(self, value, bits):
        idx = len(self.mt)
        cands = self.calc_value0(idx)

        if cands == None:
            if bits >= 24:
                self.mt.append(gen_cand(value, bits))
            else:
                self.mt.append(None)
        else:
            mask = (1 << bits) - 1
            cands2 = set()
            for cand in cands:
                if (tempering(cand) & mask) == (value & mask):
                    cands2.add(cand)
        
            self.mt.append(list(cands2))
            
            # if len(cands2) < len(cands):
                # print "filtered with value %08x bits %d from %d to %d" % (value, bits, len(cands), len(cands2))
                
            
        self.queue.append(idx)
        self.eval_queue()
        
    def filter_values(self, values, mask):
        idx = len(self.mt)
        cands = self.calc_value0(idx)

        if cands == None:
            self.mt.append(None)
        else:
            cands2 = set()
            for cand in cands:
                for value in values:
                    if (tempering(cand) & mask) == (value & mask):
                        cands2.add(cand)
        
            self.mt.append(list(cands2))
            
            self.queue.append(idx)
            self.eval_queue()
            
    def eval_queue(self):
        first = True
        while len(self.queue) > 0:
            idx = self.queue.pop(0)
            a624 = self.gen_a624(idx)
            a623 = self.mt[idx - 623]
            a227 = self.mt[idx - 227]
            a0 = self.mt[idx]
            
            changed = False
            
            if first:
                first = False
            else:
                cands = self.calc_value0(idx)
                if cands != None:
                    if a0 == None:
                        res = list(cands)
                    else:
                        res = []
                        for cand in a0:
                            if cand in cands:
                                res.append(cand)
                                
                    if a0 == None or len(res) < len(a0):
                        self.mt[idx] = res
                        changed = True
                
            if a623 != None and a0 != None:
                if len(a623) * len(a0) <= self.comblimit:
                    cands = set()
                    for v624 in a624:
                        for v623 in a623:
                            for v0 in a0:
                                y = (v624 & 0x80000000) | (v623 & 0x7fffffff)
                                if y & 1 == 1:
                                    v0 ^= 0x9908b0df
                                    
                                cands.add(v0 ^ (y >> 1))
                                
                    if len(cands) == 0:
                        print "WTFFF"
                        exit()
                        
                    if a227 == None:
                        res = list(cands)
                    else:
                        res = []
                        for cand in a227:
                            if cand in cands:
                                res.append(cand)

                    if a227 == None or len(res) < len(a227):
                        self.mt[idx - 227] = res
                        changed = True
                # else:
                    # print "TOO BIG a623 a0", len(a623), len(a0), len(self.queue)
            
            if a227 != None and a0 != None:
                if len(a227) * len(a0) <= self.comblimit:
                    cands = set()
                    for v227 in a227:
                        for extrabit in (0, 1):
                            for upperbit in (0, 0x80000000):
                                for v0 in a0:
                                    t = v0
                                    if extrabit == 1:
                                        t ^= 0x9908b0df
                                        
                                    t ^= v227
                                    
                                    if t & 0x80000000:
                                        continue
                                        
                                    t = ((t << 1) | extrabit) ^ upperbit
                                    
                                    cands.add(t)
                                
                    if len(cands) == 0:
                        print "WTFFF"
                        exit()
                        
                    if a623 == None:
                        res = list(cands)
                    else:
                        res = []
                        for cand in a623:
                            if cand in cands:
                                res.append(cand)

                    if a623 == None or len(res) < len(a623):
                        self.mt[idx - 623] = res
                        changed = True
                # else:
                    # print "TOO BIG a227 a0", len(a227), len(a0), len(self.queue)
                    
            if changed and len(self.queue) < 200:
                if idx >= 624 + 227:
                    self.queue.append(idx - 227)
                if idx >= 624 + 623:
                    self.queue.append(idx - 623)
                if idx >= 624 + 624:    
                    self.queue.append(idx - 624)
                if idx + 1 < len(self.mt):
                    self.queue.append(idx + 1)
                if idx + 397 < len(self.mt):
                    self.queue.append(idx + 397)
                if idx + 624 < len(self.mt):
                    self.queue.append(idx + 624)
                    
            #print "qqqq", len(self.queue)
            
            
def gen_subsets(input, offset = 0):
    half = len(input)
    res = []
    bits = {}
    
    for i in xrange(1, 1 << half):
        total = offset
        for j in xrange(half):
            if i & (1 << j) != 0:
                total = (total + input[j])
        res.append(total)
        bits[total] = i
        
    return res, bits
    
def solve(numbers, target):
    half = len(numbers) / 2
    
    input1 = numbers[:half]
    res1, bits1 = gen_subsets(input1)
    set1 = set(res1)
    
    input2 = [-x for x in numbers[half:]]
    res2, bits2 = gen_subsets(input2, target)
    set2 = set(res2)
    
    common = list(set1.intersection(set2))[0]
    
    answer = []
    
    for i in xrange(half):
        if bits1[common] & (1 << i) != 0:
            answer.append(numbers[i])
    
    for i in xrange(len(numbers)-half):
        if bits2[common] & (1 << i) != 0:
            answer.append(numbers[half+i])
            
    return answer

def solve3(numbers, target, set1size, set2size):
    start = time.time()
    print "."
    
    input1 = numbers[:set1size]
    res1, bits1 = gen_subsets(input1)
    set1 = set(res1)
    
    print ".", len(set1)
    
    input2 = numbers[set1size:set1size+set2size]
    res2, bits2 = gen_subsets(input2)
    set2 = set(res2)
    
    print ".", len(set2)
    
    input3 = [-x for x in numbers[set1size+set2size:]]
    res3, bits3 = gen_subsets(input3)
    set3 = set(res3)
    
    print ".", len(set3)
    
    for a in res1:
        for b in res2:
            if a + b - target in set3:
                print "FOUND"
                print "elapsed", time.time() - start

                answer = []
                
                for i in xrange(set1size):
                    if bits1[a] & (1 << i) != 0:
                        answer.append(numbers[i])
                
                for i in xrange(set2size):
                    if bits2[b] & (1 << i) != 0:
                        answer.append(numbers[set1size+i])
                        
                for i in xrange(len(numbers)-(set1size+set2size)):
                    if bits3[a + b - target] & (1 << i) != 0:
                        answer.append(numbers[set1size+set2size+i])
                        
                return answer
                
    print "no answer, elapsed", time.time() - start
                
def consume_bits(t, bitsleft, bits):
    bits = min(bitsleft, bits)
    mask = ((1 << bits) - 1)
    res = (t >> (bitsleft - bits)) & mask
    return res, bitsleft - bits, bits
    
# randcalls = 0
# for i in xrange(1, 30):
    # n = 4 * i + 7
    # m = min(4 * i + 20, 120)
    # rnds_per_val = (m + 31) / 32
    # randcalls += (rnds_per_val + 1) * n
    # randcalls += n * 2
    # print i, randcalls, rnds_per_val, m % 32
    
# seed = random.getrandbits(32)
# mt = MT19937(0)
# mt2 = MT19937_2(0)

if False:
    seed = random.getrandbits(32)
    mt = MT19937_2(seed)
    pred = MTpred2()

    for i in xrange(1, 30):
        n = 4 * i + 7
        m = min(4 * i + 20, 120)
        for j in xrange(n):
            mm = m
            while mm != 0:
                w = min(mm, 32)
                mask = (1 << w) - 1
                r = mt.extract_number() & mask
                pred.set_value(r, w)
                #print "%08x" % r,
                mm -= w
                
            r = mt.extract_number() & 0x80000001
            #print "%08x" % r
            # if r == 1:
                # pred.filter_values((1,), 0x80000001)
            # else:
                # pred.filter_values((0, 0x80000000, 0x80000001), 0x80000001)
            pred.set_value(r, 0)
                
        for j in xrange(n):
            r = mt.extract_number() & 1
            #print "%08x" % r
            pred.set_value(r, 1)
            
    count = 0
    perfect = 0
    total = 0
    s = ""
    for i in xrange(len(pred.mt)):
        if pred.mt[i] != None:
            assert mt.mt[i] in pred.mt[i]
            count += 1
            if len(pred.mt[i]) == 1:
                perfect += 1
                s += "*"
            else:
                s += "."
        else:
            s += " "
            
        total += 1
        
    print "total", total
    print "verified", count
    print "perfect", perfect
    print s
    exit()
# for i in xrange(100000):
    # assert mt.extract_number() == mt2.extract_number()
# exit()

# pred = MTpred()

# for i in xrange(624):
    # t = mt.extract_number()

# for i in xrange(1000):
    # for ii in xrange(100):
        # t = mt.extract_number()
        # if random.getrandbits(1) == 1:
            # pred.set_value(t, 32)
        # else:
            # pred.set_value(t, 0)
            
        # if random.getrandbits(2) == 1:
            # b = random.choice((32, 28, 24, 16, 8, 1, 1))
            # pred.set_value(t, b)
        # else:
            # pred.set_value(t, 0)
        
        # pred.advance(1)
        
    # count = 0
    # for j in xrange(624):
        # if pred.mt[j] != None and len(pred.mt[j]) == 1:
            # count += 1
            
    # print count
    # print mt.index-1, mt.mt[mt.index-1]
    # print pred.index, pred.mt[pred.index]
    
# for j in xrange(624):
    # if pred.mt[j] != None:
        # if mt.mt[j] not in pred.mt[j]:
            # print "WTFF", i, j
            # print mt.mt[j]
            # print pred.mt[j]
            # exit()
    
#print pred.mt
#exit()

def task():
    pred = MTpred2()
    # sc = socket.create_connection(("10.0.0.97", 12345))
    sc = socket.create_connection(("54.92.67.18", 50216))

    prob = 1
    while prob <= 30:
        read_until(sc, ": ")
        res = readline(sc, False).split()
        target = int(res[0])
        arr = [int(x) for x in res[2:]]
        print "problem %d size %d" % (prob, len(arr)),
        n = 4 * prob + 7
        assert n == len(arr)
        
        for t in arr:
            tt = abs(t)
            bitsleft = min(4 * prob + 20, 120)
            while bitsleft > 0:
                res, bitsleft, bitsused = consume_bits(tt, bitsleft, 32)
                #print hex(res), bitsused
                pred.set_value(res, bitsused)
                # mtindex = (mtindex + 1) % 624
                
            if t < 0:
                 pred.set_value(1, 1)
            else:
                 pred.set_value(0, 1)
                
            # mtindex = (mtindex + 1) % 624
            
        res = []
        arr2 = []
        target2 = target
        
        savedstate = list(pred.mt)
        
        for v in arr:
            cands = pred.calc_value0(len(pred.mt))
            pred.set_value(0, 0)
            
            if cands is not None:
                weight = [0, 0]
                for cand in cands:
                    weight[tempering(cand) & 1] += 1
                
                #print weight, v
                if weight[0] == 0 and weight[1] != 0:
                    res.append(v)
                    target2 -= v
                elif weight[0] != 0 and weight[1] == 0:
                    pass
                else:
                    arr2.append(v)
            else:
                arr2.append(v)
        
        probsize = len(arr2)
        print "SOLVE FOR NUMBER OF BITS", probsize
        if probsize == 0:
            res2 = []
        elif probsize <= 32:
            try:
                res2 = solve(arr2, target2)
            except IndexError:
                print "crash in solver, retrying"
                sc.close()
                return
        elif probsize <= 43:
            large = 18
            small = (probsize - large) / 2
            res2 = solve3(arr2, target2, small, probsize - large - small)
        elif probsize <= 47:
            large = 20
            small = (probsize - large) / 2
            res2 = solve3(arr2, target2, small, probsize - large - small)
        elif probsize <= 52:
            arr2 = arr2[:-7]
            probsize = len(arr2)
            large = 20
            small = (probsize - large) / 2
            res2 = solve3(arr2, target2, small, probsize - large - small)
            if res2 is None:
                print "no solution"
                sc.close()
                return
                
        else:
            print "problem too large"
            sc.close()
            return
            
        res.extend(res2)

        pred.mt = savedstate
        
        res3 = []
        for v in arr:
            if v in res:
                res3.append(v)
                pred.set_value(1, 1)
            else:
                pred.set_value(0, 1)
                
        sc.send(str(len(res3)) + " " + " ".join([str(x) for x in res3]) + "\n")
        prob += 1
        
        
    # t = telnetlib.Telnet()                                                  
    # t.sock = sc
    # t.interact()  

    while True:
        data = sc.recv(16384)
        if len(data) == 0:
            break
        for line in data.split("\n"):
            print repr(line)
        
while True:
    print "-----------------------------------------------------------------"
    try:
        task()
    except:
        pass