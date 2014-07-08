/*
 * Encoder.cpp
 *
 *  Created on: 02/01/2014
 *      Author: james
 */

#include <Arduino.h>
#include "Encoder.h"

Encoder::Encoder(){
}

Encoder::Encoder(int encoder_pin1, int encoder_pin2) {
	pinA = encoder_pin1;
	pinB = encoder_pin2;
	encoderDistance = 0;
	currentTime = millis();
	timeLastAccessed = millis();
	timeBetweenLastTwoAccesses = 0;
}

Encoder::~Encoder() {

}

void Encoder::interrupt(void){
	encoderDistance += (digitalRead(pinB) * 2) - 1;
}

void Encoder::beginInterrupt(){
	attachInterrupt(pinA, &Encoder::interrupt, FALLING);
}

void Encoder::endInterrupt(){
	detachInterrupt(pinA);
}

signed int Encoder::getEncoderDistance(void){
	signed int encoderdist = encoderDistance;
	currentTime = millis();
	timeBetweenLastTwoAccesses = currentTime - timeLastAccessed;
	timeLastAccessed = currentTime;

	return encoderDistance;

}

unsigned long Encoder::getTimeBetween(void){
	return timeBetweenLastTwoAccesses;
}

