/* Definicion de pines */
int DI_00 = 32;
int DI_01 = 33;

int DO_00 = 23;

// Señales virtuales
// Entradas
byte X_00 = 0;
byte X_01 = 0;

byte Y_00 = 0;

byte M_00 = 0;

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

  pinMode(DO_00, OUTPUT);

  // Definicion de Teporizadores
  TON[0].tiempo = (unsigned long)1 *5000;
  
  Serial.begin(115200);
}

void loop() {
  //programa
  // señal de acntivacion
  M_00 = (M_00 || X_00) && !X_01 && !TON[0].salida;

  TON[0].entrada = M_00;
  actualizarTON(0);

  // Lampara piloto
  Y_00 = M_00;


  // Para debugear
  Serial.printf("\nX_00 %d, X_01 %d, Y_00 %d", X_00, X_01, Y_00);

  // Mapeando entradas y salidas
  X_00 = digitalRead(DI_00);
  X_01 = digitalRead(DI_01);
  digitalWrite(DO_00, Y_00);

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
