/*
 * Motor.h
 *
 *  Created on: 02/01/2014
 *      Author: james
 */

#ifndef MOTOR_H_
#define MOTOR_H_
#include "Arduino.h"
#define FORWARD true
#define REVERSE false


class Motor {
public:
	Motor(int motor_for_pin, int motor_rev_pin, int pwm_pin, int motor_angl);
	Motor();
	void setPWM(int pwm, boolean FOR);
	void off(void);
	int getMotorAngl(void);
	virtual ~Motor();
private:
	int pin_for;
	int pin_rev;
	int pin_pwm;
	int motorAngl;

};

#endif /* MOTOR_H_ */


