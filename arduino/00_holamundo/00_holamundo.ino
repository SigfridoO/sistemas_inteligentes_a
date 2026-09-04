/* Definicion de pines */
int DI_00 = 32;
int DI_01 = 33;

int DO_00 = 23; //25;

// Señales virtuales
// Entradas
byte X_00 = 0;
byte X_01 = 0;

byte Y_00 = 0;

void setup() {
  pinMode(DI_00, INPUT);
  pinMode(DI_01, INPUT);

  pinMode(DO_00, OUTPUT);
  Serial.begin(115200);
}

void loop() {
  //programa

  Y_00 = (Y_00 || X_00) && !X_01;

  // Para debugear
  Serial.printf("\nX_00 %d, X_01 %d, Y_00 %d", X_00, X_01, Y_00);

  // Mapeando entradas y salidas
  X_00 = digitalRead(DI_00);
  X_01 = digitalRead(DI_01);
  digitalWrite(DO_00, Y_00);

}
