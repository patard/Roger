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

cap_rad = 0. # radians
g_cptL = 0
g_cptR = 0

#################################################
def compute(delta_t, trace_activated):
	
	global distance_L
	global distance_R
	global distance_M

	global distance_prev_L
	global distance_prev_R
	global distance_prev_M
	
	global cap_rad
	
	global g_cptR
	global g_cptL
	
	distance_prev_R = distance_R
	distance_prev_L = distance_L
	distance_prev_M = distance_M
  
	cptL = interface_i2c.getEncoderCounter(robot.encoder_left_Id)
	g_cptL += cptL
	cptR = interface_i2c.getEncoderCounter(robot.encoder_right_Id)
 	g_cptR += cptR


	distance_L += cptL / robot.encoderResolution * robot.wheel_diameter * _PI_ 
	distance_R += cptR / robot.encoderResolution * robot.wheel_diameter * _PI_
#	l_distance_L = cptL / robot.encoderResolution * robot.wheel_diameter * _PI_ 
#	l_distance_R = cptR / robot.encoderResolution * robot.wheel_diameter * _PI_
#	distance_M += (l_distance_L + l_distance_R) / 2.0
	distance_M = (g_cptL + g_cptR)/ robot.encoderResolution * robot.wheel_diameter * _PI_ /2
	
	cap_rad = ((g_cptR-g_cptL)/ robot.encoderResolution)*robot.wheel_diameter/robot.wheel_distance*_PI_
	
	if (trace_activated) :
		print 'cap : (',g_cptL, '/', g_cptR, ') -> ' , cap_rad, ' rad (', cap_rad*180./_PI_, ' deg )'		
		print 'g_cptR : ', g_cptR

#################################################


