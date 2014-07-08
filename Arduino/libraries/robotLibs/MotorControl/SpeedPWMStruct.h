/*
 * SpeedtoPWM.h
 *
 *  Created on: 03/01/2014
 *      Author: james
 */

#ifndef SPEEDTOPWM_H_
#define SPEEDTOPWM_H_

static const int testPWMLENGTH = 16;

class SpeedPWMStruct {
public:
	SpeedPWMStruct();
	virtual ~SpeedPWMStruct();
	int getLength(void);
	void setSpeedForPWM(float speed, int PWM);
	int getPWMFromSpeed(float speed);
	int interpolatePWM(int left, int right, float speed);
private:
	int PWMArray[testPWMLENGTH];
	float SpeedArray[testPWMLENGTH];
};

#endif /* SPEEDTOPWM_H_ */
