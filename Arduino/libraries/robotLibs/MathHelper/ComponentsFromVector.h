/*
 * ComponentVectors.h
 *
 *  Created on: 02/01/2014
 *      Author: james
 */

#ifndef COMPONENTVECTORS_H_
#define COMPONENTVECTORS_H_
#include "Vector.h"

class ComponentsFromVector {
public:
	ComponentsFromVector();
	ComponentsFromVector(Vector vect);
	virtual ~ComponentsFromVector();
	float getXMagnitude();
	float getYMagnitude();
private:
	float xmagnitude;
	float ymagnitude;
	char onecomponentflag;
};

#endif /* COMPONENTVECTORS_H_ */
