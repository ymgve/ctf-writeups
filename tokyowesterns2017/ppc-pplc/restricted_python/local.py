import sys
from restrict import Restrict

r = Restrict()
# r.set_timeout()

def get_flag(x):
    flag = "TWCTF{CENSORED}"
    return x

d = sys.stdin.read()
assert d is not None
d = d[:30]

r.seccomp()

print eval(d)
