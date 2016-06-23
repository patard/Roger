/*
 *UltrasonicDemo.pde - Ultrasonic sensor Ranging measure Demo
 *@Author:dragon
 *@DATA:2013-8-7
 *Company website:www.elecfreaks.com
 */
#include <Ultrasonic.h>

int trigpin = 2;//appoint trigger pin
int echopin = 3;//appoint echo pin

Ultrasonic ultrasonic(trigpin,echopin);

void setup()
{
	Serial.begin(9600);//set Serial Baud rate
	Serial.println("Ultrasonic sensor starting!!!!!");
}

void loop()
{
	float cmdistance,indistance;
	long microsec = ultrasonic.timing();
	Serial.print("microsec: ");
	Serial.print(microsec);
	cmdistance = ultrasonic.CalcDistance(microsec,Ultrasonic::CM);//this result unit is centimeter
	indistance = ultrasonic.CalcDistance(microsec,Ultrasonic::IN);//this result unit is inches
	Serial.print(" cmdistance: ");
	Serial.print(cmdistance);
	Serial.print(" indistance: ");
	Serial.println(indistance);
	delay(1000);
}