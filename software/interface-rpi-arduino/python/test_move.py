#!/usr/bin/python


import sys
import odometry
import interface_i2c
import robot
import time

print 'Nb args :',  len(sys.argv)
print 'ArgList :', str(sys.argv)

print 'argv[0] : ', sys.argv[0]

def usage():
  print '   python',   sys.argv[0], ' X  Y  angleDeg \n'

if (len(sys.argv) < 3) :
  print '\nArgument error, use :'
  usage()
  sys.exit()
  
  
  
if (isinstance( sys.argv[1], (int, long)) == False) :
  print sys.argv[1], ' est un entier'



# test odometry
distL = 0
distR = 0

robot.init()

while True:
	time.sleep(0.3)
	odometry.compute(0.3)
	print "DistL : " , distance_L, ' m'
	print "DistR : ", distance_R, ' m'
	print "DistM : ", distance_M, ' m'



