import sys
from subprocess import PIPE, Popen
from threading  import Thread
import time

try:
    from queue import Queue, Empty
except ImportError:
    from Queue import Queue, Empty  # python 2.x

ON_POSIX = 'posix' in sys.builtin_module_names

def enqueue_output(out, queue):
	for line in iter(out.readline, b''):
		queue.put(line)
	out.close()

p = Popen(['./darknet','detector','test','data/obj.data','yolov3-tiny-obj.cfg','backup/yolov3-tiny-obj_mango_50000.weights'], stdout=PIPE, bufsize=1, close_fds=ON_POSIX)
time.sleep(40)
q = Queue()
t = Thread(target=enqueue_output, args=(p.stdout, q))
t.daemon = True # thread dies with the program
t.start()



# ... do other things here

# read line without blocking
try:  line = q.get_nowait() # or q.get(timeout=.1)
except Empty:
	print('no output yet')
else: # got line
    # ... do something with line
	print(line)

