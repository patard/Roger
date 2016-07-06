#!/usr/bin/python


import sys
import odometry
import interface_i2c
import robot
import time
import subprocess


#parse des arguments  
target_dist = float(sys.argv[1])

# initialisation des variables 
Kp_Dist = 500.
Ki_Dist = 0.
Kd_Dist = 0.

cmd_motor = 0.

sum_error = 0.
deltaT = 0.01
prev_error=0.
cmd_motor = 1.
cmd_motor_right = 1.
cmd_motor_left = 1.




#################################################
def pid_dist():
  global sum_error
  global prev_error
  global cmd_motor
  
  sum_error = 0.
  error = float(target_dist) - odometry.distance_M;
  prop = error * Kp_Dist;
  sum_error += error * deltaT;

  derror = (error - prev_error) / deltaT;
  prev_error = error;
  integ = sum_error * Ki_Dist;
  deriv = derror * Kd_Dist;

  cmd = prop + integ + deriv;

  if( cmd < 0) :
    cmd = -cmd
    backward()
  else : 
	forward() 

  if ( cmd > 255 ) :
    cmd = 255.0
  if ( cmd <= 12 ) :
    cmd = .0
  cmd_motor = (int)(cmd)
#################################################

#################################################
def pid_dist_left():
  global sum_error
  global prev_error
  global cmd_motor_left
  
  sum_error = 0.
  error = float(target_dist) - odometry.distance_M;
  prop = error * Kp_Dist;
  sum_error += error * deltaT;

  derror = (error - prev_error) / deltaT;
  prev_error = error;
  integ = sum_error * Ki_Dist;
  deriv = derror * Kd_Dist;

  cmd = prop + integ + deriv;

  if( cmd < 0) :
    cmd = -cmd
    backward_left()
  else : 
	forward() 

  if ( cmd > 255 ) :
    cmd = 255.0
  if ( cmd <= 12 ) :
    cmd = .0
  cmd_motor = (int)(cmd)
#################################################


#################################################
def forward():
  time.sleep(0.01)
  interface_i2c.digitalWrite(robot.wheel_direction_pin_left, 1);
  time.sleep(0.01)
  interface_i2c.digitalWrite(robot.wheel_direction_pin_right, 1);
  time.sleep(0.01)
#################################################

#################################################
def forward_left():
  interface_i2c.digitalWrite(robot.wheel_direction_pin_left, 1);
#################################################
#################################################
def forward_right():
  interface_i2c.digitalWrite(robot.wheel_direction_pin_right, 1);
#################################################

#################################################
def backward() :
  time.sleep(0.01)
  interface_i2c.digitalWrite(robot.wheel_direction_pin_left, 0);
  time.sleep(0.01)
  interface_i2c.digitalWrite(robot.wheel_direction_pin_right, 0);
  time.sleep(0.01)
#################################################

#################################################
def backward_left() :
  interface_i2c.digitalWrite(robot.wheel_direction_pin_left, 0);
  time.sleep(0.01)
#################################################

#################################################
def backward_right() :
  interface_i2c.digitalWrite(robot.wheel_direction_pin_right, 0);
  time.sleep(0.01)
#################################################



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
		pid_dist()
		print 'cmd_motor ' , cmd_motor
		time.sleep(0.01)
		interface_i2c.analogWrite(robot.PWM_pin_right, cmd_motor)
		interface_i2c.analogWrite(robot.PWM_pin_left, cmd_motor)
	except 	IOError:
		subprocess.call(['i2cdetect', '-y', '1'])
		flag = 1
		break
    
	



