#include <Thermistor.h>


// the setup function runs once when you press reset or power the board
byte leitura;
int porta = 5;
int portaGas = 0;
int leituraGas = 0;
float gasMapeado = 0;
int temperature = -999;
Thermistor temp(1);


void setup() {

  Serial.begin(9600);
  pinMode(LED_BUILTIN , OUTPUT);
  pinMode(portaGas, INPUT);
  digitalWrite(LED_BUILTIN, LOW);
 

}

// the loop function runs over and over again forever
void loop() {
   
   if (Serial.available() >= 0) {
     leitura = Serial.read();
     if (leitura == 'H') {
       digitalWrite(porta, HIGH);
       digitalWrite(LED_BUILTIN, HIGH);
       delay(1000);
       digitalWrite(LED_BUILTIN, LOW); 
       temperature = temp.getTemp();
       Serial.println(temperature);
       delay(1000);
     }
     else if(leitura == 'G') {
       digitalWrite(porta, HIGH);
       digitalWrite(LED_BUILTIN, HIGH);
       delay(1000);
       digitalWrite(LED_BUILTIN, LOW);

       leituraGas = analogRead(portaGas);
       Serial.println(leituraGas);
       delay(1000);
     }
   }
   
}
