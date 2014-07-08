#include <motorcontrol.ino>
#include <Arduino.h>


#define mtr3encoder 45


const int motorpwm[] = {4,5,8};
//array of pin numbers for the first input for the motors
const int motorfor[] = {22,26,51};
//array of pin numbers for the second input for the motors
const int motorrev[] = {24,28,53};

int heading = 60;
volatile int encoderdistance;
int encoder_distance;
unsigned long prev_time;
unsigned long time;
float mtrgoalprop[3];
String output;
int mtr3encoder2 = 44;
int loopcount = 0;
int commatch;
int timerinterruptfreq = 2000;
int prescaler = 64;
byte portl;
byte prevencoderstate = 00000000;
byte mask1 = 00001000;
byte mask2 = 00000100;
int mtrencoderdistance[3];
unsigned long last_prev_time;
unsigned long newprevioustime;
int mtr3encoderdistance;
int clicksper10sec;
float speed_last_time_step;
int clicksperrev = 304;
int speed3;
int previous_aim;
int new_set_point;
float mtrconstant = 0.5;
int pwm_of_set_point;
int half;
int left = 0;
int right = 12;
int lowerspeed;
int higherspeed;
boolean found = false;
int pwmarray[] = {35,55,75,95,115,135,155,175,195,215,235,255};
float speedarray[] = {10, 30, 46, 58, 67,73, 78, 80, 82, 84, 86, 90};
float pwm_output;
float speed_percent;
int pwmarrayind;
unsigned long previous_time;
int* aims_sets_pwms;
int negation;
int* speed_prev_time;

void setup(){
  loopcount = 0;
  pinMode(38,OUTPUT);
  pinMode(40,OUTPUT);
  digitalWrite(40, HIGH);
  pinMode(42,INPUT);
  for (int i=0; i<4;i++){
    pinMode(motorfor[i],OUTPUT);
    pinMode(motorrev[i],OUTPUT);
  }
  pinMode(mtr3encoder2,INPUT);
  pinMode(20, INPUT);
  mtrgoalprop[2] = 0.5;
  Serial.begin(9600);
  digitalWrite(motorfor[2], HIGH);
  digitalWrite(motorrev[2], LOW);
  analogWrite(motorpwm[2], mtrgoalprop[2] * 255);
  attachInterrupt(3,encoder3funct,FALLING);
}


void encoder3funct(){
  encoderdistance += digitalRead(mtr3encoder2) * 2 - 1;
}

void loop(){
  if (loopcount == 100){
    Serial.begin(9600);
    digitalWrite(motorfor[2], LOW);
    digitalWrite(motorrev[2], LOW);
    analogWrite(motorpwm[2], 0);
    Serial.println(output);
    Serial.end(); 

  }
  else{
    delay(75);
    float* wheelvelos = goal_wheel_proportions(heading, 0, 1);
    for (int i = 0; i < 3; i++){
      mtrgoalprop[i] = wheelvelos[i];
      output += " \n ";
      output += " Mtr: " ;
      output += int(i);
      output += " Goal proportion: ";
      output += int(mtrgoalprop[i]*1000);  
    }
    if(previous_time){
      speed_prev_time = wheel_speed(previous_time);
    }
    else{
      speed_prev_time = wheel_speed(0);
    }
    output += " Speed_prev_time[1]: ";
    output += speed_prev_time[1];
    output += " Speed_prev_time[1]: ";
    output += speed_prev_time[1];
    speed3 = speed_prev_time[0];
    previous_time = speed_prev_time[1];
    if (previous_aim){
      aims_sets_pwms = motor_feedback_control(previous_aim,mtrgoalprop[2],speed3);
    }
    else{
      aims_sets_pwms = motor_feedback_control(false, mtrgoalprop[2], speed3);
    }
    previous_aim = aims_sets_pwms[0];
    new_set_point = aims_sets_pwms[1];
    pwm_of_set_point = aims_sets_pwms[2];
    negation = aims_sets_pwms[3];
    
    if(negation){
      digitalWrite(motorfor[2], LOW);
      digitalWrite(motorrev[2], HIGH);  
    }
    else{
      digitalWrite(motorfor[2], HIGH);
      digitalWrite(motorrev[2], LOW);  
    }
    analogWrite(motorpwm[2],pwm_of_set_point);
    
    
    output += " Speed: ";
    output += speed3;  
    output += " New Set Point: ";
    output += new_set_point;
    output += "\n";
    output += " PWM OUTPUT: ";
    output += pwm_of_set_point;
    output += "\n\n\n\n";
    loopcount += 1;
  }
}


