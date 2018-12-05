#ifndef _LEGO_BUILDER_H_
#define _LEGO_BUILDER_H_

#include <A4988.h>
#include <cstdlib>
#include <cstdint>
#include <Servo.h>
#define StepMoter A4988
#define COMMAND_LEN 50

typedef struct command_t{
   uint8_t command_id;
   uint8_t len;
   uint8_t data[COMMAND_LEN];
}command_t;

class LegoBuilder{
public:
    LegoBuilder();
    void moveToXYZ(float x,float y,float z);
    void rotateToXYZ(int x,int y,int z);
    void rotateToXYZ(float x,float y,float z);
    void moveToOrigin();
    void calibrate();
    void softwareSystem();
    void testRunSquare();
    void test();
private:
    float _now_x,_now_y,_now_z;
    int _switch_x1 = 2;int _switch_x2 = 3;int _switch_y = 4;
    int _is_calibrate = 0;
    StepMoter _stepper_x1,_stepper_x2,_stepper_y;
    command_t _command;
    int _gripper_relay_pin = 5;
    int _push_relay_pin = 17;
    Servo rotate_servo;
    int _servo_pin = 6;
    int readCommand();
    int parseCommand();
    void print_command();
    //
    void pushGripper();
    void pullGripper();
    void tightenGripper();
    void releaseGripper();
    void pickLego();
    void placeLego();


};
#endif
