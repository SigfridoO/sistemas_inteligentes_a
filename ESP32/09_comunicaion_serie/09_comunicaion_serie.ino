//////////////////////////////////////////////// Definicion de pines 
int DI_00 = 32;
int DI_01 = 33;
int DI_02 = 25;
int DI_03 = 26;
int DI_04 = 27;
int DI_05 = 14;

int DO_00 = 2;
int DO_01 = 23;
int DO_02 = 22;

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

//////////////////////////////////////////////// Temporizadores

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

//////////////////////////////////////////////// Contadores
#define numeroDeContadores 8

struct contador {
    byte entrada;
    byte salida;
    byte habilitar;
    int cuentaActual;
    int cuentaMaxima;
    byte reset;
    byte aux1;
    byte aux2;
} C[numeroDeContadores];
void actualizarContador (byte);


// Secuencia
int contador;

// Comunicación por el puerto serie
byte caracter;

void setup() {
  // Configuracion de pines
  pinMode(DI_00, INPUT);
  pinMode(DI_01, INPUT);
  pinMode(DI_02, INPUT);
  pinMode(DI_03, INPUT);
  pinMode(DI_04, INPUT);
  pinMode(DI_05, INPUT);


  pinMode(DO_00, OUTPUT);
  pinMode(DO_01, OUTPUT);
  pinMode(DO_02, OUTPUT);

  // Temporizandores
    // Señal de vida
    TON[0].tiempo = (unsigned long) 800;
    TON[1].tiempo = (unsigned long) 300;
    TON[2].tiempo = (unsigned long) 2000;

    // Secuencia
    TON[3].tiempo = (unsigned long) 1000;

    contador = 0;

  // Contadores
  C[0].cuentaMaxima = 3;
  
  // Puerto Serie
  Serial.begin(115200);
}


void loop() {
  //////////////////////////////////////////////////////////
  // leer datos del puerto serie
  if (Serial.available() > 0) {
      caracter = Serial.read();
      if ((char) caracter == 'k'){
        M_01 = 1;
      }
  }
  
  
  //Señal de vida

  TON[0].entrada = !TON[1].salida && !C[0].salida;
  actualizarTON(0);

  TON[1].entrada = TON[0].salida;
  actualizarTON(1);

  C[0].habilitar =  !TON[2].salida;
  C[0].entrada = !TON[0].salida;
  actualizarContador(0);

  TON[2].entrada = C[0].salida;
  actualizarTON(2);

  Y_00 = !TON[0].salida && !C[0].salida;

  // Secuencia
  TON[3].entrada = !TON[3].salida;
  actualizarTON(3);

  if (TON[3].salida) {
      contador++;
  }

  // Control del programa
  M_00 = (X_00 || M_00 || M_01) && !X_01;

  Y_01 = M_00;

  
  // Para debugear
  //Serial.printf ("\nX_00 %d, X_01 %d M_00 %d, M_01 %d", X_00, X_01, M_00, M_01);
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

//////////////////////////////////////////////// Temporizadores


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


//////////////////////////////////////////////// Contadores


void actualizarContador (byte numeroContador) {

    if (!C[numeroContador].habilitar) {
        C[numeroContador].salida = 0;
        C[numeroContador].cuentaActual = 0;
    } else {
        C[numeroContador].aux2 = C[numeroContador].aux1 & !C[numeroContador].entrada;
    
        if (C[numeroContador].aux2) {
            //if (C[numeroContador].cuentaActual < C[numeroContador].cuentaMaxima){
              C[numeroContador].cuentaActual++;
            //}
        }
    }
    
    if (C[numeroContador].reset) {
        C[numeroContador].cuentaActual = 0;
    }
    if (C[numeroContador].cuentaActual >= C[numeroContador].cuentaMaxima ) {
        C[numeroContador].salida = 1;
    } else {
        C[numeroContador].salida = 0;
    }
    
    C[numeroContador].aux1 = C[numeroContador].entrada;
    C[numeroContador].reset = 0;
}
