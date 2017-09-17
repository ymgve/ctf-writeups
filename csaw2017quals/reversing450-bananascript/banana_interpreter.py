import sys

ab = "6162636465666768696a6b6c6d6e6f707172737475767778797a4142434445464748494a4b4c4d4e4f505152535455565758595a200a303132333435363738392c2e2f3b275b5d3d2d607e21402324255e262a28295f2b7b7d7c5c3a223f3e3c0000000000000000000000000000000000000000000000000000000000000000".decode("hex")

def b2i(s):
    n = 0
    for c in s:
        n = n * 2
        if c in "bans":
            n |= 1
            
    return n

def i2b(n):
    s = ""
    for i in xrange(7):
        if (n >> (6 - i)) & 1:
            s += "bananas"[i]
        else:
            s += "BANANAS"[i]
            
    return s
        
def reg2i(r):
    n = 0
    for t in r:
        n += t ^ 0x7f
        
    return n
    
def get_reg(s):
    assert s.startswith("banA")
    return b2i(s) & 7

def reg2s(r):
    s = ""
    for n in r:
        s += ab[n]
        
    return s

class BananaVM(object):
    def __init__(self):
        self.regs = [None] * 16
        
    def run(self, filename, fakestdin):
        self.program = []
        self.fakestdin = fakestdin
        
        for line in open(filename, "rb"):
            cmd = line.strip().split()
            self.program.append(cmd)
            
        self.ip = 0
        
        while self.ip < len(self.program):
            print "%05d" % self.ip,
            cmd = self.program[self.ip]
            
            if cmd[0] == "bananas":
                if cmd[1].startswith("banA"):
                    src = get_reg(cmd[1])
                    self.print_register(src)
                elif cmd[1] == "bananAS":
                    if cmd[2].startswith("banA"):
                        src = 8 + get_reg(cmd[2])
                        self.print_register(src)
                    else:
                        print "UNSUPPORTED", repr(cmd)
                        raise Exception
                else:
                    print "UNSUPPORTED", repr(cmd)
                    raise Exception
                    
            elif cmd[0] == "bananaS":
                if cmd[1].startswith("banA"):
                    dest = get_reg(cmd[1])
                    self.read_stdin(dest)
                else:
                    print "UNSUPPORTED", repr(cmd)
                    raise Exception
                
            elif cmd[0] == "bananAs":
                if cmd[1] == "bananAS" and cmd[2].startswith("banA"):
                    src = get_reg(cmd[2]) + 8
                    print "NEWIP r%d" % src
                    ip_offset = int(reg2s(self.regs[src])) - 1
                    self.ip += ip_offset
                else:
                    print "UNSUPPORTED", repr(cmd)
                    raise Exception
                
            elif cmd[0] == "bananAS":
                if cmd[1].startswith("banA"):
                    dest = 8 + get_reg(cmd[1])
                    if cmd[2] == "baNanas":
                        if cmd[3] != "bananAS":
                            self.load_register(dest, cmd[3:])
                        else:
                            print "UNSUPPORTED", repr(cmd)
                            raise Exception
                    else:
                        print "UNSUPPORTED", repr(cmd)
                        raise Exception
                    
                else:
                    print "UNSUPPORTED", repr(cmd)
                    raise Exception
                
            elif cmd[0] == "banaNAS":
                if cmd[1].startswith("banA") and cmd[3].startswith("banA"):
                    self.process_compare(cmd)
                else:
                    print "UNSUPPORTED", repr(cmd)
                    raise Exception
                
            elif cmd[0].startswith("banA"):
                dest = get_reg(cmd[0])
                if cmd[2].startswith("banA"):
                    src = get_reg(cmd[2])
                    if cmd[1] == "baNAnas":
                        self.do_add(dest, src)
                    elif cmd[1] == "baNaNaS":
                        self.do_or(dest, src)
                    elif cmd[1] == "baNaNas":
                        self.do_and(dest, src)
                    elif cmd[1] == "baNanAS":
                        self.do_xor(dest, src)
                    else:
                        raise Exception
                else:
                    if cmd[1] == "baNanas":
                        self.load_register(dest, cmd[2:])
                        
                    else:
                        print "UNSUPPORTED", repr(cmd)
                        raise Exception
            else:
                print "UNSUPPORTED2", repr(cmd)
                raise Exception
                
            self.ip += 1
            
    
    def load_register(self, reg, vars):
        data = [b2i(s) for s in vars]
        self.regs[reg] = data
        print "LOAD r%d, %s" % (reg, data[0:16])

    def print_register(self, reg):
        s = reg2s(self.regs[reg])
        print "PRINT r%d, %s" % (reg, repr(s))
        
    def read_stdin(self, reg):
        line = self.fakestdin.pop(0)
        print "INPUT r%d, %s" % (reg, repr(line))
        destdata = []
        for c in line:
            destdata.append(ab.index(c))
            
        self.regs[reg] = destdata
        
    def do_add(self, dest, src):
        print "ADD r%d, r%d" % (dest, src)
        destdata = self.regs[dest][::-1]
        srcdata = self.regs[src][::-1]
        carry = 1
        for i in xrange(len(destdata)):
            if i < len(srcdata):
                t = destdata[i] + srcdata[i] + carry
                carry = t >> 7
                destdata[i] = t & 0x7f
            
        self.regs[dest] = destdata[::-1]
            
    def do_and(self, dest, src):
        print "AND r%d, r%d" % (dest, src)
        destdata = self.regs[dest][::-1]
        srcdata = self.regs[src][::-1]
        for i in xrange(len(destdata)):
            destdata[i] &= srcdata[i % len(srcdata)] ^ 0x7f
            
        self.regs[dest] = destdata[::-1]
        
    def do_or(self, dest, src):
        print "OR r%d, r%d" % (dest, src)
        destdata = self.regs[dest][::-1]
        srcdata = self.regs[src][::-1]
        for i in xrange(len(destdata)):
            destdata[i] |= srcdata[i % len(srcdata)] ^ 0x7f
            
        self.regs[dest] = destdata[::-1]
            
    def do_xor(self, dest, src):
        print "XOR r%d, r%d" % (dest, src)
        destdata = self.regs[dest][::-1]
        srcdata = self.regs[src][::-1]
        for i in xrange(len(destdata)):
            destdata[i] ^= srcdata[i % len(srcdata)] ^ 0x7f
            
        self.regs[dest] = destdata[::-1]
            
    def process_compare(self, cmd):
        reg1 = get_reg(cmd[1])
        reg2 = get_reg(cmd[3])
    
        do_skip = False
        if cmd[2] == "baNANaS":
            num1 = reg2i(self.regs[reg1])
            num2 = reg2i(self.regs[reg2])
            print "COMP r%d, r%d : %d >= %d" % (reg1, reg2, num1, num2)
            if num1 >= num2:
                do_skip = True
                        
        elif cmd[2] == "baNANAS":
            print "COMPstr r%d, r%d : %s == %s" % (reg1, reg2, repr(reg2s(self.regs[reg1])), repr(reg2s(self.regs[reg2])))
            if self.regs[reg1] == self.regs[reg2]:
                do_skip = True
                
        else:
            print "UNSUPPORTED2", repr(cmd)
            raise Exception
            
                
        if do_skip:
            self.ip += 1
            
vm = BananaVM()
vm.run(sys.argv[1], ["11", "BanaNAs!", "cOFe", "aaaa"])
