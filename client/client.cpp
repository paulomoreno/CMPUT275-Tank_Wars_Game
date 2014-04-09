#include <Arduino.h>
#include <mem_syms.h>


// Arduino analog input pin for the horizontal on the joystick.
const uint8_t joy_pin_x = 0;
// Arduino analog input pin for the vertical on the joystick.
const uint8_t joy_pin_y = 1;
// Digital pin for the joystick button on the Arduino.
const uint8_t joy_pin_button = 4;

int OFFSET = 60; 
int16_t joy_center_x = 512;
int16_t joy_center_y = 512;
int vertical, horizontal;

void setup() {
  Serial.begin(9600);
  //initialize the joystick
  pinMode(4, INPUT);
  digitalWrite(4,HIGH);
  //Set center point for joystick
  joy_center_x = analogRead(joy_pin_x);
  joy_center_y = analogRead(joy_pin_y);
  Serial.println("Starting...");
  Serial.flush();    // There can be nasty leftover bits.

}

void loop(){
 
  while(digitalRead(4)!=LOW){
   
    vertical = analogRead(joy_pin_y);
    horizontal = analogRead(joy_pin_x);
    //If joystick is behon offset in y postition write to the serial port
    if(horizontal > joy_center_x+OFFSET){
      Serial.print("R");
    }
    else if(horizontal < joy_center_x-OFFSET){
      Serial.print("L");
    }
       
    else if(vertical > joy_center_y+OFFSET){
      Serial.print("D");
    }
    else if(vertical < joy_center_y-OFFSET){
      Serial.print("U");
    }
    delay(100);    
  }
    
    Serial.print("F");
    delay(100);
  
}
