#include <Arduino.h>
#include "LegoBuilder.h"
const int SWITH_PIN = 2;
const int FSR_PIN = 14;
LegoBuilder legoBuilder;
void setup() {
  pinMode(SWITH_PIN,INPUT);
  pinMode(FSR_PIN,INPUT);
  Serial.begin(115200);
}

int cnt = 0;
void loop() {
    int swith_val = digitalRead(SWITH_PIN);
    int FSR_val = analogRead(FSR_PIN);
   Serial.printf("swith %d FSR %d cnt %d\n",swith_val,FSR_val,cnt++);
   //legoBuilder.test();
   //legoBuilder.rotateToXYZ(360,360,0);
   delay(10);
}
