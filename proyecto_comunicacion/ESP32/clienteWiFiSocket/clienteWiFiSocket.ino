#include <WiFi.h>
#include <WiFiClient.h>

const char* ssid = "ardilluda2";
const char* password = "01971101";

const char* server_ip = "192.168.0.XXX";
const uint16_t server_port = 65432;

WiFiClient cliente;
uint8_t contador = 0;

//////////////////////////////// Señales digitales
#define NUMERO_DE_M  8
uint8_t M[NUMERO_DE_M] = {0};

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

void setup() {
    Serial.begin(115200);
    TON[0].tiempo = 1000;
    TON[1].tiempo = 3000;

    WiFi.mode(WIFI_STA);
    WiFi.begin(ssid, password);
    Serial.println("Inciando cliente WiFi");
}

void loop() {
  // put your main code here, to run repeatedly:

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
