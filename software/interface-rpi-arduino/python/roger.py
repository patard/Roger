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


def getEncoderCounter( p_IdEncoder):
    print "Envoi de getEncoderCounter", p_IdEncoder
    counter = 0;
    bus.write_i2c_block_data(address, GET_ENCODER_COUNTER_MSG_ID,  [p_IdEncoder])
    retour = bus.read_i2c_block_data(address, GET_ENCODER_COUNTER_MSG_ID)
#    print "MSG ID = ", retour[0]
#    print "encoder ID = ", retour[1] >> 5
    counter =(retour[2]+ ((retour[1] & 0x0F) <<8))
#    print "|counter| = ", counter
    if (retour[1] & 0x10) :
        counter *= -1
#       print "compteur negatif => counter = " , counter
#    print "retour = ", retour[0], retour[1], retour[2]
    
    return counter
    
    
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
#    print "retour = ", retour
#    print "MSG ID = ", retour[0]
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
   

    
try:
        

    print "\n==========================="
    print "   IDL_VERSION"
    print "==========================="
    idlVersion = getIdlVersion()
    print "arduino has sent idlVersion : ", idlVersion

    print "\n==========================="
    print "   SOFT_VERSION"
    print "==========================="
    softVersion = getSoftVersion()
    print "arduino has sent idlVersion : ", softVersion

    
    print "\n==========================="
    print "   TYPE_ARDUINO"
    print "==========================="
    typeArduino = getTypeArduino()
    print "arduino has sent type : ", typeArduino

    print "\n==========================="
    print "   STATUS"
    print "==========================="
    status = getStatus()
    print "arduino has sent type : ", status

    print "\n==========================="
    print "   PIN_MODE"
    print "==========================="
    print "set pinMode(9, OUTPUT "
    setPinMode(9, OUTPUT_PIN_MODE)
    print "set pinMode(8, PULLUP_PIN_MODE "
    setPinMode(8, PULLUP_PIN_MODE)


    print "\n==========================="
    print "   DIGITAL_READ"
    print "==========================="
    print "digitalRead(8) "
    value = digitalRead(8)
    print "arduino has sent digital value : ", value


    print "\n==========================="
    print "   ANALOG_WRITE"
    print "==========================="
    print "analogWrite(9,255) "
    analogWrite(9, 255)
    time.sleep (1)
    analogWrite(9, 128)

    

    print "\n==========================="
    print "   ANALOG_READ"
    print "==========================="
    print "analogRead(0) "
    value = analogRead(0)
    print "arduino has sent analog value : ", value



# close
    
    print "\n==========================="
    print "   DIGITAL_WRITE"
    print "==========================="
    print "set digitalWrite(13, HIGH "
    digitalWrite(7, DIGITAL_HIGH)
    time.sleep (1)
    digitalWrite(8, DIGITAL_LOW)
    time.sleep (1)
    digitalWrite(10, DIGITAL_HIGH)
    time.sleep (1)
    digitalWrite(11, DIGITAL_LOW)
    time.sleep (1)

    print "\n==========================="
    print "   DIGITAL_WRITES"
    print "==========================="
    print "set digitalWrites(13, HIGH, 9, LOW) and  digitalWrites(13, LOW, 9, HIGH)"
    digitalWrites(13, DIGITAL_HIGH, 9, DIGITAL_LOW)
    time.sleep (1)
    digitalWrites(13, DIGITAL_LOW, 9, DIGITAL_HIGH)
    time.sleep (1)
    digitalWrites(13, DIGITAL_HIGH, 9, DIGITAL_LOW)
    time.sleep (1)
    digitalWrites(13, DIGITAL_LOW, 9, DIGITAL_HIGH)
    time.sleep (1)

#   close
    print "\n==========================="
    print "   DEFINE_ENCODER"
    print "==========================="
    print "Send EncoderSettings ", 1, 5, 4
    sendEncodersettings(0, 2, 3)
    sendEncodersettings(1, 5, 4)
    print "Send EncoderSettings ", 0, 2, 3
    



    time.sleep (5)

    print "\n==========================="
    print "   GET_ENCODER_COUNTER"
    print "==========================="
    p_IdEncoder = 1
    counter = getEncoderCounter(p_IdEncoder);
    print "getEncoderCounter ", p_IdEncoder, " return : ", counter
 
    print
    
except:
    print "finish"


