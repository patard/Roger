#!/usr/bin/python
 
import interface_i2c
import time

encoder_left_Id = 1
encoder_left_A = 2
encoder_left_B = 3

encoder_right_Id = 0
encoder_right_A = 18
encoder_right_B = 19

PWM_pin_left = 4
PWM_pin_right = 5

wheel_direction_pin_left = 22
wheel_direction_pin_right = 23

encoderResolution = 2652.0
wheel_diameter = 0.135 # meters
wheel_diameter = 0.134 # meters
wheel_distance = 0.28 # meters
wheel_distance = 0.265 # meters

MAX_MOTOR_CMD = 150 # commande max des moteurs
MIN_MOTOR_CMD = 20  # commande min des moteurs

# constante des PID distance et cap
Kp_Dist = 200.
Ki_Dist = 30.
Kd_Dist = 75.

Kp_Dist_abs = 200.
Ki_Dist_abs = 30.
Kd_Dist_abs = 75.

Kp_Cap = 200.
Ki_Cap = 20.
Kd_Cap = 10.

Kp_Cap_abs = 300.
Ki_Cap_abs = 1.
Kd_Cap_abs = 10.

#################################################
def init() :
	#definition des encodeurs
	interface_i2c.sendEncodersettings( encoder_left_Id, encoder_left_A, encoder_left_B )
	interface_i2c.sendEncodersettings( encoder_right_Id, encoder_right_A, encoder_right_B)
	print 'init done'
#################################################

#################################################
def forward_left():
  interface_i2c.digitalWrite(wheel_direction_pin_left, 1);
#################################################

#################################################
def forward_right():
  interface_i2c.digitalWrite(wheel_direction_pin_right, 1);
#################################################

#################################################
def backward_left() :
  interface_i2c.digitalWrite(wheel_direction_pin_left, 0);
#################################################



#################################################
def backward_right() :
  interface_i2c.digitalWrite(wheel_direction_pin_right, 0);
#################################################

#################################################
def set_cmd_motor_left(motor_cmd) :
	if ( motor_cmd > MAX_MOTOR_CMD ) :
		motor_cmd = MAX_MOTOR_CMD
	if ( motor_cmd <= MIN_MOTOR_CMD ) :
		motor_cmd = 0	
	interface_i2c.analogWrite(PWM_pin_left, int(motor_cmd));	
#################################################

#################################################
def set_cmd_motor_right(motor_cmd) :
	if ( motor_cmd > MAX_MOTOR_CMD ) :
		motor_cmd = MAX_MOTOR_CMD
	if ( motor_cmd <= MIN_MOTOR_CMD ) :
		motor_cmd = 0
	interface_i2c.analogWrite(PWM_pin_right, int(motor_cmd));	
#################################################
