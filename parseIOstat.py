#!/usr/bin/env python3

import re
import pdb
from collections import defaultdict 

# iostat format
# Device:            tps    kB_read/s    kB_wrtn/s    kB_read    kB_wrtn
# nvme0n1           0.00         0.00         0.00          0          0

#\s       Matches any whitespace character
#"+"      Matches 1 or more (greedy) repetitions of the preceding RE.
#"?"      Matches 0 or 1 (greedy) of the preceding RE.
#"*"      Matches 0 or more (greedy) repetitions of the preceding RE.
#(?P<name>...) The substring matched by the group is accessible by name

#\d       Matches any decimal digit

pattern = re.compile(r"\s*(?P<Device>(nvme1n1)\s+)\s+(?P<tps>([0-9]*[.])?[0-9]+)\s+(?P<kbrdS>([0-9]*[.])?[0-9]+)\s+(?P<kbwrS>([0-9]*[.])?[0-9]+)\s+(?P<kBr>\d+)\s+(?P<kBw>\d+)")
#pattern = re.compile(r"\s*(?P<Device>(nvme1n1)\s+)")

class iostat:
    def __init__(self, device, kBr, kBw):
        self.device  = device
        self.kBr  = kBr
        self.kBw  = kBw
		
    def dumpRW(self):
        print(self.device,',',self.kBr,',',self.kBw)


data = defaultdict(list)


def collect(match):
    device = match.group("Device")
    #print(device)
    stat = iostat(device,match.group("kBr"),match.group("kBw"))
    #stat.dumpRW();
    data[0].append(stat)  #one key only. Device=nvme1 is a string


def parse(line):
    if len(line.strip()) == 0 or line.startswith("#"):
        return

    match = pattern.match(line)
    if match is not None:
        collect(match)    
    #print (">", line.strip())

with open ("iostat.log") as f:
    for line in f:
        parse(line)
    
lengths = [len(v) for v in data.values()]
print ("length per key",lengths)
 
#for k,v in data.items():
#   for index in range(len(data[k])):
#        print("%s, %s, %s\n" % (data[k][index].device,data[k][index].kBr,data[k][index].kBw))
		

		
with open ('iostat.dat','w') as ofile:
 ofile.write("%s\n" % ("#yaxis= kB R/W"))
 ofile.write("%s\n" % ("#xaxis=Time-seconds"))
 ofile.write("%s\n" % ("#xlabels="))
 ofile.write("%s\n" % ("#showlabels=1"))
 ofile.write("%s\n" % ("#exactx=1"))
 ofile.write("%s\n" % ("#format=eps,png"))
 ofile.write("%s,%s,%s,%s,%s\n" % ("x","kB_read","kB_wrtn","kB_read-err","kB_wrtn-err"))
 for k,v in data.items():
   for index in range(len(data[k])):
        ofile.write("%d,%s,%s,0,0\n" % (index,data[k][index].kBr,data[k][index].kBw))




