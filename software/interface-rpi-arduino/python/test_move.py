#!/usr/bin/python


import sys
import odometry
import interface_i2c
import robot
import time
import subprocess
import pids

#parse des arguments  
target_dist = float(sys.argv[1])

# initialisation des variables 
deltaT = 0.01

print 'Nb args :',  len(sys.argv)
print 'ArgList :', str(sys.argv)
print 'target_dist ' , target_dist

# initialisation
robot.init()

# boucle principale
while True:
	try:
		time.sleep(deltaT)
		odometry.compute(deltaT)
		print 'DistL : ', odometry.distance_L, ' m'
		print 'DistR : ', odometry.distance_R, ' m'
		print 'DistM : ', odometry.distance_M, ' m'
		cmd_motor = pids.pid_dist(target_dist)
		print 'cmd_motor ' , cmd_motor
		if (cmd_motor <= 12) : 
			cmd_motor = 0
		time.sleep(0.01)
		interface_i2c.analogWrite(robot.PWM_pin_right, cmd_motor)
		interface_i2c.analogWrite(robot.PWM_pin_left, cmd_motor)
	except 	IOError:
		subprocess.call(['i2cdetect', '-y', '1'])
		flag = 1
#		break
    
	



