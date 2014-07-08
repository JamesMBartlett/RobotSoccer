/*
 * SpeedtoPWM.cpp
 *
 *  Created on: 03/01/2014
 *      Author: james
 */

#include "SpeedPWMStruct.h"

SpeedPWMStruct::SpeedPWMStruct() {
}

SpeedPWMStruct::~SpeedPWMStruct() {
}

int SpeedPWMStruct::getLength(){
	return testPWMLENGTH;
}

void SpeedPWMStruct::setSpeedForPWM(float speed, int PWM){
	int k = PWM / (255 / testPWMLENGTH);
	this->PWMArray[k] = PWM;
	this->SpeedArray[k] = speed;
}

int SpeedPWMStruct::getPWMFromSpeed(float speed){
	int PWM = 0;
	int left = 0;
	int right = testPWMLENGTH;

	// BINARY Search loop
	for ( int i = 1; i < 11; i++){
		if (speed < SpeedArray[int(right/2)]){
			right = right/2;
		}
		else if(speed = SpeedArray[int(right/2)]){
			PWM = SpeedArray[int(right/2)];
			break;
		}
		else{
			left = right / 2;
		}
		if ( (right - left) == 1){
			PWM = this->interpolatePWM(left, right, speed);
			break;
		}	
	}
	return PWM;
}

int SpeedPWMStruct::interpolatePWM(int left, int right, float speed){
	return int(PWMArray[left] + ((PWMArray[right]-PWMArray[left])*((speed-SpeedArray[left])/(SpeedArray[right]-SpeedArray[left])))); // based on the interpolation formula y = y0 + (y1-y0)*(x-x0)/(x1-x0)
}
