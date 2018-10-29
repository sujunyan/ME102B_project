#include <Arduino.h>
#include "LegoBuilder.h"

LegoBuilder legoBuilder;
void setup() {
  Serial.begin(9600);
    // Set target motor RPM to 60RPM and microstepping to 1 (full step mode)
}

int cnt = 0;
void loop() {
   Serial.printf("Hello World %d\n",cnt++);
   legoBuilder.test();
   delay(1000);
}
