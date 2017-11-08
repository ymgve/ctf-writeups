import socket, struct, os, binascii, base64, random, time, itertools
import telnetlib   

try:
    import psyco; psyco.full()
except ImportError:
    pass

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
        self.queue = []
        self.comblimit = 131072
        
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
            
        self.queue.append(idx)
        
        while len(self.queue) > 0:
            idx = self.queue.pop(0)
            a624 = self.gen_a624(idx)
            a623 = self.mt[idx - 623]
            a227 = self.mt[idx - 227]
            a0 = self.mt[idx]
            
            changed = False
            
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
                    
            if changed and len(self.queue) == 0:
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
            
def solve(numbers, target, splitpoint):
    start = time.time()
    
    bitsdict = {}
    gen_subsets_recursive(numbers[:splitpoint], 0, 0, -target, bitsdict)
    print "dictsize", len(bitsdict), "time to build", time.time() - start
    
    return find_answer_recursive(numbers[splitpoint:], 0, 0, 0, bitsdict, splitpoint, numbers)
        
def gen_subsets_recursive(input, depth, bits, summ, res):
    if depth == len(input):
        res[summ] = bits
    else:
        gen_subsets_recursive(input, depth + 1, bits, summ, res)
        gen_subsets_recursive(input, depth + 1, bits | (1 << depth), summ + input[depth], res)

def find_answer_recursive(input, depth, bits, summ, bitsdict, splitpoint, numbers):
    if depth == len(input):
        if -summ in bitsdict:
            answer = []
            for i in xrange(splitpoint):
                if bitsdict[-summ] & (1 << i) != 0:
                    answer.append(numbers[i])
            
            for i in xrange(len(numbers)-splitpoint):
                if bits & (1 << i) != 0:
                    answer.append(numbers[splitpoint+i])
                    
            return answer
        else:
            return None
    else:
        res = find_answer_recursive(input, depth + 1, bits, summ, bitsdict, splitpoint, numbers)
        if res != None:
            return res
        return find_answer_recursive(input, depth + 1, bits | (1 << depth), summ + input[depth], bitsdict, splitpoint, numbers)

def consume_bits(t, bitsleft, bits):
    bits = min(bitsleft, bits)
    mask = ((1 << bits) - 1)
    res = (t >> (bitsleft - bits)) & mask
    return res, bitsleft - bits, bits

def task():
    pred = MTpred()
    # sc = socket.create_connection(("10.0.0.97", 12345))
    sc = socket.create_connection(("54.92.67.18", 50216))

    prob = 1
    while prob <= 30:
        start = time.time()
    
        try:
            read_until(sc, ": ")
        except:
            print "disconnect, probably time limit exceeded"
            return
            
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
                pred.set_value(res, bitsused)
                
            if t < 0:
                 pred.set_value(1, 1)
            else:
                 pred.set_value(0, 1)
                
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
        print "solve for problem size", probsize

        if probsize == 0:
            res2 = []
        elif probsize <= 43:
            res2 = solve(arr2, target2, probsize / 2)
        elif probsize == 50:
            arr2 = arr2[:-4]
            probsize = len(arr2)
            print "NEW PROBLEM SIZE", probsize
            res2 = solve(arr2, target2, 23)
        else:
            print "problem too large"
            sc.close()
            return
            
        if res2 != None:
            print "FOUND, elapsed", time.time() - start
        else:
            print "no answer, elapsed", time.time() - start
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
        print
        
    while True:
        data = sc.recv(16384)
        if len(data) == 0:
            exit()
        for line in data.split("\n"):
            print repr(line)
        
while True:
    print "-----------------------------------------------------------------"
    task()
        

# print solve((1,2,3,4), 6, 2)
#print solve([-14401657914802816692L, -1287355602542416076L, 12420320653421792419L, -18289089911370855220L, 8154750199012466825L, -16975574958611700400L, 2328485991584494208L, -10169372204395520230L, -9148825013174389751L, -9441755996626252807L, 7505124813360736254L, -10679791618967359394L, 15964853472317495255L, -13282327856229625587L, -16622136551977997259L, -14175112237676695222L, -8506337722890397067L, -14688701886578814872L, -5667863163802541984L, 8479616289841584299L, -10502677222669211740L, -12074991642491781841L, -8815572391427830261L, -3122136909004008143L, 6401052931953676445L, 3512894426301976223L, -713490316193477136L, -8800545918834572384L, -17625735858106872866L, -10292913035227393380L, 4709515018989847140L, 7856475123160069118L, 10881453673179168666L, 4920435938773854457L, -5753756767311825361L, -16569511549274683320L, -1976402672757179780L, -6296705733442779413L, -17139681844815308426L, -7388158026819514253L, -12858641108224236354L, -7186175713134030864L], -158858050467640791970, 21)
