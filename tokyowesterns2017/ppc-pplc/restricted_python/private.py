import sys
from restrict import Restrict

r = Restrict()
# r.set_timeout()

class Private:
    def __init__(self):
        pass

    def __flag(self):
        return "TWCTF{CENSORED}"

p = Private()
Private = None

d = sys.stdin.read()
assert d is not None
assert "Private" not in d, "Private found!"
d = d[:24]

r.seccomp()

print eval(d)
