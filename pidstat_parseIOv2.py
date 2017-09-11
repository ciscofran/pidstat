#!/usr/bin/env python3

import re
import pdb
from collections import defaultdict 

# pidstat xxx format
#     Time   UID      TGID       TID    %usr %system  %guest   %wait    %CPU   CPU  minflt/s  majflt/s     VSZ     RSS   %MEM   kB_rd/s   kB_wr/s kB_ccwr/s iodelay   cswch/s nvcswch/s  Command

pattern = re.compile(r"\s*(?P<Time>\d+)\s+(?P<UID>\d+)\s+(?P<TGID>\d+)\s+(?P<TID>\d+)\s+(?P<usr>([0-9]*[.])?[0-9]+)\s+(?P<system>([0-9]*[.])?[0-9]+)\s+(?P<guest>([0-9]*[.])?[0-9]+)\s+(?P<wait>([0-9]*[.])?[0-9]+)\s+(?P<pcpu>([0-9]*[.])?[0-9]+)\s+(?P<cpu>\d+)\s+(?P<minflt>([0-9]*[.])?[0-9]+)\s+(?P<majflt>([0-9]*[.])?[0-9]+)\s+(?P<VSZ>\d+)\s+(?P<RSS>\d+)\s+(?P<mem>([0-9]*[.])?[0-9]+)\s+(?P<kbrd>([0-9]*[.])?[0-9]+)\s+(?P<kbwr>([0-9]*[.])?[0-9]+)\s+(?P<kbccwr>([0-9]*[.])?[0-9]+)\s+(?P<iodelay>\d+)\s+(?P<cswch>([0-9]*[.])?[0-9]+)\s+(?P<nvcswch>([0-9]*[.])?[0-9]+)\s+(?P<command>.*)")

class pidstat:
    def __init__(self, time, tid, pcpu, kbrd, kbwr):
        self.time = time
        self.tid  = tid
        self.pcpu = float(pcpu)
        self.kbrd  = float(kbrd)
        self.kbwr  = float(kbwr)

    def dump(self):
        print("      ", self.time, self.tid, self.kbrd, self.kbwr)

    def dumpRW(self):
        if (self.tid == "0"):
          print(self.tid,',',self.time,',',self.kbrd,',',self.kbwr)


data = defaultdict(list)

def analyze(data,ofile):
    for k,v in data.items():
       for index in range(len(data[k])):
         if (k == "0"):
            ofile.write("%s, %s, %s ,0,0 \n" % (data[k][index].time,data[k][index].kbrd,data[k][index].kbwr))

def collect(match):
    tid = match.group("TID")
    stat = pidstat(match.group("Time"), tid , match.group("pcpu"),match.group("kbrd"),match.group("kbwr"))
    stat.dumpRW();
    data[tid].append(stat)


def parse(line):
    if len(line.strip()) == 0 or line.startswith("#"):
        return

    match = pattern.match(line)
    if match is not None:
        collect(match)    
    print (">", line.strip())

with open ("pidstat.log") as f:
    for line in f:
        parse(line)
    
lengths = [len(v) for v in data.values()]
print ("length per key",lengths)

with open ('IO.dat','w') as ofile:
     ofile.write("%s\n" % ("#yaxis=kB_rd/s kB_wr/s"))
     ofile.write("%s\n" % ("#xaxis=Time-seconds"))
     #xlabels = ','.join(str(x) for x in range(1,300))
     ofile.write("%s\n" % ("#xlabels="))
     ofile.write("%s\n" % ("#showlabels=1"))
     ofile.write("%s\n" % ("#exactx=1"))
     ofile.write("%s\n" % ("#format=eps,png"))
     ofile.write("%s,%s,%s,%s,%s\n" % ("x","tid1Read","tid2Write","tid1Read-err","tid2Write-err"))
     
     analyze(data,ofile)



