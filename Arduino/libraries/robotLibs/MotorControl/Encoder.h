/*
 * Encoder.h
 *
 *  Created on: 02/01/2014
 *      Author: james
 */

#ifndef ENCODER_H_
#define ENCODER_H_

class Encoder {
public:
	Encoder(int encoder_pin1, int encoder_pin2);
	static void interrupt();
	signed int getEncoderDistance();
	unsigned long getTimeBetween();
	void beginInterrupt();
	void endInterrupt();
	virtual ~Encoder();
	Encoder();
private:
	int pinA;
	static int pinB;
	static signed int encoderDistance;
	unsigned long timeLastAccessed;
	unsigned long currentTime;
	unsigned long timeBetweenLastTwoAccesses;
};

#endif /* ENCODER_H_ */
