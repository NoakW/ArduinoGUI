#include <Servo.h>

Servo myServo;

void setup() {
  pinMode(5, OUTPUT);
  pinMode(6, OUTPUT);
  Serial.begin(9600);
  pinMode(2,OUTPUT);
  pinMode(3,OUTPUT);
  Serial.println("Send 'HIGH' to turn on LED, 'LOW' to turn it off");
  myServo.attach(2);
}

String command;
void loop() {
  if (Serial.available() > 0) {
    
    command = Serial.readStringUntil('\n');

    command.trim();
    if (command == "HIGH_BLUE") {
      digitalWrite(5, HIGH);
    }
    else if (command == "LOW_BLUE") {
      digitalWrite(5, LOW);
    }
    else if (command == "HIGH_RED") {
      digitalWrite(6, HIGH);
    }
    else if (command == "LOW_RED") {
      digitalWrite(6, LOW);
    }
    else if (command == "MOTOR_ON") {
      myServo.write(180);
    }
    else if (command == "MOTOR_OFF"){
      myServo.write(0);
    }
    else if (command == "PARTY"){
      digitalWrite(6, HIGH);
      digitalWrite(5, LOW);
      myServo.write(0);
      delay(100);
      digitalWrite(5, HIGH);
      digitalWrite(6, LOW);
      myServo.write(50);
      delay(100);
      digitalWrite(6, HIGH);
      digitalWrite(5, LOW);
      myServo.write(0);
      delay(100);
      digitalWrite(5, HIGH);
      digitalWrite(6, LOW);
      myServo.write(50);
      delay(100);
      digitalWrite(6, HIGH);
      digitalWrite(5, LOW);
      myServo.write(0);
      delay(100);
      digitalWrite(5, HIGH);
      digitalWrite(6, LOW);
      myServo.write(50);
      delay(100);
      digitalWrite(6, HIGH);
      digitalWrite(5, LOW);
      myServo.write(0);
      delay(100);
      digitalWrite(5, HIGH);
      digitalWrite(6, LOW);
      myServo.write(50);
      delay(100);
      digitalWrite(6, HIGH);
      digitalWrite(5, LOW);
      myServo.write(0);
      delay(100);
      digitalWrite(5, HIGH);
      digitalWrite(6, LOW);
      myServo.write(50);
      delay(100);
    }
    else {
      Serial.println("Unknown Command");
    }
  }
}
