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

int LED = 2;
byte estado = 0;

void setup() {
  pinMode(LED, OUTPUT);
  C[0].cuentaMaxima = 8;
  Serial.begin(115200);
}

void loop() {

  estado = !estado;
  digitalWrite(LED, estado);
  delay(500);
 
  C[0].habilitar =  1; // Señal para habilitar el funcionamiento del contador
  C[0].entrada = estado; // Se describe aqui la señal que contine los pulsos de entrada
  actualizarContador(0);
  Serial.printf("\nCuentaActual %d Salida %d", C[0].cuentaActual, C[0].salida);
  // Cuando llegue a la cuenta final se activa la salida del contador 
  // La señal de reset reinicia la cuenta
  // La señal de habilitar permite que el contador funcione
}



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
