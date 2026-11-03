# Comunicación UART ESP32 y Python

Versión sin Wi-Fi ni tareas adicionales en ESP32.

1. Cargar `ESP32/09_comunicaion_serie.ino` en un ESP32-WROOM-32 (pines de este módulo).
2. Instalar Python: `pip install pyserial InquirerPy blessed`.
3. Conectar el ESP32 y ajustar `/dev/ttyUSB0` en `Menu.py` si es necesario.
4. Ejecutar `python comunicacion/menu/Menu.py` desde esta carpeta.
5. En Puerto serie: abrir. En Señales digitales: Leer entradas y salidas. Salir con Q, Enter o Esc.

Protocolo: `& | tipo(1) | numero(1) | datos | LG(2 little-endian) | XOR(1) | *`.
LG cuenta bytes desde `&` hasta XOR; XOR se calcula desde `&` hasta los 2 bytes LG.
Solicitud de señales: 26 31 32 06 00 23 2A. Respuesta: 9 bytes, datos X,Y.
Hay seis entradas físicas X00-X05 y tres salidas físicas Y00-Y02; las otras posiciones se mantienen en 0.
Las entradas se configuran como INPUT: se requiere una señal eléctrica definida (pull-up/pull-down externo). No aplicar 5 V directamente.
Los GPIO corresponden al ESP32-WROOM-32; para ESP32-S3 es necesario remapearlos.
El monitor está preparado para UART de 115200 baudios y consultas cada 0.5 s.
No se ha validado con hardware físico.

## Temporizadores del menu

En `comunicacion/menu/Menu.py` se declaran los temporizadores en `self.TON = []`.
Actualmente `self.TON[0]` regula la consulta de señales digitales cada 0.5 segundos.
Para cambiar el periodo, edita `self.TON[0].tiempo = 0.5` (segundos).
Se reinicia al entrar a la pantalla y se desactiva al salir.
Los siguientes temporizadores se agregarán con `self.TON.append(Temporizador(...))` y se usarán por índice.
