#!/usr/bin/python

import sys
import interface_i2c
import robot


robot.init()

interface_i2c.analogWrite(robot.PWM_pin_right, 0)
interface_i2c.analogWrite(robot.PWM_pin_left, 0)
    
    
	



