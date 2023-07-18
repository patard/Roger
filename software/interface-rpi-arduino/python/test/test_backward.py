#!/usr/bin/python


import sys
import interface_i2c
import robot
import subprocess


#-----------------
print 'Nb args :',  len(sys.argv)
print 'ArgList :', str(sys.argv)

# initialisation
robot.init()

# boucle principale
try:
	cmd_motor_left = 50
	cmd_motor_right = 50

	robot.backward_left() 
	robot.backward_right()

	print 'cmd_motors : ' , cmd_motor_left, ' ', cmd_motor_right
	interface_i2c.analogWrite(robot.PWM_pin_left, cmd_motor_left)
	interface_i2c.analogWrite(robot.PWM_pin_right, cmd_motor_right)
				
			
except 	IOError:
	subprocess.call(['i2cdetect', '-y', '1'])
	flag = 1
#		break
    
	


