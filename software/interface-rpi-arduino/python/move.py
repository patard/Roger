#!/usr/bin/python


import sys
import odometry
import interface_i2c
import robot
import time
import subprocess
import pids


_PI_ = 3.1415926535897932384626

# parse des arguments  
target_dist = float(sys.argv[1])
target_cap = 0

if (len(sys.argv) >= 3):
	target_cap = float(sys.argv[2])

# initialisation des variables 
deltaT = 0.01
deltaT = 0.175


#-----------------
print 'Nb args :',  len(sys.argv)
print 'ArgList :', str(sys.argv)
print 'target_dist ' , target_dist
print 'target_cap ' , target_cap


# initialisation
robot.init()

pid_dist = pids.PID_control(robot.Kp_Dist, robot.Ki_Dist, robot.Kd_Dist)
pid_dist.SetTarget(target_dist)

pid_cap = pids.PID_control(robot.Kp_Cap, robot.Ki_Cap, robot.Kd_Cap)
pid_cap.SetTarget(target_cap)

tmp_it = 0

# boucle principale
while True:
	try:
		tmp_it += 1
		trace_active = 0
		if (tmp_it > 10) :
			trace_active = 1
		print ' '

		time.sleep(deltaT)
		
		
		odometry.compute(deltaT, trace_active)
		if (trace_active) :
			tmp_it = 0
			print 'DistL : ', odometry.distance_L, ' m'
			print 'DistR : ', odometry.distance_R, ' m'
			print 'DistM : ', odometry.distance_M, ' m'
			print 'Cap_rad : ', odometry.cap_rad, ' rad (', odometry.cap_rad*180./_PI_, ' deg)'

		error_dist = float(target_dist) - odometry.distance_M;
		cmd_motor_dist = pid_dist.pid_compute(odometry.distance_M, deltaT)
		
		error_cap = (float(target_cap) - odometry.cap_rad);
		cmd_motor_cap = pid_cap.pid_compute(odometry.cap_rad, deltaT)

		print 'error_dist (', error_dist, ') -> cmd_motor_dist ' , cmd_motor_dist
		print 'error_cap (', error_cap, ') -> cmd_motor_cap ' , cmd_motor_cap
		

		# fusion des commandes moteur distance et cap
		cmd_motor_left  = +cmd_motor_dist - cmd_motor_cap 
		cmd_motor_right = +cmd_motor_dist + cmd_motor_cap
		print 'cmd_motors : ' , cmd_motor_left, ' ', cmd_motor_right
		

		if( cmd_motor_left < 0) :
			cmd_motor_left = -cmd_motor_left
			robot.backward_left()
#			print 'robot.backward_left'
		else : 
			robot.forward_left() 
#			print 'robot.forward_left'

		if ( cmd_motor_left > 255 ) :
			cmd_motor_left = 255
		if ( cmd_motor_left <= 25) :
			cmd_motor_left = 0

		if( cmd_motor_right < 0) :
#			print 'robot.backward_right'
			cmd_motor_right = -cmd_motor_right
			robot.backward_right()
		else : 
			robot.forward_right()
#			print 'robot.forward_right'

		if ( cmd_motor_right > 255 ) :
			cmd_motor_right = 255
		if ( cmd_motor_right <= 25 ) :
			cmd_motor_right = 0
		
		print ' => cmd_motors : ' , cmd_motor_left, ' ', cmd_motor_right
#		interface_i2c.analogWrite(robot.PWM_pin_left, cmd_motor_left)
		robot.set_cmd_motor_left(cmd_motor_left)
#		interface_i2c.analogWrite(robot.PWM_pin_right, cmd_motor_right)
		robot.set_cmd_motor_right(cmd_motor_right)
					

			
	except 	IOError:
		subprocess.call(['i2cdetect', '-y', '1'])
		flag = 1
#		break
    
	


