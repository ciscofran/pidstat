#!/usr/bin/env python3
# python 2.7 method is : call
# python 3.x method is : run

import subprocess


completed = subprocess.call('sudo sysctl -w vm.drop_caches=3',shell=True)
#completed = subprocess.run('sudo sysctl -w vm.drop_caches=3',shell=True)
print ('returncode:',completed)
