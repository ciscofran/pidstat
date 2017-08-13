#!/usr/bin/env python3

import re
import pdb
from collections import defaultdict 
import numpy as np
import pandas as pd

#pattern = re.compile(r"\s*(?P<Time>\d+)\s+(?P<UID>\d+)\s+(?P<TGID>\d+)\s+(?P<TID>\d+)\s+(?P<usr>([0-9]*[.])?[0-9]+)\s+(?P<system>([0-9]*[.])?[0-9]+)\s+(?P<guest>([0-9]*[.])?[0-9]+)\s+(?P<wait>([0-9]*[.])?[0-9]+)\s+(?P<pcpu>([0-9]*[.])?[0-9]+)\s+(?P<cpu>\d+)\s+(?P<minflt>([0-9]*[.])?[0-9]+)\s+(?P<majflt>([0-9]*[.])?[0-9]+)\s+(?P<VSZ>\d+)\s+(?P<RSS>\d+)\s+(?P<mem>([0-9]*[.])?[0-9]+)\s+(?P<kbrd>([0-9]*[.])?[0-9]+)\s+(?P<kbwr>([0-9]*[.])?[0-9]+)\s+(?P<kbccwr>([0-9]*[.])?[0-9]+)\s+(?P<iodelay>\d+)\s+(?P<cswch>([0-9]*[.])?[0-9]+)\s+(?P<nvcswch>([0-9]*[.])?[0-9]+)\s+(?P<command>.*)")
pattern = re.compile(r"\s*(?P<Time>\d+)\s+(?P<UID>\d+)\s+(?P<TGID>\d+)\s+(?P<TID>\d+)\s+(?P<usr>([0-9]*[.])?[0-9]+)\s+(?P<system>([0-9]*[.])?[0-9]+)\s+(?P<guest>([0-9]*[.])?[0-9]+)\s+(?P<pcpu>([0-9]*[.])?[0-9]+)\s+(?P<cpu>\d+)\s+(?P<minflt>([0-9]*[.])?[0-9]+)\s+(?P<majflt>([0-9]*[.])?[0-9]+)\s+(?P<VSZ>\d+)\s+(?P<RSS>\d+)\s+(?P<mem>([0-9]*[.])?[0-9]+)\s+(?P<kbrd>([0-9]*[.])?[0-9]+)\s+(?P<kbwr>([0-9]*[.])?[0-9]+)\s+(?P<kbccwr>([0-9]*[.])?[0-9]+)\s+(?P<cswch>([0-9]*[.])?[0-9]+)\s+(?P<nvcswch>([0-9]*[.])?[0-9]+)\s+(?P<command>.*)")
##      Time   UID      TGID       TID    %usr %system  %guest    %CPU   CPU  minflt/s  majflt/s     VSZ    RSS   %MEM   kB_rd/s   kB_wr/s kB_ccwr/s   cswch/s nvcswch/s  Command
class pidstat:
    def __init__(self, time, tid, pcpu, kbrd, kbwr):
        self.time = time
        self.tid  = tid
        self.pcpu = float(pcpu)
        self.kbrd  = float(kbrd)
        self.kbwr  = float(kbwr)

    def dump(self):
        print("      ", self.time, self.tid, self.pcpu,self.kbrd,self.kbwr)



data = defaultdict(list)

	 
def collect(match):
    tid = match.group("TID")
    stat = pidstat(match.group("Time"), tid , match.group("pcpu"),match.group("kbrd"),match.group("kbwr"))
    stat.dump();
    if (tid != "0"):
      data[tid].append(stat)


def parse(line):
    if len(line.strip()) == 0 or line.startswith("#"):
        return

    match = pattern.match(line)
    if match is not None:
        collect(match)    
    #print (">", line.strip())

with open ("pidstat.log") as f:
    for line in f:
        parse(line)
    
    
  
lengths = [len(v) for v in data.values()]
print ("length per key",lengths)
keys = [k for k in data.keys()]
print (keys)
print (keys[0])   # print first key
del data[keys[0]] # delete first element
del keys[0] # delete first key of variable from lie 56de
lengths = [len(v) for v in data.values()]
print ("length per key",lengths)


print("Printing dataframe\n")
df = pd.DataFrame(columns=data.keys())
print (df)


for k in keys:
 for index in range(len(data[k])):
    df.loc[index,k] = (data[k][index].pcpu)
	
print (df)

df.to_csv('pcpu1.dat',encoding='utf-8')

with open ('pid.dat','w') as ofile:
 ofile.write("%s\n" % ("#yaxis= Percent CPU Utilization"))
 ofile.write("%s\n" % ("#xaxis=Time-seconds"))
 ofile.write("%s\n" % ("#xlabels="))
 ofile.write("%s\n" % ("#showlabels=1"))
 ofile.write("%s\n" % ("#exactx=1"))
 ofile.write("%s\n" % ("#format=eps,png"))
 ofile.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % ("x","tid1pCPU","tid2pCPU","tid3pCPU","tid4pCPU","tid5pCPU","tid6pCPU","tid1pCPU-err","tid2pCPU-err","tid3pCPU-err","tid4pCPU-err","tid5pCPU-err","tid6pCPU-err"))
 with open ('pcpu1.dat','r') as fh:
    for line in fh:
      ofile.write("%s,0,0,0,0,0,0\n" % line.strip('\n'))
	  
