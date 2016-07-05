#!/usr/bin/python


import sys
import odometry
import interface_i2c
import robot
import time

print 'Nb args :',  len(sys.argv)
print 'ArgList :', str(sys.argv)

print 'argv[0] : ', sys.argv[0]

  

Kp_Dist = 500.
Ki_Dist = 0.
Kd_Dist = 0.


cmd_motor = 0.

# test odometry
distL = 0
distR = 0

robot.init()

target_dist = 0.
target_dist = float(sys.argv[1])
#target_dist = 2.
print 'target_dist ' , target_dist

sum_error = 0.
deltaT = 0.3
prev_error=0.
cmd_motor = 1.

def pid_dist():
  global sum_error
  global prev_error
  global cmd_motor
  
  sum_error = 0.
  error = float(target_dist) - odometry.distance_M;
  print 'error ' , error
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
  else : forward() 


  if ( cmd > 255 ) :
    cmd = 255.0
  if ( cmd < 12 ) :
    cmd = .0
    
  cmd_motor = (int)(cmd)

def forward():
  interface_i2c.digitalWrite(robot.wheel_direction_pin_left, 0);
  interface_i2c.digitalWrite(robot.wheel_direction_pin_right, 1);

def backward() :
  interface_i2c.digitalWrite(robot.wheel_direction_pin_left, 1);
  interface_i2c.digitalWrite(robot.wheel_direction_pin_right, 0);



while True:
	time.sleep(deltaT)
	odometry.compute(deltaT)
	print 'DistL : ' , odometry.distance_L, ' m'
	print 'DistR : ', odometry.distance_R, ' m'
	print 'DistM : ', odometry.distance_M, ' m'
	pid_dist()
	print 'cmd_motor ' , cmd_motor
	interface_i2c.analogWrite(robot.PWM_pin_right, cmd_motor)
    
    
	



