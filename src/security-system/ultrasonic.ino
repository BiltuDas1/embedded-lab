const int TRIG_PIN = D5;
const int ECHO_PIN = D6;
const int RELAY_PIN = D1;
const int ALERT_DISTANCE = 50; // In cm

void setup() {
  Serial.begin(115200);
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  pinMode(RELAY_PIN, OUTPUT);
  
  // HIGH to OFF
  digitalWrite(RELAY_PIN, HIGH); 
}

void loop() {
  long duration;
  int distance;

  // Trigger Sensor
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  duration = pulseIn(ECHO_PIN, HIGH);
  distance = duration * 0.034 / 2;

  // If distance is less than threshold, trigger relay
  if (distance > 0 && distance <= ALERT_DISTANCE) {
    digitalWrite(RELAY_PIN, LOW); // Turn on Relay
  } else {
    digitalWrite(RELAY_PIN, HIGH); // Turn off Relay
  }

  delay(500); 
}