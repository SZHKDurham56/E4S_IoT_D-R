#include "Arduino.h"
#include "MPU6050.h"
#include "Wire.h"
#include "I2Cdev.h"

int16_t mpu6050Ax, mpu6050Ay, mpu6050Az;
int16_t mpu6050Gx, mpu6050Gy, mpu6050Gz;

MPU6050 mpu6050;

const int timeout=10000;
char menuOption=0;
long time0;

void setup() {
  Serial.begin(9600);
  while(!Serial);
  Serial.println("Start");

  Wire.begin();
  mpu6050.initialize();
  menuOption=menu();
}

void loop() {
  if (menuOption=='1'){
    mpu6050.getMotion6(&mpu6050Ax, &mpu6050Ay, &mpu6050Az, &mpu6050Gx, &mpu6050Gy, &mpu6050Gz);
    Serial.print(mpu6050Ax); Serial.print("\t");
    Serial.print(mpu6050Ay); Serial.print("\t");
    Serial.print(mpu6050Az); Serial.print("\t");
    Serial.print(mpu6050Gx); Serial.print("\t");
    Serial.print(mpu6050Gy); Serial.print("\t");
    Serial.println(mpu6050Gz); 
    delay(100);
    }

    if (millis()-time0>timeout){
      menuOption=menu();
    }
}

char menu(){
  Serial.println(F("Press 1 and enter when testing is ready to begin\n"));
  while (!Serial.available());
  while (Serial.available()){
    char c=Serial.read();
    if (isAlphaNumeric(c)){
      if (c=='1'){
        Serial.println(F("Now testing the Accelerometer and Gyro functions of the MPU6050 sensor"));
      }
      else {
        Serial.println(F("Input not recognised"));
        return 0;
      }
      time0=millis();
      return c;
    }
  }
}
