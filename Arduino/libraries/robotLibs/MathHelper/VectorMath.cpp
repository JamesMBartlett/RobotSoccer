/*
 * VectorMath.cpp
 *
 *  Created on: 02/01/2014
 *      Author: james
 */

#include "VectorMath.h"
#include <Arduino.h>

VectorMath::VectorMath() {


}

VectorMath::~VectorMath() {

}

ComponentsFromVector VectorMath::getComponentVector(Vector vector){
	return ComponentsFromVector(vector);
}



Vector VectorMath::getVectorFromComponents(float xmagnitude, float ymagnitude){
	float vect_mag = sqrt((xmagnitude * xmagnitude) + (ymagnitude * ymagnitude));
	float vect_angl = atan((xmagnitude / ymagnitude) * DEG_TO_RAD);

	return Vector(vect_mag, vect_angl);
}
