#!/usr/bin/python

import interface_i2c
import robot
import time

_PI_ = 3.1415926535897932384626

position_current=[0. , 0. , 0.] # meters
position_prev=[0. , 0. , 0.] # meters

orientation_current=[0. , 0. , 0.] # rad
orientation_prev=[0. , 0. , 0.] # rad

distance_L = 0. # meters
distance_R = 0. # meters
distance_M = 0. # meters

distance_prev_L = 0.  # meters
distance_prev_R = 0.  # meters
distance_prev_M = 0.  # meters



def compute(delta_t):
	
	global distance_L
	global distance_R
	global distance_M

	global distance_prev_L
	global distance_prev_R
	global distance_prev_M
	
	distance_prev_R = distance_R
	distance_prev_L = distance_L
	distance_prev_M = distance_M
  
	cptL = interface_i2c.getEncoderCounter(robot.encoder_left_Id)
	cptR = interface_i2c.getEncoderCounter(robot.encoder_right_Id)
	print 'cptL : ', cptL, ' cptR : ', cptR

     
	cptL /= robot.encoderResolution
	cptR /= robot.encoderResolution

	distance_L = cptL * robot.wheel_diameter * _PI_ 
	distance_R = cptR * robot.wheel_diameter * _PI_
	distance_M += (distance_L + distance_R) / 2.0


# test odometry

distL = 0
distR = 0

robot.init()

while True:
	time.sleep(0.3)
	compute(0.3)
	print "DistL : " , distance_L, ' m'
	print "DistR : ", distance_R, ' m'
	print "DistM : ", distance_M, ' m'
