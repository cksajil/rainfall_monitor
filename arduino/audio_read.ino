void setup() {
  pinMode(WIO_MIC, INPUT);
  Serial.begin(2000000);
}

void loop() {
  int val = analogRead(WIO_MIC);
  Serial.println(val);
}