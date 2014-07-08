/*
 * ComponentVectors.cpp
 *
 *  Created on: 02/01/2014
 *      Author: james
 */

#include <ComponentsFromVector.h>
#include <Arduino.h>

ComponentsFromVector::ComponentsFromVector(){
}

ComponentsFromVector::ComponentsFromVector(Vector vect) {
	float angl = vect.getAngle();
	float mag = vect.getMagnitude();
	boolean xnegation = false;
	boolean ynegation = false;

	if(angl<180){
		xnegation = false;
	}else if(angl > 180){
		xnegation = true;
	}
	if((angl + 90) < 180){
		ynegation = false;
	}else if((angl+90 > 180)){
		ynegation = true;
	}
	float local_angl = 90 - (int(angl) % 90);
	if(local_angl == 0){
		for(int i = 0; i < 4; i++){
			if(angl == (i*90)){
				if(i == 0 || i == 2){
					ymagnitude = mag*(i*((-1)/2)); //passes positive magnitude if i is 0 and negative if i is 2
					onecomponentflag = 2; // 2 means there is only a y component
				}else
				{
					xmagnitude = mag*((i-1)*((-1)/2)); // passes positive magnitude if i is 1 and negative if i is 3
					onecomponentflag = 1; // 1 means there is only an x component
				}
			}
		}
	}else{
		onecomponentflag = 0; // 0 means there are both components
		xmagnitude = mag * cos(local_angl * DEG_TO_RAD)  * xnegation;
		ymagnitude = mag * sin(local_angl * DEG_TO_RAD) * ynegation;
	}
}

ComponentsFromVector::~ComponentsFromVector() {
}

float ComponentsFromVector::getXMagnitude(void){
	if(onecomponentflag != 2){ // meaning there is either both magnitudes or only an x
		return xmagnitude;
	}else{
		return 0;
	}
}
float ComponentsFromVector::getYMagnitude(void){
	if(onecomponentflag != 1){ // meaning there is either both magnitudes or only a y
		return ymagnitude;
	}else{
		return 0;
	}
}
