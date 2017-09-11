#!/usr/bin/python
import os
import subprocess
import pdb
import time

print ('starting')

subprocess.call('sudo sysctl -w vm.drop_caches=3',shell=True)

os.chdir('/home/franc/runtimeLogs/test2')
print ('Changed dir')


with open('pidstat.log','w') as f:
   process1 = subprocess.Popen('sudo /home/franc/bin/pidstat -t -urd -h -w -C dedup 1',shell=True,executable='/bin/bash',stdout=f)
#print(process1.pid)
#process1.wait()



with open('iostat.log','w') as fio:
  process2 = subprocess.Popen('iostat -c -d 1 -y',shell=True,executable='/bin/bash',stdout=fio)


os.chdir('/media/nvme1/parsec-3.0/pkgs/kernels/dedup/src')

subprocess.call('sudo rm *.ddp',shell=True)

time.sleep(2)

process3 = subprocess.Popen('sudo time ./dedup -c -w none -t 1 -i dvd4G.iso -o output.ddp',shell=True,stdout=subprocess.PIPE)
print(process3.pid)
process3.wait()
print("Parsec completed")

time.sleep(2)
print("Killing logging threads")
f.close()
fio.close()
os.system("sudo kill %d"%(process1.pid))
#process1.kill()
process2.kill()


subprocess.call('ls -lhtr',shell=True)
print("End")
