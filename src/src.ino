#include <Arduino.h>
#include "LegoBuilder.h"
const int SWITH_PIN = 3;
const int FSR_PIN = 14;
const int OUT_PIN = 5;
LegoBuilder legoBuilder;
void setup() {
  pinMode(SWITH_PIN,INPUT);
  pinMode(FSR_PIN,INPUT);
  pinMode(OUT_PIN,OUTPUT);
  Serial.begin(115200);
}
const int ROTATION_DEGREE = 90;
int cnt = 0;
int flag =0;
const float TEST_LEN = 50;
const int DELAY_TIME = 100;
void loop() {
    int swith_val = digitalRead(SWITH_PIN);
    int FSR_val = analogRead(FSR_PIN);
   //Serial.printf("swith %d FSR %d cnt %d\n",swith_val,FSR_val,cnt++);
   //legoBuilder.calibrate();
   //Serial.printf("flag is %d \n",flag);
   legoBuilder.test();
}
