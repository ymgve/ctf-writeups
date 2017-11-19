import sys, struct

def s2n(s):
    if s.startswith("0x"):
        if s.endswith("L"):
            s = s[:-1]
        n = int(s[2:], 16)
    else:
        n = int(s)
        
    return n
    
def s2b(s, nbits=8):
    n = s2n(s)
        
    if n < 0 or n >= (1<<nbits):
        raise Exception("num too large")
        
    res = bin(n)[2:].rjust(nbits, "0")
    return res
        
functions = []
ram = []

for line in open(sys.argv[1]):
    line = line.split(";")[0].strip()
    if len(line) == 0:
        continue
        
    tokens = line.split()
    op = tokens[0].lower()
    
    if op == "function":
        function = []
        inscount = 0
    elif op == "end":
        functions.append(function)
    elif op == "blankram":
        ram.extend([0] * s2n(tokens[1]))
        
    elif op == "qword":
        ram.append(s2n(tokens[1]))
        
    elif op == "jmpz":
        function.append("000" + s2b(tokens[1].replace("label", "")))
    elif op == "jmp":
        function.append("001" + s2b(tokens[1].replace("label", "")))
    elif op == "call":
        function.append("010" + s2b(tokens[1]))
    elif op == "loadram":
        function.append("1000" + s2b(tokens[1], 7))
    elif op == "saveram":
        function.append("1001" + s2b(tokens[1], 7))
    elif op == "dup":
        function.append("1010" + s2b(tokens[1], 7))
    elif op == "place":
        function.append("1011" + s2b(tokens[1], 7))
    elif op == "loadi":
        function.append("110" + s2b(tokens[1]))
    elif op == "shl":
        function.append("11100" + s2b(tokens[1], 6))
    elif op == "shr":
        function.append("11101" + s2b(tokens[1], 6))
    elif op == "not":
        function.append("111100")
    elif op == "and":
        function.append("111101")
    elif op == "or":
        function.append("111110")
    elif op == "setif":
        function.append("111111")
    elif op == "pop":
        function.append("110" + s2b("0"))
        function.append("111101")
        function.append("111110")
    elif op.startswith("label"):
        function.append("011" + s2b(op.replace("label", "")))
    else:
        raise Exception("invalid token " + line)

headersize = 16 + len(functions) * 8

header = struct.pack(">Q", len(functions))

data = ""
for function in functions:
    codebits = "".join(function)
    while len(codebits) % 8 != 0:
        codebits += "0"
    code = ""
    for i in xrange(0, len(codebits), 8):
        code += chr(int(codebits[i:i+8], 2))
        
    header += struct.pack(">Q", headersize + len(data))
    data += struct.pack(">Q", len(function))
    data += code
    
header += struct.pack(">Q", headersize + len(data))
data += struct.pack(">Q", len(ram)) * 2

for n in ram:
    data += struct.pack(">Q", n)
    
open("output.cmp", "wb").write(header + data)
