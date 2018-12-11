import sys,string,os,commands
import numpy as np
import pandas as pd
import subprocess
import timeit
from subprocess import Popen,PIPE
import math
import time
import serial
import numpy as np
import warnings


out111 = subprocess.check_call('echo 388 > /sys/class/gpio/unexport', shell = True)
out22 = subprocess.check_call('echo 396 > /sys/class/gpio/unexport', shell = True)
out111 = subprocess.check_call('echo 388 > /sys/class/gpio/export', shell = True)
out22 = subprocess.check_call('echo 396 > /sys/class/gpio/export', shell = True)
out11 = subprocess.check_call('echo out > /sys/class/gpio/gpio388/direction', shell = True)
out1 = subprocess.check_call('echo out > /sys/class/gpio/gpio396/direction', shell = True)
ser=serial.Serial("/dev/ttyTHS2" , 19200, timeout= 1)


def main():


	times = 2
	times2 = 2

	#mapping

	test_camera_1=np.array([187.350,378.020,0.834 ])
	test_arm_1   =np.array([-94.558,-379.979,80.647])

	test_camera_2=np.array([336.77,283.42, 0.825 ])
	test_arm_2   =np.array([109.491,-488.961,80.569])  

	test_camera_3=np.array([504.17,322.48,0.82 ])
	test_arm_3   =np.array([321.526,-440.118,80.218 ])

	test_camera_4=np.array([157.7305,231.3786])
	test_arm_4   =np.array([-126.579,-563.052])

	test_camera_5=np.array([510.8974,376.556])
	test_arm_5   =np.array([324.556,-374.19])

	test_camera_6=np.array([310.3019,378.8711])
	test_arm_6   =np.array([324.556,-374.19])

	camera_x = np.array([test_camera_1[0],test_camera_2[0],test_camera_3[0],test_camera_4[0]]) #insert camera x coordinates.......,test_camera_5[0]

	arm_x = np.array([test_arm_1[0],test_arm_2[0],test_arm_3[0],test_arm_4[0]])  #insert arm x coordinates........,test_arm_5[0]

	para_for_x = np.polyfit(camera_x, arm_x, 3)
	

	camera_y = np.array([test_camera_1[1],test_camera_2[1],test_camera_3[1],test_camera_4[1]])  #insert camera y coordinates,test_camera_5[1]

	arm_y = np.array([test_arm_1[1],test_arm_2[1],test_arm_3[1],test_arm_4[1]])  #insert arm y coordinates,test_arm_5[1]

	para_for_y = np.polyfit(camera_y, arm_y, 3)


	camera_z = np.array([test_camera_1[2],test_camera_2[2]])  #insert camera z coordinates,test_camera_3[2]

	arm_z = np.array([test_arm_1[2],test_arm_2[2]])  #insert arm z coordinates,test_arm_3[2]

	para_for_z =np.polyfit(camera_z, arm_z, 1)



	corect_x = np.poly1d(para_for_x)  #mapping function    

	corect_y = np.poly1d(para_for_y)  #mapping function

	corect_z = np.poly1d(para_for_z)  #mapping function

	Yolo = subprocess.Popen("./darknet detector test data/obj.data yolov3-tiny-obj.cfg backup/yolov3-tiny-obj_mango_50000.weights", stdout=subprocess.PIPE, shell=True)
	
	while (1):


		start=timeit.default_timer()


		out2 = subprocess.check_call('echo 0 > /sys/class/gpio/gpio396/value', shell = True)
		out3 = subprocess.check_call('echo 0 > /sys/class/gpio/gpio388/value', shell = True)
		
		print("ready")
		

		os.system("/usr/local/bin/rs-save-to-disk")

		with warnings.catch_warnings():
			warnings.simplefilter("ignore")
			
			yolo = np.loadtxt("file.txt", dtype=str)
		

		c=[];

		if(yolo!=c):
				
			xx,yy = maptorealsense_andrecongnizesweetspot(yolo)

			xxb,yyb = maptorealsense_andpickbadmango(yolo)

			print(xx,yy)

			r = './rs-measure '+xx+yy
			
			(output,out) = commands.getstatusoutput(r)
			
			
			x,y,z = maptoxyz(out,xx,yy,corect_x,corect_y,corect_z)
			
	
			print(x,y,z)

			a = ser.read(3)

			print(a)

			
			if(a=='GO1'):
				print (a)
				out22 = subprocess.check_call('echo 1 > /sys/class/gpio/gpio396/value', shell = True)
				out33 = subprocess.check_call('echo 1 > /sys/class/gpio/gpio388/value', shell = True)
		
				xs = str(x)
				ys = str(y)
				zs = str(z)

				to_arm_x = np.array(list(xs))
	
				to_arm_y = np.array(list(ys))

				to_arm_z = np.array(list(zs))

				for i in range(0,7):
					if(i==0):
						if (to_arm_x[i] == '-'):
							to_arm_x[i] = 2	
						else:
							to_arm_x[i] = 1
					if i == 4:
						continue
					ser.write(chr(int(to_arm_x[i])))

				for d in range(0,7):
					if(d==0):				
						if (to_arm_y[d] == '-'):
							to_arm_y[d] = 2
						else:
							to_arm_y[d] = 1	
					if d == 4:
						continue
			
					ser.write(chr(int(to_arm_y[d])))
 
				for g in range(0,7):
					if(g==0):
						if (to_arm_z[g] == '-'):
							to_arm_z[g] = 2
						else:
							to_arm_z[g] = 1
					if g == 4:
						continue
			
					ser.write(chr(int(to_arm_z[g])))
	
	
				

				ser.write(chr(44))	#endcode123	
				
				out227 = subprocess.check_call('echo 0 > /sys/class/gpio/gpio396/value', shell = True)
				out337 = subprocess.check_call('echo 0 > /sys/class/gpio/gpio388/value', shell = True)
		
				a=""

			if(a=='GO2'):

				print (a)
				
				rb = './rs-measure '+xxb+yyb
			
				(outputb,outb) = commands.getstatusoutput(r)
			
			
				xb,yb,zb = maptoxyz(outb,xxb,yyb,corect_x,corect_y,corect_z)
			
	
				print(xb,yb,zb)


				
				
				out22 = subprocess.check_call('echo 1 > /sys/class/gpio/gpio396/value', shell = True)
				out33 = subprocess.check_call('echo 1 > /sys/class/gpio/gpio388/value', shell = True)
		
				xsb = str(xb)
				ysb = str(yb)
				zsb = str(zb)

				to_arm_xb = np.array(list(xsb))
	
				to_arm_yb = np.array(list(ysb))

				to_arm_zb = np.array(list(zsb))

				for i in range(0,7):
					if(i==0):
						if (to_arm_xb[i] == '-'):
							to_arm_xb[i] = 2	
						else:
							to_arm_xb[i] = 1
					if i == 4:
						continue
					ser.write(chr(int(to_arm_xb[i])))

				for d in range(0,7):
					if(d==0):				
						if (to_arm_yb[d] == '-'):
							to_arm_yb[d] = 2
						else:
							to_arm_yb[d] = 1	
					if d == 4:
						continue
			
					ser.write(chr(int(to_arm_yb[d])))
 
				for g in range(0,7):
					if(g==0):
						if (to_arm_zb[g] == '-'):
							to_arm_zb[g] = 2
						else:
							to_arm_zb[g] = 1
					if g == 4:
						continue
			
					ser.write(chr(int(to_arm_zb[g])))
	
	
				

				ser.write(chr(44))	#endcode123	
				
				out227 = subprocess.check_call('echo 0 > /sys/class/gpio/gpio396/value', shell = True)
				out337 = subprocess.check_call('echo 0 > /sys/class/gpio/gpio388/value', shell = True)
		
				a=""


			if(a=='GO3'):

				print a
				a=""
				ifgrippable(yolo)
				
				while(a==""):
					a=ser.read(3)
					print a 
					if(a=='YES'):
						break	
						
				out22 = subprocess.check_call('echo 1 > /sys/class/gpio/gpio396/value', shell = True)
				out33 = subprocess.check_call('echo 1 > /sys/class/gpio/gpio388/value', shell = True)
		
				xs = str(x)
				ys = str(y)
				zs = str(z)

				to_arm_x = np.array(list(xs))
	
				to_arm_y = np.array(list(ys))

				to_arm_z = np.array(list(zs))

				for i in range(0,7):
					if(i==0):
						if (to_arm_x[i] == '-'):
							to_arm_x[i] = 2	
						else:
							to_arm_x[i] = 1
					if i == 4:
						continue
					ser.write(chr(int(to_arm_x[i])))

				for d in range(0,7):
					if(d==0):				
						if (to_arm_y[d] == '-'):
							to_arm_y[d] = 2
						else:
							to_arm_y[d] = 1	
					if d == 4:
						continue
			
					ser.write(chr(int(to_arm_y[d])))
 
				for g in range(0,7):
					if(g==0):
						if (to_arm_z[g] == '-'):
							to_arm_z[g] = 2
						else:
							to_arm_z[g] = 1
					if g == 4:
						continue
			
					ser.write(chr(int(to_arm_z[g])))
	
	
				

				ser.write(chr(44))	#endcode123	
				
				out227 = subprocess.check_call('echo 0 > /sys/class/gpio/gpio396/value', shell = True)
				out337 = subprocess.check_call('echo 0 > /sys/class/gpio/gpio388/value', shell = True)
		
				a=""

		stop =timeit.default_timer()
	
		print (stop-start)



