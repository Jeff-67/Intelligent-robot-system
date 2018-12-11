import sys,string, os,commands
import numpy as np
import subprocess
import timeit
from subprocess import Popen,PIPE
import math
angle = 18
while True:
	start = timeit.default_timer()
	os.system(r'"/usr/local/bin/rs-save-to-disk"')
	stop =timeit.default_timer()
	print stop-start
