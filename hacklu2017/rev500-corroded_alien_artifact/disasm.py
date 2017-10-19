
from capstone import *

data = open("ctf_alien_cpu-f1f94ee9f95b8bde.exe", "rb").read()[0xd20:0x1890]

md = Cs(CS_ARCH_X86, CS_MODE_64)
for i in xrange(len(data), -16, -16):
    code = data[i:i+16]
    for i in md.disasm(code, 0x140001920 + i):
        print "0x%x:\t%s\t%s" % (i.address, i.mnemonic, i.op_str)
        break