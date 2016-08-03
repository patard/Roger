#!/usr/bin/python


import sys
import odometry
import interface_i2c
import robot
import time
import subprocess
import pids
import math




#################################################
def compute_dist(p_current_pos, p_target_pos) :
	l_distance = math.sqrt( (p_target_pos[0]-p_current_pos[0])*(p_target_pos[0]-p_current_pos[0]) + 
	(p_target_pos[1]-p_current_pos[1])*(p_target_pos[1]-p_current_pos[1]) +
	(p_target_pos[2]-p_current_pos[2])*(p_target_pos[2]-p_current_pos[2]) )
	return l_distance
#################################################

#################################################
def compute_cap(p_current_ori, p_current_pos, p_target_pos) :
	l_cap = [0. ,  0., 0.]
	

#	l_cap[0] = math.atan2(p_current_pos[1]-p_target_pos[1], p_current_pos[0]-p_target_pos[0])
	l_cap[0] = math.atan2(p_target_pos[0]-p_current_pos[0], p_target_pos[1]-p_current_pos[1])
	
	return l_cap
#################################################





_PI_ = 3.1415926535897932384626


# initialisation des variables 
deltaT = 0.175
deltaT = 0.2

target_position_X = 0.
target_position_Y = 0.
target_position_Z = 0.

initial_position    = [0. , 0. , 0.] # meters
initial_orientation = [0. , 0. , 0.] # rad

current_position    = [0. , 0. , 0.] # meters
current_orientation = [0. , 0. , 0.] # rad


# parse des arguments
if (len(sys.argv) >= 2):  
	target_position_X = float(sys.argv[1])
if (len(sys.argv) >= 3):  
	target_position_Y = float(sys.argv[2])
if (len(sys.argv) >= 4):  
	target_position_Z = float(sys.argv[3])
target_position = [target_position_X , target_position_Y , target_position_Z] # meters


current_position = initial_position
current_orientation = initial_orientation



#-----------------
print 'Nb args :',  len(sys.argv)
print 'ArgList :', str(sys.argv)
print 'current_position ' , current_position
print 'current_orientation ' , current_orientation

print 'target_position ' , target_position



# initialisation

robot.init()
pid_dist = pids.PID_control(robot.Kp_Dist, robot.Ki_Dist, robot.Kd_Dist)
pid_cap = pids.PID_control(robot.Kp_Cap, robot.Ki_Cap, robot.Kd_Cap)



target_dist = compute_dist(current_position, target_position)
print 'target_dist = ' , target_dist

target_cap = compute_cap(current_orientation, current_position, target_position)
print 'target_cap  = ' , target_cap, ' ( ', target_cap[0]*180./_PI_, ' deg)'



pid_dist.SetTarget(target_dist)
pid_cap.SetTarget(target_cap[0])
tmp_it = 9





# boucle principale
while True:
	try:
		tmp_it += 1
		trace_active = 1
	#	if (tmp_it > 10) :
		trace_active = 1
		print ' '

		time.sleep(deltaT)
		
		
		odometry.compute(deltaT, trace_active)
		if (trace_active) :
			tmp_it = 0
			print 'odometry.position = ' , odometry.position_current
			print 'odometry.orientation = ' , odometry.orientation_current, ' => cap = ', odometry.orientation_current[0]*180./_PI_, ' deg)'

		error_dist = float(target_dist) - odometry.distance_M;
		print 'error_dist (', error_dist, ' )'

		cmd_motor_dist = 0.
		"""
		l_Distance = compute_dist(odometry.position_current, target_position)
		print 'odometry.position_current(',odometry.position_current, ') Vs target_position(',target_position, ') -> new l_Distance = ' , l_Distance

		cmd_motor_dist = pid_dist.pid_compute_new(l_Distance, deltaT)
		"""
		cmd_motor_dist = pid_dist.pid_compute(odometry.distance_M, deltaT)
		
		print 'target_cap[0] : ', target_cap[0]*180./_PI_, ' deg)'
		print 'odometry.cap_rad : ', odometry.cap_rad*180./_PI_, ' deg)'
		
		error_cap = (float(target_cap[0]) - odometry.cap_rad);
		print 'error_cap (', error_cap, ') -> ' , error_cap*180./_PI_, ' deg)'
		cmd_motor_cap = 0.
		cmd_motor_cap = pid_cap.pid_compute(odometry.cap_rad, deltaT)

		print '___error_dist (', error_dist, ') -> cmd_motor_dist ' , cmd_motor_dist
		print '___error_cap (', error_cap, ') -> cmd_motor_cap ' , cmd_motor_cap
		

		# fusion des commandes moteur distance et cap
		cmd_motor_left  = +cmd_motor_dist - cmd_motor_cap
		cmd_motor_right = +cmd_motor_dist + cmd_motor_cap
		print 'cmd_motors : ' , cmd_motor_left, ' ', cmd_motor_right
		

		if( cmd_motor_left < 0) :
			cmd_motor_left = -cmd_motor_left
			robot.backward_left()
		else : 
			robot.forward_left() 

		if( cmd_motor_right < 0) :
			cmd_motor_right = -cmd_motor_right
			robot.backward_right()
		else : 
			robot.forward_right()

		print ' => cmd_motors : ' , cmd_motor_left, ' ', cmd_motor_right
		robot.set_cmd_motor_left(cmd_motor_left)
		robot.set_cmd_motor_right(cmd_motor_right)
					
					


		
	except 	IOError:
		subprocess.call(['i2cdetect', '-y', '1'])
		flag = 1
#		break
    



