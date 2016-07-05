#!/usr/bin/python
 
import interface_i2c

encoder_left_Id = 0
encoder_left_A = 2
encoder_left_B = 3

encoder_right_Id = 1
encoder_right_A = 18
encoder_right_B = 19

PWM_pin_left = 4
PWM_pin_right = 5

wheel_direction_pin_left = 22
wheel_direction_pin_right = 23

encoderResolution = 2652.0
wheel_diameter = 0.135 # meters
wheel_distance = 0.28 # meters

delta_T = 0.3


def init() :
  #definition des encodeurs
  interface_i2c.sendEncodersettings( encoder_left_Id, encoder_left_A, encoder_left_B )
  interface_i2c.sendEncodersettings( encoder_right_Id, encoder_right_A, encoder_right_B)



