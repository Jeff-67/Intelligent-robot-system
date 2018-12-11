import time
import serial
import numpy as np
import subprocess
out111 = subprocess.check_call('echo 388 > /sys/class/gpio/unexport', shell = True)
out22 = subprocess.check_call('echo 396 > /sys/class/gpio/unexport', shell = True)
out111 = subprocess.check_call('echo 388 > /sys/class/gpio/export', shell = True)
out22 = subprocess.check_call('echo 396 > /sys/class/gpio/export', shell = True)
out11 = subprocess.check_call('echo out > /sys/class/gpio/gpio388/direction', shell = True)
out1 = subprocess.check_call('echo out > /sys/class/gpio/gpio396/direction', shell = True)
#out2 = subprocess.check_call('echo 0 > /sys/class/gpio/gpio396/value', shell = True)
#out3 = subprocess.check_call('echo 0 > /sys/class/gpio/gpio388/value', shell = True)
ser=serial.Serial("/dev/ttyTHS2" , 19200, timeout= 1)
#ser = serial.Serial('/dev/ttyS0', 9600, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE, timeout= 0.5)

#ser.open()
print ser.baudrate
print ser.bytesize
print ser.parity
print ser.stopbits
print ser.xonxoff
print ser.rtscts
print ser.dsrdtr 
print ser.name
#print ser.inWaiting()
#ser.open()
#ser.flushInput()
while(1):
	out2 = subprocess.check_call('echo 0 > /sys/class/gpio/gpio396/value', shell = True)
	out3 = subprocess.check_call('echo 0 > /sys/class/gpio/gpio388/value', shell = True)
	print("ready")	
	#print ser.inWaiting()
	#time.sleep(1)
	
	#print("ready")
	#a = ser.readline()
	a= ser.read(3)	
	#a=ser.readline()
	print a
	if(a=='YES'):
		print a,type(a)
		out22 = subprocess.check_call('echo 1 > /sys/class/gpio/gpio396/value', shell = True)
		out33 = subprocess.check_call('echo 1 > /sys/class/gpio/gpio388/value', shell = True)
		#ser.write(chr(num[0]))
		#endcode
		ser.write(chr(0))
		ser.write(chr(44))
		#print (unichr(a))
		#print a.decode('utf-8')
		#i=2
		print("first")
		a=""
	if(a=='GET' ):
		print a,type(a)
		out22 = subprocess.check_call('echo 1 > /sys/class/gpio/gpio396/value', shell = True)
		out33 = subprocess.check_call('echo 1 > /sys/class/gpio/gpio388/value', shell = True)
		#number = 104464
		#num = np.array(list(number))
		#ser.write(chr(num[0]))
		#ser.write(chr(num[1]))		
	#endcode	
		
		#print (unichr(a))
		#print a.decode('utf-8')
		#i=2
		a=""
		
	#print ser.inWaiting()
		
	#time.sleep(1)	
#print(a)
#c = np.array([59,232,655])
#x = c[1]
#y = c[2]
#values = chr(x)

#value = 'x'
#values = chr(y)
#ser.write(value)


#values = bytearray([4, 9, 62, 144, 56, 30, 147, 3, 210, 89, 111, 78, 184, 151, 17, 129])
	#ser.write(values)
#ser.write(value)
#ser.close()





