/* Definicion de pines */
int DI_00 = 32;
int DI_01 = 33;
int DI_02 = 25;
int DI_03 = 26;
int DI_04 = 27;
int DI_05 = 14;

int DO_00 = 23;
int DO_01 = 22;
int DO_02 = 21;

// Señales virtuales
// Entradas
byte X_00 = 0;
byte X_01 = 0;
byte X_02 = 0;
byte X_03 = 0;
byte X_04 = 0;
byte X_05 = 0;

byte Y_00 = 0;
byte Y_01 = 0;
byte Y_02 = 0;

byte M_00 = 0;
byte M_01 = 0;
byte M_02 = 0;
byte M_03 = 0;
byte M_04 = 0;

/////////////////////////////////////////// Temporizadores

#define  numeroDeTON 16

struct temporizador {
    byte entrada;
    byte salida;
    unsigned long tiempo;
    unsigned long tiempoActual;
} TON[numeroDeTON];


struct temporizadorAux {
    byte bandera;
    unsigned long tiempo_Aux1;
    unsigned long tiempo_Aux2;
} TON_Aux[numeroDeTON];

void actualizarTON (int);





void setup() {
  pinMode(DI_00, INPUT);
  pinMode(DI_01, INPUT);
  pinMode(DI_02, INPUT);
  pinMode(DI_03, INPUT);
  pinMode(DI_04, INPUT);
  pinMode(DI_05, INPUT);



  pinMode(DO_00, OUTPUT);
  pinMode(DO_01, OUTPUT);
  pinMode(DO_02, OUTPUT);

  // Definicion de Teporizadores
  TON[0].tiempo = (unsigned long) 5000;
  TON[1].tiempo = (unsigned long) 2000;
  TON[2].tiempo = (unsigned long) 6000;
  
  Serial.begin(115200);
}

void loop() {
  //programa

  // Activacion del sistema
  M_00 =(X_00 || M_00) && !X_01 && !M_04;

  // Etapa A+
  M_01 = M_00 && !M_02 && !M_03;
  // Etapa A-
  M_02 = M_00 && ( (M_01 && X_03) || M_02 ) && !M_03;
  // Etapa B+
  M_03 = M_00 && ( (M_02 && X_02) || M_03 ) && !M_04;
  // Etapa B-
  M_04 = M_00 && ( (M_03 && X_05) || M_04 ) && !X_04;

  // Salidas 
  Y_00 = M_00 && (M_01 || Y_00) && !M_02; 
  Y_01 = M_00 && (M_03 || Y_01) && !M_04; 

  // Para debugear
  Serial.printf("\nX_00 %d, X_01 %d, X_02 %d, X_03 %d, X_04 %d, X_05 %d, Y_00 %d, Y_01 %d M_00 %d, M_01 %d, M_02 %d, M_03 %d, M_04 %d,", 
      X_00, X_01,  X_02, X_03,  X_04, X_05,Y_00, Y_01, M_00, M_01,  M_02, M_03,  M_04);

  // Mapeando entradas y salidas
  X_00 = digitalRead(DI_00);
  X_01 = digitalRead(DI_01);
  X_02 = digitalRead(DI_02);
  X_03 = digitalRead(DI_03);
  X_04 = digitalRead(DI_04);
  X_05 = digitalRead(DI_05);
  
  
  digitalWrite(DO_00, Y_00);
  digitalWrite(DO_01, Y_01);
  digitalWrite(DO_02, Y_02);

}


/////////////////////////////////////////// Temporizadores

void actualizarTON (int i) {
     if (TON [i].entrada)
   {
        if (!TON_Aux[i].bandera) {
           TON_Aux[i].bandera = true;
           TON_Aux[i].tiempo_Aux1 = millis ();  
        }
        TON_Aux[i].tiempo_Aux2 = millis ();
        TON [i].tiempoActual = TON_Aux[i].tiempo_Aux2 - TON_Aux[i].tiempo_Aux1;

        if (TON [i].tiempoActual > TON [i].tiempo) {
            TON [i].salida = true;
        }
    } else {
        TON [i].salida = false;
        TON_Aux[i].bandera = false;
    }
}
