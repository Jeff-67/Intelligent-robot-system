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



	#mapping

	test_camera_1=np.array([160.74,394.56,0.91])  #357.42', ' 381.57

	test_arm_1   =np.array([-119.558,-361.734,91.464])

	test_camera_2=np.array([268.60, 307.82,0.90])

	test_arm_2   =np.array([11.177,-480.788,90.600])  

	test_camera_3=np.array([184.97, 383.24,0.82 ]) #'153.84', ' 357.38'

	test_arm_3   =np.array([-85.977,-381.862,80.218 ])

	test_camera_4=np.array([231.06,258.40])
	test_arm_4   =np.array([-38.115,-518.495])


	test_camera_5=np.array([265.81,389.53])
	test_arm_5   =np.array([7.93,-358.24])

	test_camera_6=np.array([310.3019,378.8711])
	test_arm_6   =np.array([324.556,-374.19])

	camera_x = np.array([test_camera_1[0],test_camera_2[0]]) #insert camera x coordinates.......,,test_camera_5[0],test_camera_4[0],test_camera_3[0]

	arm_x = np.array([test_arm_1[0],test_arm_2[0]])  #insert arm x coordinates........,,test_arm_5[0],test_arm_4[0],test_arm_3[0]

	para_for_x = np.polyfit(camera_x, arm_x, 1)
	

	camera_y = np.array([test_camera_1[1],test_camera_2[1]])  #insert camera y coordinates,test_camera_[1],test_camera_5[1],test_camera_4[1],test_camera_3[1]

	arm_y = np.array([test_arm_1[1],test_arm_2[1]])  #insert arm y coordinates,test_arm_5[1],test_arm_5[1]],test_arm_4[1],test_arm_3[1]

	para_for_y = np.polyfit(camera_y, arm_y, 1)


	camera_z = np.array([test_camera_1[2],test_camera_2[2]])  #insert camera z coordinates,test_camera_3[2]

	arm_z = np.array([test_arm_1[2],test_arm_2[2]])  #insert arm z coordinates,test_arm_3[2]

	para_for_z =np.polyfit(camera_z, arm_z, 1)



	corect_x = np.poly1d(para_for_x)  #mapping function    
	corect_y = np.poly1d(para_for_y)  #mapping function

	corect_z = np.poly1d(para_for_z)  #mapping function
	
	os.system("/usr/local/bin/rs-save-to-disk")
	Yolo = subprocess.Popen("./darknet detector test data/obj.data yolov3-tiny-obj.cfg backup/yolov3-tiny-obj_10000.weights", stdout=subprocess.PIPE, shell=True)
	
	while (1):


		start=timeit.default_timer()


		out2 = subprocess.check_call('echo 0 > /sys/class/gpio/gpio396/value', shell = True)
		out3 = subprocess.check_call('echo 0 > /sys/class/gpio/gpio388/value', shell = True)
		
		print("ready")
		

		

		with warnings.catch_warnings():
			warnings.simplefilter("ignore")
			
			while (1):
				Yolo = np.loadtxt("file.txt", dtype=str)
				passcode = np.size(Yolo)
				os.system("/usr/local/bin/rs-save-to-disk")
				print passcode
				if (passcode != 0 ):
					break

		c=[];

		if(Yolo!=c):
			
			print Yolo
			xx,yy = maptorealsense_andrecongnizesweetspot(Yolo)
			print(xx,yy)
			if (xx!= 0 and yy != 1):
				r = './rs-measure '+xx+yy
				print(r)
				(output,out) = commands.getstatusoutput(r)
				print out
				x,y,z = maptoxyz(out,xx,yy,corect_x,corect_y,corect_z)
			
	
				print(x,y,z)

				a = ser.read(3)

				print(a)

				
				if(a=='GO1' or 'YES'):
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
						print to_arm_x[i]
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
		
					a=""
					out2 = subprocess.check_call('echo 0 > /sys/class/gpio/gpio396/value', shell = True)
					out3 = subprocess.check_call('echo 0 > /sys/class/gpio/gpio388/value', shell = True)
			
			

				if(a=='GO2'):
				
					print (a)
					out22 = subprocess.check_call('echo 1 > /sys/class/gpio/gpio396/value', shell = True)
					out33 = subprocess.check_call('echo 1 > /sys/class/gpio/gpio388/value', shell = True)
					xd,yd = getbadmango(Yolo)
					while (xd == 0 and yd == 1):
						os.system("/usr/local/bin/rs-save-to-disk")
						Yolo = np.loadtxt("file.txt", dtype=str)
						xd,yd = getbadmango(Yolo)
						if(xd != 0 and yd != 1):
							break


					r = './rs-measure '+xd+yd
					print(r)
					(output,out) = commands.getstatusoutput(r)
			
					xd,yd,zd = maptoxyz(out,xd,yd,corect_x,corect_y,corect_z)

					xs = str(xd)
					ys = str(yd)
					zs = str(zd)

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
						print to_arm_x[i]

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
	

					
				
					ser.write(chr(44))	#endcode1231231231321
		
					a=""
					out2 = subprocess.check_call('echo 0 > /sys/class/gpio/gpio396/value', shell = True)
					out3 = subprocess.check_call('echo 0 > /sys/class/gpio/gpio388/value', shell = True)
			
		
				if (a=='GO3'):
					
					print a 
					
					while(1):					
						cc = ifgrippable(Yolo,corect_x,corect_y)
						if(cc == 'YES'):
							break
	

		stop =timeit.default_timer()
	
		print (stop-start)



