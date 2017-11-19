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
        
class Function(object):
    def __init__(self, codeseq, labels):
        self.codeseq = codeseq
        self.labels = labels
        
class VMException(Exception):
    pass
    
class VM(object):
    def __init__(self, functions, memory):
        self.functions = functions
        self.memory = memory
        self.funcstack = []
        self.stack = []
        self.currfunc = 0
        self.currip = 0

    def printstate(self):
        print "funcstack", self.funcstack
        print "stack", 
        for val in self.stack:
            print hex(val),
        print
        
        op, op2, arg = self.functions[self.currfunc].codeseq[self.currip]
        print self.currfunc, self.currip, "|", op, op2, arg
        print
    
    def step(self):
        op, op2, arg = self.functions[self.currfunc].codeseq[self.currip]
        #self.printstate()
        do_inc = True
        
        if op == 0:
            if len(self.stack) < 1:
                raise VMException("stack empty")
            
            if self.stack.pop() == 0:
                if arg not in self.functions[self.currfunc].labels:
                    raise VMException("unknown label")
                    
                self.currip = self.functions[self.currfunc].labels[arg]
                do_inc = False
                
        elif op == 1:
            if arg not in self.functions[self.currfunc].labels:
                raise VMException("unknown label")
                
            self.currip = self.functions[self.currfunc].labels[arg]
            do_inc = False
                
        elif op == 2:
            if arg == 252:
                print "challenge init not implemented"
            elif arg == 253:
                print "challenge verification not implemented"
            elif arg == 254:
                print "getchar not implemented"
            elif arg == 255:
                # print "output byte %s" % repr(chr(self.stack[-1] & 0xff))
                sys.stdout.write(chr(self.stack[-1] & 0xff))
                
            else:
                if arg >= len(self.functions):
                    raise VMException("unknown function called")
                    
                self.funcstack.append((self.currfunc, self.currip + 1, len(self.stack)))
                self.currfunc = arg
                self.currip = 0
                do_inc = False
                #self.printstate()
        elif op == 4:
            if op2 == 0:
                if len(self.stack) < 1:
                    raise VMException("stack empty")
                    
                index = self.stack.pop() + arg
                if index >= len(self.memory) or index < 0:
                    raise VMException("memory out of bounds")
                    
                #print "read from mem location %016x %016x" % (index, self.memory[index])
                self.stack.append(self.memory[index])
            else:
                if len(self.stack) < 2:
                    raise VMException("stack empty")
                    
                index = self.stack.pop() + arg
                data = self.stack.pop()
                
                if index >= len(self.memory) or index < 0:
                    raise VMException("memory out of bounds")
                    
                #print "wrote to mem location %016x %016x" % (index, data)
                self.memory[index] = data
                
        elif op == 5:
            if op2 == 0:
                if len(self.stack) < 1:
                    raise VMException("stack empty")
                index = self.stack.pop() + arg + 1
                
                if len(self.stack) < index:
                    raise VMException("stack underflow")
                
                self.stack.append(self.stack[-index])
                
            else:
                if len(self.stack) < 2:
                    raise VMException("stack empty")
                    
                index = self.stack.pop() + arg + 1
                value = self.stack.pop()
                
                if len(self.stack) < index:
                    raise VMException("stack underflow")
                    
                self.stack[-index] = value
                
        elif op == 6:
            self.stack.append(arg)
            
        elif op == 7:
            if op2 == 0:
                if len(self.stack) < 1:
                    raise VMException("stack empty")
                    
                res = (self.stack.pop() << arg) & 0xffffffffffffffff
                self.stack.append(res)
                
            elif op2 == 2:
                if len(self.stack) < 1:
                    raise VMException("stack empty")
                    
                res = self.stack.pop() >> arg
                self.stack.append(res)
                
            elif op2 == 4:
                if len(self.stack) < 1:
                    raise VMException("stack empty")
                    
                res = self.stack.pop() ^ 0xffffffffffffffff
                self.stack.append(res)
                
            elif op2 == 5:
                if len(self.stack) < 2:
                    raise VMException("stack empty")
                    
                val1 = self.stack.pop()
                val2 = self.stack.pop()
                self.stack.append(val1 & val2)
                
            elif op2 == 6:
                if len(self.stack) < 2:
                    raise VMException("stack empty")
                    
                val1 = self.stack.pop()
                val2 = self.stack.pop()
                self.stack.append(val1 | val2)
                
            elif op2 == 7:
                if len(self.stack) < 2:
                    raise VMException("stack empty")
                    
                val1 = self.stack.pop()
                val2 = self.stack.pop()
                if val2 >= val1:
                    self.stack.append(1)
                else:
                    self.stack.append(0)
                    
            else:
                raise VMException("op2 not impl %d" % op2)
        else:
            raise VMException("op not impl %d" % op)
        
        if do_inc:
            self.currip += 1
            
        while self.currip >= len(self.functions[self.currfunc].codeseq):
            if len(self.funcstack) == 0:
                print "program exited"
                return False
                
            if len(self.stack) < 1:
                raise VMException("stack empty")
                    
            self.currfunc, self.currip, stacksize = self.funcstack.pop()
            retval = self.stack.pop()
            self.stack = self.stack[0:stacksize]
            self.stack.append(retval)
            
        return True

data = open(sys.argv[1], "rb").read()

nfuncs = struct.unpack(">Q", data[0:8])[0]

offsets = []
for i in xrange(nfuncs):
    offset = struct.unpack(">Q", data[8+i*8:16+i*8])[0]
    offsets.append(offset)

functions = []

for funcno in xrange(nfuncs):
    codeseq = []
    labels = {}
    bytecode = data[offsets[funcno]:]
    
    b = Bits(bytecode[8:])
    
    num_instr = struct.unpack(">Q", bytecode[0:8])[0]
    for i in xrange(num_instr):
        op = b.readbits(3)
        
        if op in (0, 1, 2, 6):
            arg = b.readbits(8)
            codeseq.append((op, 0, arg))
        elif op == 3:
            arg = b.readbits(8)
            labels[arg] = len(codeseq)
        elif op in (4, 5):
            mode = b.readbits(1)
            offset = b.readbits(7)
            codeseq.append((op, mode, offset))
        else:
            op2 = b.readbits(3)
            if op2 in (0, 1, 2, 3):
                arg = (op2 & 1) << 5 | b.readbits(5)
                codeseq.append((op, op2 & 6, arg))
            elif op2 in (4, 5, 6, 7):
                codeseq.append((op, op2, 0))
            else:
                print "UNKNOWN OP2", bin(op2)
                exit()

    functions.append(Function(codeseq, labels))
    
offset = struct.unpack(">Q", data[8+nfuncs*8:16+nfuncs*8])[0]
numqwords, totalqwords = struct.unpack(">QQ", data[offset:offset+16])

memory = [0] * totalqwords
for i in xrange(numqwords):
    qword = struct.unpack(">Q", data[offset+16+8*i:offset+24+8*i])[0]
    memory[i] = qword
    
vm = VM(functions, memory)

while True:
    cont = vm.step()
    if not cont:
        break
        
# for i in xrange(6):
    # print "%016x" % vm.memory[i]
