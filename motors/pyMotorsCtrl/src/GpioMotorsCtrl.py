'''
Created on 27 mars 2016

@author: patrick
'''

import RPi.GPIO as GPIO # comment ajouter un dépot RPi sur ubuntu? est-ce que ca un sens d'ailleurs?

from time import sleep

GPIO.setmode(GPIO.BOARD) # choose BCM or BOARD numbering schemes. 

Motor1A = 23
Motor1B = 24
Motor1E = 13 # PWM that will enable 

GPIO.setup(Motor1A, GPIO.OUT)
GPIO.setup(Motor1B, GPIO.OUT)

pwmMotor1 = GPIO.PWM(Motor1E, 100) # create obkect for PWM on port 13 at 100 Hertz
pwmMotor1.start(50) # start with a duty cycle of 50%

# now the fun starts, we'll vary the duty cycle to   
# dim/brighten the leds, so one is bright while the other is dim  
  
pause_time = 0.02           # you can change this to slow down/speed up


try:  
    while True:  
        for i in range(0,101):      # 101 because it stops when it finishes 100  
            pwmMotor1.ChangeDutyCycle(i)  
            sleep(pause_time)  
        for i in range(100,-1,-1):      # from 100 to zero in steps of -1  
            pwmMotor1.ChangeDutyCycle(i)  
            sleep(pause_time)  
  
except KeyboardInterrupt:  
    pwmMotor1.stop()            # stop the white PWM output  
    GPIO.cleanup()          # clean up GPIO on CTRL+C exit  