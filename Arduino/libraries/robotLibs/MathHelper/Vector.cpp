/*
 * Vector.cpp
 *
 *  Created on: 02/01/2014
 *      Author: james
 */

#include "Vector.h"

Vector::Vector(float magnitude, float angl) {
	mag = magnitude;
	ang = angl;

}
Vector::Vector(){
}

Vector::~Vector() {
}

float Vector::getMagnitude(){
	return mag;
}
float Vector::getAngle(){
	return ang;
}

void Vector::setMagnitude(float magnitude){
	mag = magnitude;
}

void Vector::setAngle(float angl){
	ang = angl;
}