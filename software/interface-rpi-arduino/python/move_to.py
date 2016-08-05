#!/usr/bin/python

"""
  Script permettant de piloter le deplacement du robot,
  dans un repere initialement auto-centre

  Usage move_to X [Y=0.] [Z=0.]
	X : Abscisse en m
	Y : Ordonnee en m
	Z : Cote en m
	(Y et Z sont optionnels)
"""

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

def correct_radian_range (p_radian) :
	# keep value in range ]-Pi;Pi]
	if (p_radian <= -_PI_) : 
		p_radian += 2.*_PI_	
	elif (p_radian > _PI_) : 
		p_radian -= 2.*_PI_				
	return p_radian

#################################################
def compute_cap(p_current_ori, p_current_pos, p_target_pos, p_sens=0) :
	l_cap = [0.,  0., 0.]
	l_cap[0] = math.atan2(p_target_pos[0]-p_current_pos[0], p_target_pos[1]-p_current_pos[1])

	l_cap[0] = correct_radian_range(l_cap[0])
	"""
	if (l_cap[0] <= -_PI_) : 
		l_cap[0] += 2.*_PI_	
	if (l_cap[0] > _PI_) : 
		l_cap[0] -= 2.*_PI_				
	"""
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
if (len(sys.argv) == 1):  
	print '\n==========================='
	print ' Usage move_to X [Y=0.] [Z=0.]'
	print '  X : Abscisse en m'
	print '  Y : Ordonnee en m'
	print '  Z : Cote en m'
	print '    (Y et Z sont optionnels)'
	print '===========================\n'
	sys.exit()
	
	
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
pid_dist = pids.PID_control(robot.Kp_Dist_abs, robot.Ki_Dist_abs, robot.Kd_Dist_abs)
pid_cap = pids.PID_control(robot.Kp_Cap_abs, robot.Ki_Cap_abs, robot.Kd_Cap_abs)

target_dist = compute_dist(current_position, target_position)
if __debug__: print 'target_dist = ' , target_dist

target_cap = compute_cap(current_orientation, current_position, target_position)


pid_dist.SetTarget(target_dist)
pid_cap.SetTarget(-target_cap[0])
if __debug__: print 'target_cap  = ' , -target_cap[0], ' ( ', -target_cap[0]*180./_PI_, ' deg)'


# boucle principale
while True:
	try:
		trace_active = 1
		time.sleep(deltaT)
		if __debug__: print ' '

		# Calcul de la position courante
		odometry.compute(deltaT, trace_active)
		if __debug__: print 'odometry : position' , odometry.position_current, ' orientation' , odometry.orientation_current, ' (cap ', odometry.orientation_current[0]*180./_PI_, ' deg)'
		
		# Calcul des consignes en distance et en orientation
		l_Distance = compute_dist(odometry.position_current, target_position)
		l_Cap = compute_cap(odometry.sum_delta_cap_rad, odometry.position_current, target_position)

		error_dist = float(target_dist) - odometry.distance_M;
		if __debug__: print 'target_dist :', target_dist, ', odometry.distance_M :', odometry.distance_M, ' -> error_dist ' , error_dist, ' <-> l_Distance :', l_Distance
		
		error_cap = correct_radian_range(-(float(l_Cap[0]) + odometry.cap_rad));
		if __debug__:print 'target   : position ' ,target_position, '\t distance(' , l_Distance, ') cap(', l_Cap[0]*180./_PI_, ' deg )'

		# Calcul des commandes moteurs associees
		cmd_motor_dist = pid_dist.pid_compute_new(l_Distance, deltaT)
		cmd_motor_cap  = pid_cap.pid_compute_new(error_cap, deltaT)
		if __debug__: print '___error_dist :', error_dist, ' (', error_dist*100.    , 'cm ) -> cmd_motor_dist ' , cmd_motor_dist
		if __debug__: print '___error_cap  :', error_cap,  ' (', error_cap*180./_PI_, 'deg) -> cmd_motor_cap  ' , cmd_motor_cap
		
		
		if (error_dist > 0.02) :	# si l'erreur de positionnement est superieure a 2 cm
			# fusion des commandes moteur distance et cap
			cmd_motor_left  = +cmd_motor_dist - cmd_motor_cap
			cmd_motor_right = +cmd_motor_dist + cmd_motor_cap
			if __debug__: print '              => cmd_motors : ' , cmd_motor_left, ' ', cmd_motor_right, ' ==> '
			

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

			# On applique les commandes moteurs
			robot.set_cmd_motor_left(cmd_motor_left)
			robot.set_cmd_motor_right(cmd_motor_right)
		else : # sinon on considere que l'objectif est atteint
			robot.set_cmd_motor_left(0)
			robot.set_cmd_motor_right(0)
			if __debug__: print '          OBJECTIF ATTEINT : ', odometry.position_current
					
	except 	IOError:
		subprocess.call(['i2cdetect', '-y', '1'])
		flag = 1
#		break
    



