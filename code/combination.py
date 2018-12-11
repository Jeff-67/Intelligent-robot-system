import sys,string, os,commands
import numpy as np
import subprocess
import timeit
from subprocess import Popen,PIPE
import math
#start = timeit.default_timer()

#subprocess.call(['cd'])
#subprocess.call(['sudo','nvpmodel','-m','0'])
#subprocess.call(['sudo','./jetson_clocks.sh'])
#subprocess.call(['cd','/darknet'])


while True:
	start=timeit.default_timer()
	os.system(r'"/usr/local/bin/rs-save-to-disk"')
	(output,xy) = commands.getstatusoutput('./darknet detector test data/obj.data yolov3-tiny-obj.cfg backup/yolov3-tiny-obj_mango_50000.weights data/123/Color.png')
	send = np.fromstring(xy,dtype=float,sep=' ')	
	send2 =np.reshape(send,(-1,3))
	X = round(send2[0][1])
	Y = round(send2[0][2])
	xx = str(X)
	yy = str(Y)
	process = subprocess.Popen(['./rs-measure', xx , yy], stdout=subprocess.PIPE)
	out, err = process.communicate()
	aftermap = np.fromstring(out,dtype=float,sep=' ')
	print(aftermap)
	stop =timeit.default_timer()
	print stop-start