def ifgrippable(send0,corect_x22,corect_y22):
	

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

		X = send0[j][0]
		Y = send0[j][1]
		print "hi"
		if (480>X and X>105 and 420>Y and Y>270):

			print "YEAH"				
			stirlx = (send0[j+1][0]+send0[j][0])/2
			stirly = (send0[j+1][1]+send0[j][1])/2				
			stirlx = corect_x22(stirlx)-5.5
			stirly = corect_y22(stirly)	
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
				
			ser.write(chr(44))
	out2266 = subprocess.check_call('echo 0 > /sys/class/gpio/gpio396/value', shell = True)
	out3366 = subprocess.check_call('echo 0 > /sys/class/gpio/gpio388/value', shell = True)
	a=ser.read(3)
	return a
	
def getbadmango(send11):
	xxxd = 0
	yyyd = 1

	send111 = np.reshape(send11,(-1,4))
	(row1,col1) = send111.shape
	for jj in range(row1):
		if (send111[jj][0] == "badmango"):
			send1111 = np.delete(send111,0,1)
			send11111 = send1111.astype(np.float)
			XX = send11111[jj][1]
			YY = send11111[jj][2]
			
			if ( 480>XX and XX>105 and 420>YY and YY>270):

				Xb = '%.2f'%XX
				Yb = '%.2f'%YY
				xxxd = str(Xb)
				yyyd = ' '+str(Yb)
 
				break
	return xxxd,yyyd
		 
def maptorealsense_andrecongnizesweetspot(send1):

	xxx = 0
	yyy = 1
	
	send2 = np.reshape(send1, (-1, 4))
	(row1,col1) = send2.shape
	print row1
	for jj in range (row1):

		if (send2[jj][0] == "t_mango_pts"):
			send22 = np.delete(send2, 0, 1)
			send222 = send22.astype(np.float)
			X = send222[jj][1]
			Y = send222[jj][2]
			

			if ( 480>X and X>105 and 420>Y and Y>270):

				X = '%.2f'%X
				Y = '%.2f'%Y
				xxx = str(X)
				yyy = ' '+str(Y)

 				break
				
	return xxx,yyy


def maptoxyz(inputtt,xx1,yy1,corect_x1,corect_y1,corect_z1):
	
	worldz = float(inputtt)
	worldz = corect_z1(worldz)
	worldz = '{:07.2f}'.format(worldz)

	worldx = float(xx1)
	#worldx = ((worldx/640)*93.3-40)*10
	worldx = corect_x1(worldx)+10
	worldx = '{:07.2f}'.format(worldx)
	worldy = float(yy1)
	#worldy = ((worldy/480)*69-89)*10
	worldy = corect_y1(worldy)-3
	worldy= '{:07.2f}'.format(worldy)
	return worldx,worldy,worldz



if __name__ == "__main__":
	
	main()


#if (xxx == 0 and yyy == 1):
#		try:
#			xxx = send2[0][2]
#			yyy = send2[0][3]
#			xxx = float(xxx)
#			yyy = float(yyy)
#			xxx = '%.2f'%xxx
#			yyy = '%.2f'%yyy
#			yyy = ' '+yyy
#		except IndexError:
#			pass
#
