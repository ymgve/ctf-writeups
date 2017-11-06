import angr

data = open("sakura-fdb3c896d8a3029f40a38150b2e30a79", "rb").read()
finds = []
avoids = []
index = 0
count = 0
while True:
    # find all the places where the code does "mov [rbp+result], 0"
    # and add them to the "avoid" list
    res = data.find("\xC6\x85\xB7\xE1\xFF\xFF\x00", index)
    if res == -1:
        break
    
    avoids.append(0x400000 + res)
    
    # add the location after each block to the "find" list
    if count % 3 == 2:
        finds.append(0x400000 + res + 7)
        
    count += 1
    index = res + 1

proj = angr.Project('./sakura-fdb3c896d8a3029f40a38150b2e30a79')
state = proj.factory.entry_state()

# we do find in multiple stages to monitor angr's progress
for find in finds:
    print hex(find)
    simgr = proj.factory.simgr(state)
    simgr.explore(find=find, avoid=avoids)
    state = simgr.found[0]
    print repr(state.posix.dumps(0))

open("input", "wb").write(state.posix.dumps(0))

# cat input | ./sakura-fdb3c896d8a3029f40a38150b2e30a79
