import re
import subprocess
import pdb

tskstr = 'taskset -pc'

# pids.log file format
#PID   TID COMMAND  USER     PSR
#31387     - dedup    ads        -
#    - 31387 -        ads       22
#
pattern = re.compile(r"\s*(?P<PID>[0-9_-]+)\s+(?P<TID>[0-9_-]+)\s+(?P<command>.*)\s+(?P<USER>.*)\s+(?P<PSR>\d+)")

print ('starting')

subprocess.call('sh getpid.sh > pids.log',shell=True)

ctr=0

def setaff(match):
    tid = match.group("TID")
    print(tid)
    commandstr = ("%s %s %s"% (tskstr,ctr,tid))
    print (commandstr)
    subprocess.call(commandstr,shell=True)  

def parse(line):
  if len(line.strip()) == 0:
     return

  match = pattern.match(line)
  if match is not None:
     setaff(match)


with open ("pids.log") as f:
    for line in f:
      parse(line)
      ctr += 1
