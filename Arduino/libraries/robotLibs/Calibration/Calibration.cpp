/*
 * Calibration.cpp
 *
 *  Created on: 03/01/2014
 *      Author: james
 */

#include "Calibration.h"



Calibration::Calibration(MotorControl parMotorControl) {
	this->speedPWMStruct = SpeedPWMStruct();
	this->motorControl = parMotorControl;
	for (int j = 0; j < testPWMLENGTH; j++){
		this->testPWMS[j] = (255/testPWMLENGTH) * (j+1);
	}
}

Calibration::~Calibration() {
}

void Calibration::calibrateMotors(){
	for (int i = 0; i < 3; i++){
		for (int j = 0; j < testPWMLENGTH; i++){
			this->motorControl.motors[i].setPWM(this->testPWMS[j], true);
			delay(2);
			this->motorControl.encoders[i].beginInterrupt();
			delay(1);
			this->speedPWMStruct.setSpeedForPWM(this->motorControl.getIndividualSpeed(i), this->testPWMS[j]);
			this->motorControl.encoders[i].endInterrupt();
		}


	}
}


SpeedPWMStruct Calibration::getSpeedPWMStruct(){
	return this->speedPWMStruct;
}


void Calibration::calibrate(){
	calibrateMotors();
}