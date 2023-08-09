/*
  ReadAnalogVoltage

*/

#define sensor_pin A7
const double delay_time = 250;  // milliseconds


void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
  pinMode(sensor_pin, INPUT);
  print_headers();
}

double last_read = millis();
void loop() {
  if ((millis() - last_read) >= delay_time) {
    // Getting voltage
    double voltage = get_voltage();

    // print out the value you read:
    Serial.print(last_read/1000, 3);
    Serial.print(" ");
    Serial.print(voltage, 3);
    Serial.println();
    last_read = millis();
  }
}

double get_voltage() {
  // Function read the sensor and return the calculated voltage.
  double val = analogRead(sensor_pin);
  return val * (5.0 / 1023.0);
}

void print_headers() {
  Serial.print("time ");
  Serial.print("voltage");
  Serial.println();
}