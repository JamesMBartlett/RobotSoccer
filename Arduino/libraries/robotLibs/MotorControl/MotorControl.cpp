/*
 * MotorControl.cpp
 *
 *  Created on: 02/01/2014
 *      Author: james
 */

#include "MotorControl.h"



const int MotorControl::clicksperrev = 16;// when interrupting on one of the two channels on only one side, FALLING or RISING there is 16 clicks per revolution,
					   //if interrupting on changing there is 32 clicks per revolution
const int MotorControl::millispersec = 1000;
const float MotorControl::mtrconst = 1; //defines the rate of reaction to not getting the right speed; in function getNewAimFromFeedback

MotorControl::MotorControl(Motor parMotors[], Encoder parEncoders[], SpeedPWMStruct parStruct){
	for(int i = 0; i < 3; i++){
		motors[i] = parMotors[i];
		encoders[i] = parEncoders[i];
		speedpwmstruct = parStruct;
	}
	overallDesiredVector = Vector(0,0);
	conversionArray = [2.0* onethird, 0, 0, onethird,
					   -onethird, oneonroot3, onethird,
					   -onethird, -oneonroot3, onethird]
	// conversion matrix represent as an array based on inverse of Matrix [ 1 cos(theta2) cos(theta3)
	//																		0 sin(theta2) sin(theta3)
	//																		1/2*pi*r 1/2*pi*r 1/2*p*r]
}

MotorControl::MotorControl(){
}

MotorControl::~MotorControl() {
}

float MotorControl::getIndividualSpeed(int encoder_num){
	signed int dist = encoders[encoder_num].getEncoderDistance(); //distance in number of encoder clicks on one edge
	unsigned long time = encoders[encoder_num].getTimeBetween(); //time in milliseconds
	float speed = float(dist/time); //speed in clicks per millisecond
	speed = speed * millispersec; //speed in clicks per second
	speed = speed / clicksperrev; //speed in revolutions per second

	return speed;
}

float MotorControl::getDesiredIndividualSpeed(int motor_num, float rotation_rate){
	return overallDesiredVector.getMagnitude() * sin((overallDesiredVector.getAngle()-motors[motor_num].getMotorAngl())*DEG_TO_RAD) - rotation_rate;

	//TODO matrix multiplication
}

boolean MotorControl::isMotorForward(int motorNum){
	//TODO	
}

void MotorControl::setOverallDesiredVector(float magnitude, float angl){
	this->overallDesiredVector.setMagnitude(magnitude);
	this->overallDesiredVector.setAngle(angl);
}

float MotorControl::getNewAimFromFeedback(float desiredSpeed, float actualSpeed){
	return desiredSpeed + ((desiredSpeed - actualSpeed) * mtrconst);
}

int MotorControl::getPWMFromSpeed(float speed){
	return speedpwmstruct.getPWMFromSpeed(speed);
}

void setMotorPWM(int motorNum, int motorPWM, boolean FOR){
	this->motors[motorNum].setPWM(motorPWM, FOR);
}

void MotorControl::updateMotors(float magnitude, float angl, float rotation_rate){

	setOverallDesiredVector(magnitude,angl);
	int motorPWMs[3];

	for (int i = 0; i < 3; i++){
		motorPWMs[i] = getPWMFromSpeed(getNewAimFromFeedback(getDesiredIndividualSpeed(i, rotation_rate),getIndividualSpeed(i)));
	}

	for (int j = 0; j < 3; j++){
		setMotorPWMs(j,motorPWMs[j],isMotorForward(j));
	}
}

