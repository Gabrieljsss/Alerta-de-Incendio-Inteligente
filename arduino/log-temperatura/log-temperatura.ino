#include <Thermistor.h>

Thermistor temp(1);

void setup() {
  Serial.begin(9600);
}

void loop() {
  int temperature = temp.getTemp();
  Serial.println(temperature);
  delay(1000);
}

 
