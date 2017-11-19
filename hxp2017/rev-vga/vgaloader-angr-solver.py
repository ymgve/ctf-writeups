import angr

proj = angr.Project('./vgaloader.elf')
state = proj.factory.entry_state()
simgr = proj.factory.simgr(state)
simgr.explore(find=0x000B8F9F)
print repr(simgr.found[0].posix.dumps(0))
