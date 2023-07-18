#!/usr/bin/python

import smbus as smbus
import time

#
bus = smbus.SMBus(1)
address = 0x05

#defintion des identifiants de message
PIN_MODE_MSG_ID = 0x01
DIGITAL_READ_MSG_ID = 0x02
DIGITAL_WRITE_MSG_ID  = 0x03
DIGITAL_WRITES_MSG_ID = 0x04
ANALOG_READ_MSG_ID  = 0x05
ANALOG_WRITE_MSG_ID  = 0x06
DEFINE_ENCODER_MSG_ID  = 0x07
GET_ENCODER_COUNTER_MSG_ID = 0x08
GET_SOFT_VERSION_MSG_ID = 0x09
GET_STATUS_MSG_ID = 0x0A
GET_TYPE_ARDUINO_MSG_ID = 0x0B
GET_IDL_VERSION_MSG_ID = 0x0C


INPUT_PIN_MODE  = 0
OUTPUT_PIN_MODE = 1
PULLUP_PIN_MODE = 2

DIGITAL_LOW  = 0
DIGITAL_HIGH = 1

RIGHT_WHEEL = 5
DIR_RIGHT_WHEEL = 23
LEFT_WHEEL = 4
DIR_LEFT_WHEEL = 22

DIR_FORWARD = 1
DIR_BACKWARD = 0

CMD_RIGHT_WHEEL = 0
CMD_LEFT_WHEEL = 0

ENCODER_RIGHT = 0
ENCODER_LEFT = 1

_PI_ = 3.1415926535897932384626

    
    
def getIdlVersion():
    print ("Envoi de GetIdlVersion")
    tmp = bus.read_i2c_block_data(address, GET_IDL_VERSION_MSG_ID)
    retour = str(tmp[1]>>4) +  '.'+ str(tmp[1]&0x0F);
    return retour


def getSoftVersion():
    print ("Envoi de getSoftVersion")
    tmp = bus.read_i2c_block_data(address, GET_SOFT_VERSION_MSG_ID)
    retour = str(tmp[1]>>4) +  '.'+ str(tmp[1]&0x0F);
    return retour

def getStatus():
    print ("Envoi de getStatus")
    tmp = bus.read_i2c_block_data(address, GET_STATUS_MSG_ID)
    print "tmp[0] = ", tmp[0]
    retour = tmp[1];
    return retour

def getTypeArduino():
    print ("Envoi de getTypeArduino")
    tmp = bus.read_i2c_block_data(address, GET_TYPE_ARDUINO_MSG_ID)
    print "tmp[0] = ", tmp[0]
    retour = tmp[1];
    return retour
    

def sendEncodersettings( p_IdEncoder, p_NoPinA, p_NoPinB ):
    print "Envoi de DefineEncoder", p_IdEncoder, p_NoPinA, p_NoPinB
    bus.write_i2c_block_data(address, DEFINE_ENCODER_MSG_ID, [ p_IdEncoder, p_NoPinA, p_NoPinB])
    

def getEncoderCounter( p_IdEncoder):
    print "Envoi de getEncoderCounter", p_IdEncoder
    counter = 0;
    bus.write_i2c_block_data(address, GET_ENCODER_COUNTER_MSG_ID,  [p_IdEncoder])
    time.sleep(0.001)
    retour = bus.read_i2c_block_data(address, GET_ENCODER_COUNTER_MSG_ID)
    counter =(retour[2]+ ((retour[1] & 0x0F) <<8))
    if (retour[1] & 0x10) :
        counter *= -1
    return counter


def setPinMode(p_Pin, p_Mode):
    if (p_Mode == INPUT_PIN_MODE) :   print "Envoi de PinMode", p_Pin, " INPUT"
    if (p_Mode == OUTPUT_PIN_MODE) :   print "Envoi de PinMode", p_Pin, " OUTPUT"
    if (p_Mode == PULLUP_PIN_MODE) :   print "Envoi de PinMode", p_Pin, " PULLUP"
    l_Param = p_Mode | (p_Pin<<2)
    bus.write_i2c_block_data(address, PIN_MODE_MSG_ID, [ l_Param])
    
def digitalRead(p_Pin):
    print "Envoi de digitalRead", p_Pin
    bus.write_i2c_block_data(address, DIGITAL_READ_MSG_ID,  [p_Pin])
    retour = bus.read_i2c_block_data(address, DIGITAL_READ_MSG_ID)
    if ((retour[1] & 0x01) == 1) : val = "HIGH"
    else : val = "LOW"
    return val

def digitalWrite(p_Pin, p_Value):
    print "Envoi de digitalWrite", p_Pin, p_Value
    l_Param = p_Value | (p_Pin<<2)
    bus.write_i2c_block_data(address, DIGITAL_WRITE_MSG_ID, [ l_Param])
    
def digitalWrites(p_Pin1, p_Value1, p_Pin2, p_Value2):
    print "Envoi de digitalWrites", p_Pin1, p_Value1, p_Pin2, p_Value2
    l_Param1 = p_Value1 | (p_Pin1<<2)
    l_Param2 = p_Value2 | (p_Pin2<<2)
    bus.write_i2c_block_data(address, DIGITAL_WRITES_MSG_ID, [ l_Param1, l_Param2])

def analogWrite(p_Pin, p_Value):
    print "Envoi de analogWrite", p_Pin, p_Value
    bus.write_i2c_block_data(address, ANALOG_WRITE_MSG_ID, [ p_Pin, p_Value])

def analogRead(p_Pin):
    print "Envoi de analogRead", p_Pin
    bus.write_i2c_block_data(address, ANALOG_READ_MSG_ID,  [p_Pin])
    retour = bus.read_i2c_block_data(address, ANALOG_READ_MSG_ID)
    val = (retour[1] << 8) | retour[2]
    print "val = ", val
    return val
   



    
##try:
        

print "\n==========================="
print "   IDL_VERSION"
print "==========================="
idlVersion = getIdlVersion()
print "arduino has sent idlVersion : ", idlVersion


print "\n==========================="
print "   ANALOG_WRITE"
print "==========================="
print "analogWrite(9,255) "
analogWrite(RIGHT_WHEEL, CMD_RIGHT_WHEEL)
analogWrite(LEFT_WHEEL, CMD_LEFT_WHEEL)
digitalWrite(DIR_RIGHT_WHEEL, DIR_FORWARD)
digitalWrite(DIR_LEFT_WHEEL, DIR_FORWARD)

time.sleep (1)
#analogWrite(RIGHT_WHEEL, CMD_RIGHT_WHEEL + 20)
#analogWrite(LEFT_WHEEL, CMD_LEFT_WHEEL + 20)

# definition encoder
sendEncodersettings(ENCODER_LEFT, 2, 3)
sendEncodersettings(ENCODER_RIGHT, 18, 19)

distL = 0
distR = 0

while True:
	time.sleep(0.3)
	encodL = getEncoderCounter(ENCODER_LEFT)
	encodR = getEncoderCounter(ENCODER_RIGHT)
	encodL /= 2652.0
	encodR /= 2652.0
	distL = encodL * 13.5 * _PI_ 
	distR = encodR * 13.5 * _PI_
	print "DistL : " , distL
	print "DistR : ", distR
	

print

##except:
##    print "finish"


