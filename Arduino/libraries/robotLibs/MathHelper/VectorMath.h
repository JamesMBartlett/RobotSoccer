/*
 * VectorMath.h
 *
 *  Created on: 02/01/2014
 *      Author: james
 */

#ifndef VECTORMATH_H_
#define VECTORMATH_H_
#include "ComponentsFromVector.h"
#include "Vector.h"


class VectorMath {
public:
	VectorMath();
	virtual ~VectorMath();
	ComponentsFromVector getComponentVector(Vector vector);
	Vector getVectorFromComponents(float xmagnitude, float ymagnitude);
};

#endif /* VECTORMATH_H_ */
