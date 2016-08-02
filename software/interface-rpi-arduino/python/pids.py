#!/usr/bin/python


#################################################
class PID_control:

	###########
	def __init__(self, Kp=0., Ki=0., Kd=0.):
		self.InitializeConstants(Kp, Ki, Kd) # initialize constants
		self.SetTarget(0.)   # initialize init target
		
	###########
	def InitializeConstants(self, Kp=0., Ki=0., Kd=0.):
		self.Kp = Kp
		self.Ki = Ki
		self.Kd = Kd

	###########
	def SetTarget(self, target):
		self.prev_error = 0
		self.sum_error = 0
		self.target = target
		
	###########
	def pid_compute(self, new_value, deltaT):
	  """ Performs a PID computation and returns a control value 
	  """

	  error = self.target - new_value   # get error
	   
	  prop = error * self.Kp;           # get proportionnal

	  self.sum_error += error * deltaT;
	  integ = self.sum_error * self.Ki; # get integral

	  derror = (error - self.prev_error) / deltaT;
	  deriv = derror * self.Kd;         # get derivative
	  
	  self.prev_error = error;          # save for next pass

	  pid = prop + integ + deriv;       # compute pid
	  
	#  print 'error (', error, ') => prop (', prop, ') integ(', integ, ') deriv(', deriv, ')'
	  return (int)(pid)
	  
	
#################################################


