import struct, binascii

f = open("SecureFloridaVotingBoothTraffic.9c56dd72a07a165680f1bdaccc37136c57f840712ac7db980064c8b386ff06c6.pcapng", "rb")

prev_id = None
prev_ts = None
count = 0

morse = ""
while True:
    t = f.read(4)
    if len(t) != 4:
        exit()
    btype = t
    
    t = f.read(4)
    blen1 = struct.unpack("<L", t)[0]
    
    data = f.read(blen1-12)
    
    t = f.read(4)
    blen2 = struct.unpack("<L", t)[0]
    
    if btype != "\x06\x00\x00\x00":
        continue
        
    packet = data[20:]
    
    if packet[6:12] == binascii.a2b_hex("000c2998b995") and packet[0x2a:0x2e] == "QUNL":
        id = struct.unpack(">H", packet[18:20])[0]
        thi, tlo = struct.unpack("<II", data[4:12])
        ts = ((thi << 32) | tlo) / 1000
        
        if prev_id is not None:
            diff = ts - prev_ts
            count += 1
            
            if diff > 10:
                if count == 3:
                    morse += "."
                    count = 0
                elif count == 6:
                    morse += "-"
                    count = 0
                    
                if diff > 400 and diff < 600:
                    count = 0
                elif diff > 1400 and diff < 1600:
                    count = 0
                    morse += " "
                else:
                    print morse
                    exit()
            
        prev_id = id
        prev_ts = ts
        
