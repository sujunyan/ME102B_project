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
#define COMMAND_HEADER 0xff
const float CORRECTION = (1.0367f); // correction for the accuracy, according to the measurement.
const float DIAMETER = (12.2f) ;
#define M_PI  3.14159265358979323846
const float DEGREE_PER_TURN =  (M_PI * DIAMETER / 360 ) * CORRECTION; //
const int RPM = 120;
const int MICRO_STEP = 16;
/****
 * LegoBuilder methods
 * */

enum command_id_t {
   MOVE_XYZ = 0,
   ROTATE_XYZ = 1,
   PUSH_AND_GRIBPPER_ACTION = 2,
};



LegoBuilder::LegoBuilder():_stepper_x1(MOTOR_STEPS,DIR_X1,STEP_X1), _stepper_x2(MOTOR_STEPS,DIR_X2,STEP_X2),
                            _stepper_y(MOTOR_STEPS,DIR_Y,STEP_Y),_now_x(0),_now_y(0),_now_z(0){
    // Set target motor RPM to 60RPM and microstepping to 1 (full step mode)
    _stepper_x1.begin(RPM, MICRO_STEP);
    _stepper_x2.begin(RPM, MICRO_STEP);
    _stepper_y.begin(RPM, MICRO_STEP);
    memset(&_command,0,sizeof(_command));
    //
    pinMode(_push_relay_pin,OUTPUT);
    pinMode(_gripper_relay_pin,OUTPUT);
    pinMode(_switch_y,INPUT);
    pinMode(_switch_x1,INPUT);
    pinMode(_switch_x2,INPUT);
}



void LegoBuilder::softwareSystem() {
    //Serial.print("Test Start\n");
    if(readCommand() == 0) // read successfully
      parseCommand();
    //Serial.print("Test End\n\n");
    delay(1000);
}

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
        case PUSH_AND_GRIBPPER_ACTION:{
            if(_command.len != 1){
                log_e("Invalid push and gripper command!");
            }
            switch (_command.data[0]) {
                case 1: {pushGripper();break;}
                case 2: {pullGripper();break;}
                case 3: {tightenGripper();break;}
                case 4: {releaseGripper();break;}
                default: {log_e("Invalid push and gripper command, wrong data\n");break;}
            }
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
    //log_e("Rotate  %d %d %d \n",x,y,z);
    _stepper_x1.startRotate(x);
    _stepper_x2.startRotate(-x);
    _stepper_y.startRotate(y);
    int flag1,flag2,flag3;
    while (true){ // try to run the stepper motor at the same time
        flag1 = _stepper_x1.nextAction();
        flag2 = _stepper_x2.nextAction();
        flag3 = _stepper_y.nextAction();
        if(!flag1 && !flag2 && !flag3)
            break;
    }
    log_e("Rotate  %d %d %d done\n",x,y,z);
}

void LegoBuilder::rotateToXYZ(float x, float y, float z) {
    //log_e("Rotate  %d %d %d \n",x,y,z);
    _stepper_x1.startRotate(x);
    _stepper_x2.startRotate(-x);
    _stepper_y.startRotate(y);
    int flag1,flag2,flag3;
    while (true){ // try to run the stepper motor at the same time
        flag1 = _stepper_x1.nextAction();
        flag2 = _stepper_x2.nextAction();
        flag3 = _stepper_y.nextAction();
        if(!flag1 && !flag2 && !flag3)
            break;
    }
    //log_e("Rotate  %d %d %d done\n",x,y,z);
}

void LegoBuilder::moveToXYZ(float x, float y, float z) {
    //log_e("Move to %f %f %f \n",x,y,z);

    rotateToXYZ( (x - _now_x)/DEGREE_PER_TURN ,( y - _now_y)/DEGREE_PER_TURN,0.0f);
    _now_x = x;
    _now_y = y;

    //log_e("Move to %f %f %f \n",x,y,z);
}

void LegoBuilder::calibrate(){
  //Serial.print("calibrate start\n");
  //Serial.printf("limit_swtich is %d\n",digitalRead(_switch_y));
    if(_is_calibrate)return;
    int y_direction = -2;
    int x_direction = -2;
    int flag_x1 = 0;
    int flag_x2 = 0;
    int flag_y = 0;
    while(true){
        if(digitalRead(_switch_x1))flag_x1=1;
        if(digitalRead(_switch_x2))flag_x2=1;
        if(flag_x1 && flag_x2) break;
        if(!flag_x1)_stepper_x1.rotate(x_direction);
        if(!flag_x2)_stepper_x2.rotate(-x_direction);
        delay(1);
    }

    _now_x =0;
    _now_z =0;
    moveToXYZ(100,0,0);
     while(true){
         Serial.printf("flag_y %d\n",flag_y);
        if(digitalRead(_switch_y))flag_y=1;
        if(flag_y) break;
        if(!flag_y)_stepper_y.rotate(y_direction);
        delay(1);
    }

    Serial.print("calibrate done\n");
    _is_calibrate = 1;
    _now_y =0;
}

void LegoBuilder::testRunSquare(){
    const int RUN_LEN = 50;
    const int DELAY_TIME = 100;
    moveToXYZ(0,0,0);
    delay(DELAY_TIME);
    moveToXYZ(RUN_LEN,0,0);
    delay(DELAY_TIME);
    moveToXYZ(RUN_LEN,RUN_LEN,0);
    delay(DELAY_TIME);
    moveToXYZ(0,RUN_LEN,0);
    delay(DELAY_TIME);
    moveToXYZ(0,0,0);
}


void LegoBuilder::pushGripper(){
    digitalWrite(_push_relay_pin,HIGH);
}
void LegoBuilder::pullGripper(){
    digitalWrite(_push_relay_pin,LOW);
}
void LegoBuilder::tightenGripper(){
    digitalWrite(_gripper_relay_pin,LOW);
}
void LegoBuilder::releaseGripper(){
    digitalWrite(_gripper_relay_pin,HIGH);
}
