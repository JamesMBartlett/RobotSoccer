/*
 * Calibration.h
 *
 *  Created on: 03/01/2014
 *      Author: james
 */

#ifndef CALIBRATION_H_
#define CALIBRATION_H_
#include "MotorControl/Motor.h"
#include "MotorControl/Encoder.h"
#include "MotorControl/MotorControl.h"
#include "MotorControl/SpeedPWMStruct.h"

class Calibration {
public:
	Calibration(MotorControl parMotorControl);
	SpeedPWMStruct getSpeedPWMStruct();
	virtual ~Calibration();
	void calibrateMotors();
	void calibrate();
private:
	MotorControl motorControl;
	SpeedPWMStruct speedPWMStruct;
	int testPWMS[testPWMLENGTH];
};

#endif /* CALIBRATION_H_ */
