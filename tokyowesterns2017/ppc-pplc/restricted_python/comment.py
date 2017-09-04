import sys
from restrict import Restrict

r = Restrict()
# r.set_timeout()

d = sys.stdin.read()
assert d is not None
d = d[:20]

import comment_flag
r.seccomp()

print eval(d)
