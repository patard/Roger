#!/usr/bin/python


import sys
import odometry
import interface_i2c
import robot
import time
import subprocess



# initialisation des variables 
Kp_Dist = 500.
Ki_Dist = 0.
Kd_Dist = 0.

cmd_motor = 0.

sum_error = 0.
deltaT = 0.01
prev_error=0.
#cmd_motor = 1.


#################################################
def pid_dist(target_dist):
  global sum_error
  global prev_error
  
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
  
  return (int)(cmd)
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
def backward() :
  time.sleep(0.01)
  interface_i2c.digitalWrite(robot.wheel_direction_pin_left, 0);
  time.sleep(0.01)
  interface_i2c.digitalWrite(robot.wheel_direction_pin_right, 0);
  time.sleep(0.01)
#################################################





