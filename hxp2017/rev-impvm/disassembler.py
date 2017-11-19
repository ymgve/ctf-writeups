import struct, sys

class Bits(object):
    def __init__(self, s):
        self.s = s
        self.index = 0
        
    def readbit(self):
        bitpos = 7 - (self.index % 8)
        bytepos = self.index / 8
        bit = (ord(self.s[bytepos]) >> bitpos) & 1
        self.index += 1
        return bit
        
    def readbits(self, n):
        res = 0
        for i in xrange(n):
            res = 2 * res + self.readbit()
            
        return res
        
    
data = open(sys.argv[1], "rb").read()

ncodeblocks = struct.unpack(">Q", data[0:8])[0]

splits = []
for i in xrange(ncodeblocks+1):
    offset = struct.unpack(">Q", data[8+i*8:16+i*8])[0]
    splits.append(offset)

for i in xrange(ncodeblocks):
    print "-------------"
    print "function %d" % i
    print "-------------"
    foo = data[splits[i]:splits[i+1]]
    num_instr = struct.unpack(">Q", foo[0:8])[0]
    # x = int(foo[8:].encode("hex"), 16)
    # print bin(x)
    
    b = Bits(foo[8:])
    
    for j in xrange(num_instr):
        op = b.readbits(3)
        # x = bin(x)[2:]
        # x = x.rjust(11, "0")
        # print x
        
        if op == 0:
            arg = b.readbits(8)
            print "jmpz label%d" % arg
        elif op == 1:
            arg = b.readbits(8)
            print "jmp label%d" % arg
        elif op == 2:
            arg = b.readbits(8)
            print "call %d" % arg
        elif op == 3:
            arg = b.readbits(8)
            print "label%d" % arg
        elif op == 4:
            mode = b.readbits(1)
            offset = b.readbits(7)
            if mode == 0:
                print "loadram %d" % offset
            else:
                print "saveram %d" % offset
        elif op == 5:
            mode = b.readbits(1)
            offset = b.readbits(7)
            if mode == 0:
                print "dup %d" % offset
            else:
                print "place %d" % offset
        elif op == 6:
            arg = b.readbits(8)
            print "loadi 0x%02x" % arg
        elif op == 7:
            op2 = b.readbits(3)
            if op2 in (0, 1):
                arg = (op2 & 1) << 5 | b.readbits(5)
                print "shl %d" % arg
            elif op2 in (2, 3):
                arg = (op2 & 1) << 5 | b.readbits(5)
                print "shr %d" % arg
            elif op2 == 4:
                print "neg"
            elif op2 == 5:
                print "and"
            elif op2 == 6:
                print "or"
            elif op2 == 7:
                print "setif s2 >= s1"
            else:
                print "UNKNOWN OP2", bin(op2)
                exit()

        else:
            print "UNKNOWN", bin(op), b.readbits(8)
            break
            
    print
