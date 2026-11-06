# Servidor TCP multicliente

## Descripción

`ServidorSocket.py` contiene la clase `ServidorSocket`, destinada a recibir conexiones TCP desde programas Python y, posteriormente, desde uno o varios ESP32. Sustituye al antiguo `servidor_tcp/servidor_tcp.py`, que fue eliminado del proyecto.

- Escucha en **0.0.0.0:65432** de forma predeterminada (el puerto coincide con `puertoTCP` del firmware actual).
- Utiliza `socket.AF_INET` y `socket.SOCK_STREAM` (TCP/IPv4).
- Acepta varias conexiones y crea un `threading.Thread` por cliente.
- Protege el conjunto de sockets mediante `threading.Lock`.
- Utiliza `threading.Event` para detener el servidor y cerrar las conexiones.
- Admite líneas UTF-8 terminadas en `\n` (máximo 4096 bytes por línea).
- Responde `aceptada\n` a mensajes normales; responde `cerrada\n` y desconecta **solo ese cliente** al recibir `cerrar\n`.

## Ejecución

Desde la raíz `proyecto_comunicacion/`:

```bash
python python/wifi/ServidorSocket.py
```

Para definir otra interfaz y puerto:

```bash
python python/wifi/ServidorSocket.py --host 0.0.0.0 --port 65432
```

Para comprobarlo con dos terminales en la misma computadora:

```bash
python python/wifi/ServidorSocket.py --host 127.0.0.1 --port 65432
```

En otra terminal:

```bash
python -c "import socket; s=socket.create_connection(('127.0.0.1',65432)); s.sendall(b'hola\n'); print(s.recv(1024)); s.sendall(b'cerrar\n'); print(s.recv(1024)); s.close()"
```

Para clientes en la red local, utilizar la dirección IP real de la computadora servidor en el cliente. `0.0.0.0` es una dirección **de escucha**, no un destino al que conectarse.

## Relación con ESP32

El firmware está en `ESP32/comunicacion/comunicacion.ino` e incluye un cliente TCP. Su configuración actual utiliza:

```cpp
IPAddress servidorTCP(192, 168, 1, 100);
const uint16_t puertoTCP = 65432;
```

Cambia `192.168.1.100` por la IP LAN de la computadora que ejecuta el servidor. El ESP32 y el servidor deben tener conectividad TCP y el cortafuegos debe permitir el puerto indicado.

**Compatibilidad actual del protocolo:** este servidor interpreta **texto delimitado por salto de línea**. El ESP32 puede enviar bytes arbitrarios por TCP, pero el servidor solo procesará líneas terminadas en `\n`. La opción de enviar mensajes TCP en `Menu.py` no añade por sí sola un salto de línea. Hasta adaptar el protocolo o la función de envío, el servidor puede quedar esperando el delimitador. Las tramas binarias UART con longitud y XOR **no están implementadas aquí**.

## Diagrama

```text
                     EQUIPO SERVIDOR (Python)
                     ServidorSocket.iniciar()
                                |
                        socket.accept()
                                |
              +-----------------+-----------------+
              |                 |                 |
        threading.Thread  threading.Thread  threading.Thread
              |                 |                 |
         Cliente PC 1       Cliente PC 2      ESP32 (futuro)
          TCP/IPv4           TCP/IPv4           Wi-Fi TCP
```

## Extensión futura

El método `procesar_mensaje(mensaje, direccion)` es el punto de extensión para añadir identificación de dispositivos y órdenes. Para implementar las tramas binarias `CI|TI|NU|DATOS|LG|V|CF` del proyecto será necesario reemplazar la separación por `\n` con un analizador por longitud, validación y buffer individual para cada conexión.

## Consideraciones

El servidor no tiene autenticación ni cifrado TLS. Utilizar únicamente en redes locales de confianza. Cada cliente consume un hilo y no hay un límite estricto de clientes activos: antes de desplegarlo en un entorno abierto se deben incorporar límites, autenticación, registro y control de recursos.

## Cliente TCP de prueba

`clienteSocket.py` es un cliente de texto independiente, compatible con el servidor de esta carpeta. Usa UTF-8 y delimita cada mensaje con `\n`.

En una terminal, iniciar el servidor:

```bash
python python/wifi/ServidorSocket.py --host 0.0.0.0 --port 65432
```

En otra terminal de la misma computadora:

```bash
python python/wifi/clienteSocket.py --host 127.0.0.1 --port 65432
```

Para probarlo desde otra computadora, reemplazar `127.0.0.1` por la IP del servidor. Enviar `cerrar` para finalizar únicamente esa conexión.

**Importante:** el cliente y servidor actuales trabajan con texto delimitado por salto de línea. Las tramas binarias `CI|TI|NU|DATOS|LG|V|CF` del firmware ESP32 requieren una adaptación posterior del servidor.
