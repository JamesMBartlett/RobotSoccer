/*
 * Vector.h
 *
 *  Created on: 02/01/2014
 *      Author: james
 */

#ifndef VECTOR_H_
#define VECTOR_H_

class Vector {
public:
	Vector(float magnitude, float angl);
	Vector();
	void setMagnitude(float magnitude);
	void setAngle(float angl);
	virtual ~Vector();
	float getMagnitude();
	float getAngle();
private:
	float mag;
	float ang;
};

#endif /* VECTOR_H_ */
