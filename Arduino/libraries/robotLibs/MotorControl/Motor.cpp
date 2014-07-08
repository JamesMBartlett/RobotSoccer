/*
 * Motor.cpp
 *
 *  Created on: 02/01/2014
 *      Author: james
 */
#include "Motor.h"


Motor::~Motor() {
}
Motor::Motor(){
}
Motor::Motor(int motor_for_pin, int motor_rev_pin, int pwm_pin, int motor_angl){
	pin_for = motor_for_pin;
	pin_rev = motor_rev_pin;
	pin_pwm = pwm_pin;
	motorAngl = motor_angl;

	pinMode(pin_for, OUTPUT);
	pinMode(pin_rev, OUTPUT);
}

void Motor::setPWM(int pwm, boolean FOR){
	if(FOR){
		digitalWrite(pin_for, HIGH);
		digitalWrite(pin_rev, LOW);
	}else{
		digitalWrite(pin_for, LOW);
		digitalWrite(pin_rev, HIGH);
	}
	analogWrite(pin_pwm, pwm);
}

void Motor:: off(void){
	digitalWrite(pin_for, LOW);
	digitalWrite(pin_rev, LOW);
}

int Motor::getMotorAngl(void){
	return motorAngl;
}
