#include <Arduino.h>
#include <mem_syms.h>


// Arduino analog input pin zero for the joystick.
const uint8_t joy_pin_x = 0;
// Arduino analog input pin 1 for vertical on the joystick.
const uint8_t joy_pin_y = 1;
// Digital pin for the joystick button on the Arduino.
const uint8_t joy_pin_button = 4;
//Button Pin
const int button_pin = 3;

int buttonState = 0;

//Min value for joystick movement to be detected
int OFFSET = 60; 
//Default Joycstick positions
int16_t joy_center_x = 512;
int16_t joy_center_y = 512;
int vertical, horizontal;

void setup() {
  Serial.begin(9600);
  //initialize the joystick
  pinMode(4, INPUT);
  digitalWrite(4,HIGH);
  //buttonPin setup
  pinMode(button_pin, INPUT);
  digitalWrite(button_pin,HIGH);
  //Set center point for joystick
  joy_center_x = analogRead(joy_pin_x);
  joy_center_y = analogRead(joy_pin_y);
  Serial.println("Starting...");
  Serial.flush();    // There can be nasty leftover bits.
  

}

void loop(){
  //Setup joystick
  while(digitalRead(4)!=LOW){
    vertical = analogRead(joy_pin_y);
    horizontal = analogRead(joy_pin_x);
    //If joystick is beyond offset in y postition write to the serial port
    if(horizontal > joy_center_x+OFFSET){
      Serial.print("R"); // Send R character for right movement
    }
    else if(horizontal < joy_center_x-OFFSET){
      Serial.print("L"); // Send L for left movement
    }
    else if(vertical > joy_center_y+OFFSET){
      Serial.print("D"); // Send D for down movement
    }
    else if(vertical < joy_center_y-OFFSET){
      Serial.print("U"); // Send U for up movement
    }
    //Alternate Firing Button
    else if(digitalRead(button_pin) == LOW){
      Serial.print('F');
      delay(200);
    }

    else Serial.print(' '); // If no commands to be sent send filler
    delay(25); // Small delay
  }
 
  Serial.print("F"); // If the joystick was clicked send f for fire
  delay(250); // Longer delay to make sure no accidental double clicks
  
}
