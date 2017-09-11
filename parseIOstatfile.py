
#import pdb


def parse(line):
   if len(line.strip()) == 0:
      return
	  
   if "nvme1n1" in line:
      print(line)
   


with open ("iostat.log","r") as f:
    for line in f:
      parse(line)