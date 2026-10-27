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
#define NUMERO_X 8
byte X[NUMERO_X];
//byte X_00 = 0;
//byte X_01 = 0;
//byte X_02 = 0;
//byte X_03 = 0;
//byte X_04 = 0;
//byte X_05 = 0;

#define NUMERO_Y 8
byte Y[NUMERO_Y];
//byte Y_00 = 0;
//byte Y_01 = 0;
//byte Y_02 = 0;

/*
byte M_00 = 0;
byte M_01 = 0;
byte M_02 = 0;
byte M_03 = 0;
byte M_04 = 0;
*/
#define numero_banderas 80
byte M[numero_banderas];
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

//////////////////////////////////////////////// Comunicación
/*
 *  CI|TI|NU|DATOS.................|LG|V|CF
 *  00 01 02 03 04 05 06 07 .......
 *  
 *  CI -- Caracter de inicio
 *  TI -- Tipo de instrucción
 *  NU -- Número de instrucción
 *  LG -- Longitud
 *  V  -- Verificación
 *  CF -- Caracter de Final
 */

#define bufferIndiceMaximo 120
byte bufferLectura[bufferIndiceMaximo];
int bufferIndice=  0;

byte bufferInstruccion[bufferIndiceMaximo];
int bufferIndiceInstruccion = 0;

void leerInstruccionDeBuffer(byte *, int *, byte *, int *);
void obtenerInstruccion();

char caracterDeInicio = '&';
char caracterDeFin = '*';
int  escrituraLongitud = 0;
byte escrituraMascara = 0;


void colocarDatosEnBuffer();

#define bufferIndiceEscrituraMaximo 120
byte bufferEscritura[bufferIndiceEscrituraMaximo];
int bufferEscrituraIndice = 0;

void bufferEscrituraLimpiar(void);
void establecerInicioEscritura(int, int);
void establecerFinEscritura(void);

void imprimirTrama(byte *, int, int);

byte obtenerByteDeArregloByte(byte *);
uint16_t obtenerInt16DeArregloByte (byte *);
uint32_t obtenerInt32DeArregloByte (byte *);
float obtenerFloatDeArregloByte (byte *);
char obtenerCaracterDeArregloByte (byte *);

void escribirUint8EnBufferEscritura(uint8_t);
void escribirUint16EenBufferEscritura(uint16_t);
void escribirUint32EnBufferEscritura(uint32_t);
void escribirFloatEnBufferEscritura(float);
void escribirCaracterEnBufferEscritura(char);



// FIXME: Actualizar codigos
#define ADMINISTRACION 48 // '0'
#define SOLICITAR_VERSION 49  // '1'

#define CONTROL 49 // '1'
#define MODIFICAR_BANDERAS 48 // '0'

#define LEER_SENALES 50 // '2'
#define LEER_SENALES_RESPUESTA 51 // '3'


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
  colocarDatosEnBuffer();  
  leerInstruccionDeBuffer(bufferLectura, &bufferIndice, bufferInstruccion, &bufferIndiceInstruccion);
  
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

  Y[0] = !TON[0].salida && !C[0].salida;

  // Secuencia
  TON[3].entrada = !TON[3].salida;
  actualizarTON(3);

  if (TON[3].salida) {
      contador++;
  }

  // Control del programa
  M[0] = (X[0] || M[0] || M[1]) && !X[1] && !M[2] ;

  Y[1] = M[0];

  M[1] = 0;
  M[2] = 0;
  
  
  // Para debugear
  //Serial.printf ("\nX_00 %d, X_01 %d M_00 %d, M_01 %d", X_00, X_01, M_00, M_01);
  // Mapeando entradas y salidas
  X[0] = digitalRead(DI_00);
  X[1] = digitalRead(DI_01);
  X[2] = digitalRead(DI_02);
  X[3] = digitalRead(DI_03);
  X[4] = digitalRead(DI_04);
  X[5] = digitalRead(DI_05);

  
  digitalWrite(DO_00, Y[0]);
  digitalWrite(DO_01, Y[1]);
  digitalWrite(DO_02, Y[2]);

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


///////////////////////////////////////////////// Comunicación
void colocarDatosEnBuffer(){
  byte caracter = 0;
  int aux = 0;

  while (Serial.available() > 0) {
    caracter = Serial.read();
    bufferLectura[bufferIndice++] = caracter;

    if (bufferIndice + 1 > bufferIndiceMaximo){
      aux = bufferIndiceMaximo >> 1;
      for (int i = aux; i < bufferIndiceMaximo + 1; i++) {
        bufferIndice = i - aux;
        bufferLectura[bufferIndice] = bufferLectura[i];
      }
    }
  }
//  imprimirTrama(bufferLectura, 0, bufferIndice);
}

void imprimirTrama(byte *prtTrama, int inicio, int tamanio){
  if (tamanio > 0) {
    Serial.print("\n>>");
    for (int k = inicio; k < inicio + tamanio; k++) {
      Serial.write(*(prtTrama + k));
      //Serial.write(prtTrama [k]);
    }
  }
}