def ifgrippable(send0):
	

	out226 = subprocess.check_call('echo 1 > /sys/class/gpio/gpio396/value', shell = True)
	out336 = subprocess.check_call('echo 1 > /sys/class/gpio/gpio388/value', shell = True)
	send0 = np.reshape(send0, (-1, 4))
	send0 = np.delete(send0, 0, 1)
	send0 = np.delete(send0, 0, 1)
	send0 = send0.astype(np.float)  
	(row,col) = send0.shape
		
	for j in range (row):
		
		if (j>1):
		
			break

		xxx = send0[j][0]
		yyy = send0[j][1]

		if (390>X>105 and 268>Y>40):

			dist = math.hypot(send0[j+1][0]-send0[j][0], send0[j+1][1]-send0[j][1])	

			if (dist>50):
					
				stirlx = (send0[j+1][0]+send0[j][0])/2
				stirly = (send0[j+1][1]+send0[j][1])/2	
		
				print stirlx,stirly			
					
				stirlx = '{:07.2f}'.format(stirlx)
				stirly = '{:07.2f}'.format(stirly)		
				stirlx = str(stirlx)	
				stirly = str(stirly)
				stirlx = np.array(list(stirlx))
				stirly = np.array(list(stirly))
	
				for p in range(0,7):
		
					if(p==0):

						if (stirlx[p] == '-'):
								stirlx[p] = 2	
						else:
								stirlx[p] = 1
					if p == 4:
	
						continue
	
					ser.write(chr(int(stirlx[p])))
	
				for q in range(0,7):
	
					if(q==0):

						if (stirly[q] == '-'):
							stirly[q] = 2	
						else:
							stirly[q] = 1
					if q == 4:
	
						continue
						
					ser.write(chr(int(stirly[q])))
		
	
	out2266 = subprocess.check_call('echo 0 > /sys/class/gpio/gpio396/value', shell = True)
	out3366 = subprocess.check_call('echo 0 > /sys/class/gpio/gpio388/value', shell = True)


