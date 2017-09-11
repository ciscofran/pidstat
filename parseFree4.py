#!/usr/bin/env python3
#Francisco Londono

import re
import pdb
from collections import defaultdict 

# free output in MB
#             total       used       free     shared    buffers     cached
#Mem:          7865       7737        127          2          4       1916
#-/+ buffers/cache:       5816       2049
#Swap:        40959        235      40724

freeMlst = []
cachedMlst =[]
UsedSwaplst = []

def writeOut(ofile):
    cnt = 1
    for f,g,h in zip(freeMlst,cachedMlst,UsedSwaplst):
     ofile.write("%s,%s,%s,%s,0,0,0\n" % (cnt,f,g,h))
     cnt+=1
	 
def collectSwap(line):
    words = line.split()
    c = words[2]   # used swap space
    	
    UsedSwaplst.append(c)
	
def collect(line):
    words = line.split()
    #print(words)
    a,b = words[3],words[6]
    
    freeMlst.append(a)
    cachedMlst.append(b)


def parse(line):
    if len(line.strip()) == 0 or line.startswith("-"):
        return

    if "Mem:" in line:
       collect(line)
    elif "Swap:" in line:
       collectSwap(line)	
    #print (">", line.strip())

with open ("free.log") as f:
    for line in f:
        parse(line)
    
with open ('free2.dat','w') as ofile:
     ofile.write("%s\n" % ("#yaxis=Megabytes"))
     ofile.write("%s\n" % ("#xaxis=Time-seconds"))
     ofile.write("%s\n" % ("#xlabels="))
     ofile.write("%s\n" % ("#showlabels=1"))
     ofile.write("%s\n" % ("#exactx=1"))
     ofile.write("%s\n" % ("#format=eps,png"))
     ofile.write("%s,%s,%s,%s,%s,%s,%s\n" % ("x","freeM","cachedM","UsedSwap","freeM-err","cachedM-err","UsedSwap-err"))
     
     writeOut(ofile)




