#!/usr/bin/python


import sys
import time
import smbus as smbus
import interface_i2c

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


tempo = float(sys.argv[1])
afterWriteSleep= float(sys.argv[2])

bus = smbus.SMBus(1)
bus.write_quick(0x05)
address = 0x05



def digitalWrite(p_Pin, p_Value):
	l_Param = p_Value | (p_Pin<<2)
#    bus.write_i2c_block_data(address, DIGITAL_WRITE_MSG_ID, [ l_Param])
	bus.write_byte_data(address, DIGITAL_WRITE_MSG_ID, l_Param)

def digitalRead(p_Pin):
#	bus.write_i2c_block_data(address, DIGITAL_READ_MSG_ID,  [p_Pin])
	bus.write_byte_data(address, DIGITAL_READ_MSG_ID, p_Pin)
	
	time.sleep(afterWriteSleep)
	retour = bus.read_i2c_block_data(address, DIGITAL_READ_MSG_ID)
	if ((retour[1] & 0x01) == 1) : val = "HIGH"
	else : val = "LOW"
	return val
    

def setPinMode(p_Pin, p_Mode):
    if (p_Mode == INPUT_PIN_MODE) :   print "Envoi de PinMode", p_Pin, " INPUT"
    if (p_Mode == OUTPUT_PIN_MODE) :   print "Envoi de PinMode", p_Pin, " OUTPUT"
    if (p_Mode == PULLUP_PIN_MODE) :   print "Envoi de PinMode", p_Pin, " PULLUP"
    l_Param = p_Mode | (p_Pin<<2)
    bus.write_i2c_block_data(address, PIN_MODE_MSG_ID, [ l_Param])
    
def analogWrite(p_Pin, p_Value):
    print "Envoi de analogWrite", p_Pin, p_Value
    p_Value = 200
    bus.write_i2c_block_data(address, ANALOG_WRITE_MSG_ID, [ p_Pin, p_Value])
        
def sendEncodersettings( p_IdEncoder, p_NoPinA, p_NoPinB ):
    bus.write_i2c_block_data(address, DEFINE_ENCODER_MSG_ID, [ p_IdEncoder, p_NoPinA, p_NoPinB])
    
    
def getEncoderCounter( p_IdEncoder):
	counter = 0
#	bus.write_i2c_block_data(address, GET_ENCODER_COUNTER_MSG_ID,  [p_IdEncoder])
	bus.write_byte_data(address, GET_ENCODER_COUNTER_MSG_ID, p_IdEncoder)

	time.sleep(afterWriteSleep)
	retour = bus.read_i2c_block_data(address, GET_ENCODER_COUNTER_MSG_ID)
	print "read_i2c_block_data return ", retour
    
	counter =(retour[2]+ ((retour[1] & 0x0F) <<8))
	if (retour[1] & 0x10) : 		counter *= -1
	return counter
        
# boucle principale
setPinMode(13, OUTPUT_PIN_MODE)
sendEncodersettings(0, 18, 19)
while True:
	time.sleep(tempo)
	digitalWrite(13, 0)
	time.sleep(afterWriteSleep)
	val = digitalRead(14)
	time.sleep(tempo)
	digitalWrite(13, 1)
	time.sleep(afterWriteSleep)
	val = digitalRead(13)
	val = getEncoderCounter( 0)
	
	analogWrite(5, 255)
	time.sleep(afterWriteSleep)
    
