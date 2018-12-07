#include <Arduino.h>
#include "LegoBuilder.h"

LegoBuilder legoBuilder;
void setup() {
  Serial.begin(115200);
  legoBuilder.calibrate();
  legoBuilder.moveToOrigin();
}

int flag = 0;
int cnt =0;
void loop() {
     //legoBuilder.testRunSquare();
   legoBuilder.softwareSystem();


   //Serial.printf("flag is %d \n",flag);
   //legoBuilder.rotateToXYZ(360,360,360);
   //delay(100);
}
