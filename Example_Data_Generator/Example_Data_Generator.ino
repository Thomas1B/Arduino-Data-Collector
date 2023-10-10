/*
Script for generator random numbers

*/


bool print_headers = true;  // true - print column header, false no headers.

unsigned long interval = 500;  // time interval between readings.


void setup() {
  Serial.begin(9600);
  while (!Serial) {
    ;  // Waiting for Serial port to connect
  }

  String headers = "Integers, Floats";
  if (print_headers) {
    Serial.println(headers);
  }
}


int get_rand_int(int lower = 0, int upper = 100) {
  /*
  Function to generate a random integer number between 2 given integers.

    Parameters:
      lower (int): lower bound of range.
      upper (int): upper bound of range.

    Returns:
      random integer.
  */

  return random(lower, upper);
}

float get_rand_float(float scale = 1.0) {
  /*
  Function to generate a random float number between 0 and 1.

    Parameters:
      scale (int): scale factor to increase range.

    Returns:
      random float.
  */

  float num = random(1, 401) / 101.1;

  while (num >= 1 || num <= 0) {
    num = random(1, 401) / 101.1;
  }

  return num * scale;
}


unsigned long lastReadTime = 0;
void loop() {
  if (millis() - lastReadTime >= interval) {

    int rand_int = get_rand_int();
    float rand_float = get_rand_float(5);

    Serial.print(rand_int);
    Serial.print(" ");
    Serial.println(rand_float);

    lastReadTime = millis();
  }
}
