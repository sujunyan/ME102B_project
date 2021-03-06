#ifndef _LEGO_BUILDER_H_
#define _LEGO_BUILDER_H_

#include <A4988.h>
#include <cstdlib>
#include <cstdint>
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
    void calibrate();
    void test();
private:
    float _now_x,_now_y,_now_z;
    int _switch_x1 = 3;
    int is_calibrate = 0;
    StepMoter _stepper_x1,_stepper_x2,_stepper_y;
    command_t _command;
    int readCommand();
    int parseCommand();
    void print_command();

};
#endif
