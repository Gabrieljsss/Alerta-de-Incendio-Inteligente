byte leitura;
int portaGas = 0;
int leituraGas = 0;
float gasMapeado = 0;
void setup() {

  Serial.begin(9600);
  pinMode(LED_BUILTIN , OUTPUT);
  pinMode(portaGas, INPUT);
  digitalWrite(LED_BUILTIN, LOW);
 

}
void loop() {
  if (Serial.available() >= 0) {
       digitalWrite(LED_BUILTIN, HIGH);
       delay(500);
       digitalWrite(LED_BUILTIN, LOW);

       leituraGas = analogRead(portaGas);
       Serial.println(leituraGas);
       delay(500);    
  }
}
