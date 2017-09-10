import subprocess

bits = "."

while True:
    cand = "0" + bits + "asisctf.com"
    args = ["dig", "@95.85.26.168", cand]

    pc = subprocess.Popen(args, stdout=subprocess.PIPE)
    stdout, stderr = pc.communicate()
    
    if "status: NXDOMAIN" in stdout:
        bits = "1" + bits
    elif "status: NOERROR" in stdout:
        bits = "0" + bits
    else:
        break
        
    if bits.index(".") == 63:
        bits = "." + bits
    
    print bits
    
    bits2 = "0" + bits.replace(".", "")[::-1]

    s = ""
    for i in xrange(0, len(bits2), 8):
        s += chr(int(bits2[i:i+8], 2))
    print repr(s)