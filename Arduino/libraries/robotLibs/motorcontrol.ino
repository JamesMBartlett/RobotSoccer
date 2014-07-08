const int mtroffset[] = {60,180,300}; 
const float pi = 3.1415; 
float wheelspeed[3];
int wheel_speed_returnarray[2];

int interpolate(int desiredspeed, int returnarray[]){
  int half;
  int left = 0;
  int right = 11;
  boolean found = false;
  int negation = 0;
  int lowerspeed;
  int higherspeed;
  float speed_proportion;
  int pwm_output;
  int pwmarray[] = {35,55,75,95,115,135,155,175,195,215,235,255};
  float speedarray[] = {10, 30, 46, 58, 67,73, 78, 80, 82, 84, 86, 90};
  half = 0;
  left = 0;
  right = 11;
  found =false;
  if (desiredspeed < 0){
    desiredspeed *= -1;
    negation = 1;  
  }
  
  do{
      half = 0;
      if ((left+right)%2 != 0){
        half = (left + right + 1)/2;
      }
      else{
        half = (left + right) / 2;
      }
      if ((right - left) == 1){
         lowerspeed = left;
         higherspeed = right;
         found = true;
      }
      else{ 
        if (speedarray[half]>desiredspeed){
          right = half;
        }
        else{
          left = half;
        }
      }
    }while(!found);
   speed_proportion = (desiredspeed - speedarray[lowerspeed]) / (speedarray[higherspeed] - speedarray[lowerspeed]);
   pwm_output = (speed_proportion * 20) + pwmarray[lowerspeed];
   if (pwm_output > 255){
     pwm_output = 255;
   }
   else if (pwm_output < 0){
     pwm_output = 0;
   }
   returnarray[0] = pwm_output;
   returnarray[1] = negation;
   return returnarray;
}

int wheel_speed(unsigned long previoustime, int returnarray[]){
  int clicksper10sec;
  int clicksperrev = 304;
  unsigned long current_time = millis();
  int mtrencoderdistance = encoderdistance;
  int speed_last_time_step;
  int difference = int(current_time - previoustime);
  output += "\n Difference: ";
  output += difference;
  clicksper10sec = mtrencoderdistance * 10000/ difference;
  output += " \n Clicksper10sec: ";
  output += clicksper10sec; 
  speed_last_time_step = clicksper10sec / clicksperrev ;
  returnarray[0] = speed_last_time_step;
  returnarray[1] = int(current_time);
  return returnarray;
}

int motor_feedback_control(int previous_aim, float goal_speed_proportion, int prev_speed, int returnarray[]){
  float mtrconstant = 0.2;
  int new_set_point;
  if (previous_aim){
    new_set_point = (goal_speed_proportion *90.0) + (mtrconstant * float(previous_aim - prev_speed));
    previous_aim = goal_speed_proportion * 90;
  }
  else{
    new_set_point = goal_speed_proportion * 90.0;
    previous_aim = goal_speed_proportion * 90;
  }
  int pwm_negate[2];
  pwm_negate = interpolate(new_set_point, pwm_negate);
  int pwm_of_set_point = pwm_negate[0];
  int negation = pwm_negate[1];
  returnarray[0] = previous_aim;
  returnarray[1] = new_set_point;
  returnarray[2] = pwm_of_set_point;
  returnarray[3] = negation;
  return returnarray;
}

float* goal_wheel_proportions(float goal_heading, int goal_rotation, int velocityprop){
  float angl[3];
  float sinofangl[3];
  for (int i = 0; i<3;i++){
    angl[i] = goal_heading - mtroffset[i];
    angl[i] *= pi;
    angl[i] /= 180;
    sinofangl[i] = sin(angl[i]);
    wheelspeed[i] = (velocityprop * sinofangl[i])- goal_rotation;
  }
  return &(wheelspeed[0]);
}


//float sinofang(float angl){
//  byte sinarray[] =  {0,22,44,66,87,108,128,146,164,180,195,209,221,231,240,246,251,254,255};
//  float sine;
//  const int lensinarray = 19;
//  const float divisor = 90.0 / float(lensinarray - 1);
//  angl = angl - (360 * floor(angl / 360));
//  int negation = 1;
//  if (angl >= 180){
//    angl -= 180;
//    negation = -1;  
//  }
//  if (angl >= 90){
//    angl = 180 - angl;  
//  }
//  // at this point angl is >= 0 and <= 90
//  int index = int(angl / divisor);
//  if (index == lensinarray - 1){
//    sine = 1;  
//  }
//  else{
//    float leftsine = float(sinarray[index]) / 255.0;
//    float rightsine = float(sinarray[index+1]) / 255.0;
//    sine = leftsine + ((angl - (index * divisor)) / divisor) * (rightsine - leftsine);
//  }
//  return sine * negation;
//}