def maptorealsense_andrecongnizesweetspot(send1):

	send2 = np.reshape(send1, (-1, 4))
	(row1,col1) = send2.shape
	
	for jj in range (row1):
		
		if (send2[jj][0] == "targetmango"):
			send22 = np.delete(send2, 0, 1)
			send222 = send22.astype(np.float)
			X = send222[jj][1]
			Y = send222[jj][2]
			
			if ( 390>X>105 and 268>Y>40):
				X = '%.2f'%X
				Y = '%.2f'%Y
				xxx = str(X)
				yyy = ' '+str(Y)
 				break		
	if (xxx == 0 and yyy ==1):
		xxx = send2[0][2]
		yyy = send2[0][3]
		xxx = float(xxx)
		yyy = float(yyy)
		xxx = '%.2f'%xxx
		yyy = '%.2f'%yyy
		yyy = ' '+yyy
	return xxx,yyy


def maptorealsense_andpickbadmango(sendd):
	xxxb = 0
	yyyb = 1
	senddb = np.reshape(sendd, (-1, 4))
	(row1b,colb) = senddb.shape

	for jjb in range (row1b):

		if (senddb[jj][0] == "badmango"):
			send22b = np.delete(senddb, 0, 1)
			send222b = send22b.astype(np.float)
			Xb = send222b[jj][1]
			Yb = send222b[jj][2]
			
			if ( 390>Xb>105 and 268>Yb>40):
				Xb = '%.2f'%Xb
				Yb = '%.2f'%Yb
				xxxb = str(Xb)
				yyyb = ' '+str(Yb)
 				break

	if (xxxb == 0 and yyyb ==1):
		xxxb = senddb[0][2]
		yyyb = senddb[0][3]
		xxxb = float(xxxb)
		yyyb = float(yyyb)
		xxxb = '%.2f'%xxxb
		yyyb = '%.2f'%yyyb
		yyyb = ' '+yyyb
	return xxxb,yyyb


def maptoxyz(inputtt,xx,yy,corect_x1,corect_y1,corect_z1):
	
	worldz = float(inputtt)
	worldz = corect_z1(worldz)
	worldz = '{:07.2f}'.format(worldz)

	worldx = float(xx)
	#worldx = ((worldx/640)*93.3-40)*10
	worldx = corect_x1(worldx)
	worldx = '{:07.2f}'.format(worldx)
	worldy = float(yy)
	#worldy = ((worldy/480)*69-89)*10
	worldy = corect_y1(worldy)
	worldy= '{:07.2f}'.format(worldy)
	return worldx,worldy,worldz



if __name__ == "__main__":
	
	main()