void leerInstruccionDeBuffer(byte *ptrBufferLectura, int *ptrBufferIndice, 
  byte *ptrBufferInstruccion, int *ptrTamanioBufferInstruccion){
  int i = 0;
  int k = 0;
  int encontrado = -1;

  if (ptrBufferLectura[*ptrBufferIndice - 1] == caracterDeFin) {
      for (k = *ptrBufferIndice; k >= 0; --k) {
         if(ptrBufferLectura[k] == (byte) caracterDeInicio) {
            encontrado = k;
            if (encontrado >= 0) {
              *ptrTamanioBufferInstruccion = 0;
  
                for (int j = k; j < *ptrBufferIndice; j++) {
                  ptrBufferInstruccion[*ptrTamanioBufferInstruccion] = ptrBufferLectura[j];
                  (*ptrTamanioBufferInstruccion)++;
                }
                // Aqui tendremos la instruccion separada
                // TODO: procesar la instruccion
                obtenerInstruccion();
                
//                imprimirTrama(ptrBufferInstruccion, 0, *ptrTamanioBufferInstruccion );
                *ptrBufferIndice = k;
            } // if
         } // if 
      } // for
  } // if 
}

void obtenerInstruccion(){
    int *tamanio;
    byte *cadena;

    int tipoDeInstruccion = 0;
    int numeroDeInstruccion = 0;

    tamanio = &bufferIndiceInstruccion;
    cadena = bufferInstruccion;

    tipoDeInstruccion = obtenerByteDeArregloByte(cadena + 1);
    numeroDeInstruccion = obtenerByteDeArregloByte(cadena + 2);

    //Serial.printf("\ntipo: %d", tipoDeInstruccion);
    //Serial.printf("\nnumero: %d", numeroDeInstruccion);

    byte indice = 0;
    byte valor = 0;
    switch(tipoDeInstruccion) {
        case ADMINISTRACION:
          switch (numeroDeInstruccion) {
              case SOLICITAR_VERSION:
                  Serial.print("\nVersion 0.0.1 en EPS32 - \nSigfrido Soria");
                  break;
          }

        
          break;

        case CONTROL:
            switch(numeroDeInstruccion) {
                case MODIFICAR_BANDERAS:

                    indice = obtenerByteDeArregloByte(cadena + 3) - 48;
                    valor = obtenerByteDeArregloByte(cadena + 4) - 48;

                    M[indice] = valor;
                    break;
                case LEER_SENALES:
                    establecerInicioEscritura(CONTROL, LEER_SENALES_RESPUESTA);

                    // Colocando las entradas
                    byte aux = 0;
                    for (int i = 0; i < 8; i++) {
                        aux |= X[i] << i;
                    }
                    escribirUint8EnBufferEscritura(aux);

                    // Colocando las salidas
                    aux = 0;
                    for (int i = 0; i < 8; i++) {
                        aux |= Y[i] << i;
                    }
                    escribirUint8EnBufferEscritura(aux);
                    
                    establecerFinEscritura();
                    Serial.write(bufferEscritura, bufferEscrituraIndice);
                    break;
            } 
        
            break;
    }
}

byte obtenerByteDeArregloByte(byte *arreglo){
    byte *punteroByte;
    punteroByte = (byte *) arreglo;
    return *punteroByte;
}
uint16_t obtenerInt16DeArregloByte(byte *arreglo){
    return (uint16_t) arreglo[0] | (uint16_t) arreglo[1] << 8;
}

uint32_t obtenerInt32DeArregloByte (byte *arreglo){
  return (uint32_t) arreglo[0] | 
         (uint32_t) arreglo[1] << 8 | 
         (uint32_t) arreglo[2] << 16 | 
         (uint32_t) arreglo[3] << 24;
}



void bufferEscrituraLimpiar(void){
  for (int i = 0; i < bufferIndiceEscrituraMaximo; i++) {
    bufferEscritura[i] = (byte) 0;
  }
  bufferEscrituraIndice = 0;
  escrituraLongitud = 0;
  escrituraMascara = 0;
}

void establecerInicioEscritura(int tipo, int numeroInstruccion) {
  bufferEscrituraLimpiar();
  escribirCaracterEnBufferEscritura(caracterDeInicio);
  escribirUint16EnBufferEscritura(tipo);
  escribirUint16EnBufferEscritura(numeroInstruccion);
}

void establecerFinEscritura(void){

  escribirCaracterEnBufferEscritura(caracterDeFin);
}


void escribirUint16EnBufferEscritura(uint16_t numero) {
  byte b0 = (byte) (numero & 0xFFU);
  byte b1 = (byte) ((numero >> 8) & 0xFFU);
  bufferEscritura[bufferEscrituraIndice++] = b0;
  bufferEscritura[bufferEscrituraIndice++] = b1;
}

void escribirCaracterEnBufferEscritura(char caracter) {
  bufferEscritura[bufferEscrituraIndice++] = (char) caracter;
}

void escribirUint8EnBufferEscritura(uint8_t numero) {
  bufferEscritura[bufferEscrituraIndice++] =  numero;
}
