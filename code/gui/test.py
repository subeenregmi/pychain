import time
import threading

ips = "PLRR:([192.0.0.1][19.234.512.2])"

ips = ips[5:]
print(ips)
ips = ips.replace("(", "")
ips = ips.replace(")", "")
ips = ips.replace("[", "")
ips = ips.replace("]", " ")
ips = ips.split()
print(ips)