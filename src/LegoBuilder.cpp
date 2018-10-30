#include "LegoBuilder.h"
#include <cstring>
/******
 * Debug functions
 * ******/
#define log_e Serial.printf

/// The configs
#define DIR_X1 23
#define STEP_X1 22
#define DIR_X2 21
#define STEP_X2 20
#define DIR_Y 19
#define STEP_Y 18
#define MOTOR_STEPS 200
const float DIAMETER = (1.0f);
#define M_PI 3.14159265358979323846
const float DEGREE_PER_TURN =  M_PI * DIAMETER * 360; //
/****
 * LegoBuilder methods
 * */

enum command_id_t {
   MOVE_XYZ = 0,
   ROTATE_XYZ = 1
};

void LegoBuilder::moveToXYZ(float x, float y, float z) {
    log_e("Move to %f %f %f \n",x,y,z);
    _stepper_x1.startRotate(x/DEGREE_PER_TURN);
    _stepper_x2.startRotate(x/DEGREE_PER_TURN);
    _stepper_y.startRotate(y/DEGREE_PER_TURN);
    while (true){ // try to run the stepper motor at the same time
        int flag1 = _stepper_x1.nextAction();
        int flag2 = _stepper_x2.nextAction();
        int flag3 = _stepper_y.nextAction();
        if(!flag1 && !flag2 && !flag3)
            break;
    }
    log_e("Move to %f %f %f done\n",x,y,z);
}

LegoBuilder::LegoBuilder():_stepper_x1(MOTOR_STEPS,DIR_X1,STEP_X1), _stepper_x2(MOTOR_STEPS,DIR_X2,STEP_X2),
                            _stepper_y(MOTOR_STEPS,DIR_Y,STEP_Y){
    // Set target motor RPM to 60RPM and microstepping to 1 (full step mode)
    _stepper_x1.begin(60, 1);
    _stepper_x2.begin(60, 1);
    _stepper_y.begin(60, 1);
    memset(&_command,0,sizeof(_command));
}


void LegoBuilder::test() {
    Serial.print("Test Start\n");
    if(readCommand() == 0) // read successfully
      parseCommand();
    Serial.print("Test End\n\n");
}
#define COMMAND_HEADER 0xff

int LegoBuilder::readCommand() {
    Serial.print("reading command\n");
    if(Serial.available() > 0){
        uint8_t theByte = Serial.read();
        //uint8_t theByte = 0;
        if(theByte != COMMAND_HEADER){
            log_e("Not valid command header, recieved 0x%x\n",theByte);
            return -1;
        }else{ // if a valid command
           _command.command_id = Serial.read();
           _command.len = Serial.read();
           int cnt = 0;
           while( cnt < _command.len){
              _command.data[cnt] = Serial.read();
              cnt++;
           }
        }
    } else{
        log_e("No byte available");
        return -2;
    }
    log_e("Read Command successfully\n");
    //print_command();
    return 0;
}

/// The protocol:
/// Header          | command_id    | len       | data
///  1 byte(255)    | 1 byte        | 1 byte   | data
int LegoBuilder::parseCommand() {
    switch (_command.command_id){
        case MOVE_XYZ:{
            if(_command.len != 3 * sizeof(float)){
                log_e("Invalid move command, sizeof float is %d\n",sizeof(float));
            }
            float tmp[3];
            memcpy(tmp,_command.data,sizeof(tmp));
            moveToXYZ(tmp[0],tmp[1],tmp[2]);
            break;
        }
        case ROTATE_XYZ:{
            if(_command.len != 3 * sizeof(int)){
                log_e("Invalid move command, sizeof float is %d\n",sizeof(float));
            }
            int tmp[3];
            memcpy(tmp,_command.data,sizeof(tmp));
            rotateToXYZ(tmp[0],tmp[1],tmp[2]);
            break;
        }
        default:{
            log_e("In parseCommand: Not a valid command_id");
            return -1;
        }
    }
    return 0;
}

void LegoBuilder::print_command() {
    for (int i = 0; i < COMMAND_LEN; ++i) {
        log_e("0x%x,",_command.data[i]);
    }
    log_e("\n");

}

void LegoBuilder::rotateToXYZ(int x, int y, int z) {
    log_e("Rotate  %d %d %d \n",x,y,z);
    _stepper_x1.startRotate(x);
    _stepper_x2.startRotate(x);
    _stepper_y.startRotate(y);
    while (true){ // try to run the stepper motor at the same time
        int flag1 = _stepper_x1.nextAction();
        int flag2 = _stepper_x2.nextAction();
        int flag3 = _stepper_y.nextAction();
        if(!flag1 && !flag2 && !flag3)
            break;
    }
    log_e("Rotate  %d %d %d \n",x,y,z);
}
