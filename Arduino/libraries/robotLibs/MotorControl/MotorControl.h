/*
 * MotorControl.h
 *
 *  Created on: 02/01/2014
 *      Author: james
 */

#ifndef MOTORCONTROL_H_
#define MOTORCONTROL_H_
#include "Arduino.h"
#include "MotorControl/Motor.h"
#include "MotorControl/Encoder.h"
#include "MathHelper/ComponentsFromVector.h"
#include "MathHelper/Vector.h"
#include "MotorControl/SpeedPWMStruct.h"
#include <gsl_math.h>

#define oneonroot3 0.5773502691896258
#define onethird 0.3333333333333333

class MotorControl {
public:
	MotorControl(Motor parMotors[], Encoder parEncoders[], SpeedPWMStruct speedpwmstruct);
	MotorControl();
	float getDesiredIndividualSpeed(int motor_num, float rotation_rate);
	void setOverallDesiredVector(float magnitude, float angl);
	float getNewAimFromFeedback(float desiredSpeed, float actualSpeed);
	int getPWMFromSpeed(float speed);
	void updateMotors();
	virtual ~MotorControl();
	void setMotorPWM(int motorNum, int, boolean FOR)
	static const int clicksperrev;
	static const int millispersec;
	Motor motors[3];
	Encoder encoders[3];
	float getIndividualSpeed(int encoder_num);
private:
	ComponentsFromVector motorSpeedComponents[3];
	Vector overallDesiredVector;
	SpeedPWMStruct speedpwmstruct;
	static const float mtrconst;
};

#endif /* MOTORCONTROL_H_ */
