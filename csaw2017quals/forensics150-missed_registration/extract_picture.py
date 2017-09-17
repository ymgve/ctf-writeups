

data = open("cap.pcap", "rb").read()

res = ""
for part in data.split("&x=")[1:]:
    print repr(part[0:220])
    res += part[0:220].split("D\x03")[0].decode("hex")
    
open("out.bmp", "wb").write(res)


# FLAG{HElp_Th3_BANANASCRIPt-guy_15_thr0wing_m0nkeys@me}
    
