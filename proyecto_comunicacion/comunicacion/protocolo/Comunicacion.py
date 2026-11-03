# -*- coding: utf-8 -*-
"""Construccion y verificacion de tramas UART para el ESP32.

Formato de solicitud:
    CI(1) | TI(1) | NU(1) | DATOS(n) | LG(2) | V(1) | CF(1)

CI = '&', CF = '*'.
LG: uint16 little-endian, longitud total menos el byte CF.
V: XOR de todos los bytes desde CI hasta el ultimo byte de LG.

Esta clase construye solicitudes y valida respuestas del firmware incluido
ESP32_UART_WIFI_Socket_Core0.ino. Solicitudes y respuestas llevan LG y XOR.
"""

from struct import pack, unpack_from


class Comunicacion:
    caracterDeInicio = '&'
    caracterDeFin = '*'
    bufferIndiceMaximo = 120

    # Codigos ASCII que el firmware compara en obtenerInstruccion().
    ADMINISTRACION = ord('0')
    SOLICITAR_VERSION = ord('1')
    WIFI_CONECTAR = ord('2')
    WIFI_DESCONECTAR = ord('3')
    SOCKET_CONECTAR = ord('4')
    SOCKET_DESCONECTAR = ord('5')
    RED_ESTADO_RESPUESTA = ord('6')
    RED_CONSULTAR_ESTADO = ord('7')
    SOCKET_ENVIAR_DATOS = ord('8')
    SOCKET_DATOS_RESPUESTA = ord('9')
    MAX_DATOS_TCP = 64

    CONTROL = ord('1')
    MODIFICAR_BANDERAS = ord('0')
    LEER_SENALES = ord('2')
    LEER_SENALES_RESPUESTA = ord('3')

    def __init__(self):
        self.arregloByte = b''
        self.tamanioInstruccion = 0

    @staticmethod
    def _validarByte(valor, nombre='dato'):
        if not isinstance(valor, int) or not (0 <= valor <= 255):
            raise ValueError(f'{nombre} debe ser un entero entre 0 y 255.')
        return valor

    @staticmethod
    def calcularMascara(datos):
        """Devuelve la mascara XOR de todos los bytes recibidos."""
        mascara = 0
        for dato in datos:
            mascara ^= dato
        return mascara

    def crearInstruccion(self, tipo=ADMINISTRACION,
                         instruccion=SOLICITAR_VERSION, *args):
        """Genera una trama de bytes lista para enviar por UART.

        Cada argumento adicional puede ser un byte (int), bytes,
        bytearray, memoryview o una lista/tupla de bytes (enteros 0..255).

        Ejemplos:
          crearInstruccion(ADMINISTRACION, SOLICITAR_VERSION)
          crearInstruccion(CONTROL, MODIFICAR_BANDERAS, [ord('1'), ord('1')])
          crearInstruccion(CONTROL, LEER_SENALES)
        """
        tipo = self._validarByte(tipo, 'tipo')
        instruccion = self._validarByte(instruccion, 'instruccion')

        cadena = bytearray((ord(self.caracterDeInicio), tipo, instruccion))

        for item in args:
            if isinstance(item, int):
                cadena.append(self._validarByte(item))
            elif isinstance(item, (bytes, bytearray, memoryview)):
                cadena.extend(item)
            elif isinstance(item, (list, tuple)):
                cadena.extend(self._validarByte(valor) for valor in item)
            else:
                raise TypeError(
                    'Los datos deben ser bytes, bytearray, memoryview, '
                    'un entero o una lista/tupla de enteros de 0 a 255.'
                )

        # LG cuenta todos los bytes excepto el caracter final CF,
        # incluidos LG(2) y la mascara V(1).
        longitud = len(cadena) + 2 + 1
        if longitud + 1 > self.bufferIndiceMaximo:
            raise ValueError(
                f'La trama excede el maximo de {self.bufferIndiceMaximo} bytes.'
            )

        cadena.extend(pack('<H', longitud))
        cadena.append(self.calcularMascara(cadena))
        cadena.append(ord(self.caracterDeFin))

        self.arregloByte = bytes(cadena)
        self.tamanioInstruccion = len(self.arregloByte)
        return self.arregloByte

    def verificarTrama(self, trama):
        """Comprueba CI, CF, LG y V usando el mismo criterio que ESP32."""
        if not isinstance(trama, (bytes, bytearray, memoryview)):
            return False
        tamanio = len(trama)
        if not 7 <= tamanio <= self.bufferIndiceMaximo:
            return False
        if trama[0] != ord(self.caracterDeInicio):
            return False
        if trama[-1] != ord(self.caracterDeFin):
            return False

        longitudTrama = unpack_from('<H', trama, tamanio - 4)[0]
        mascaraTrama = trama[tamanio - 2]
        escrituraLongitud = tamanio - 1
        escrituraMascara = self.calcularMascara(trama[:-2])
        return (escrituraLongitud == longitudTrama and
                escrituraMascara == mascaraTrama)

    def solicitarVersion(self):
        return self.crearInstruccion(
            self.ADMINISTRACION, self.SOLICITAR_VERSION
        )

    def modificarBandera(self, indice, valor):
        """Modifica M[0]..M[9] con valor 0..9 (limite del firmware actual).

        El ESP32 interpreta cada campo como un caracter ASCII decimal
        y le resta 48. Para indices 10..79 sera necesario modificar
        obtenerInstruccion() en el ESP32.
        """
        if not isinstance(indice, int) or not (0 <= indice <= 9):
            raise ValueError('El ESP32 actual admite indices de 0 a 9.')
        if not isinstance(valor, int) or not (0 <= valor <= 9):
            raise ValueError('El ESP32 actual admite valores de 0 a 9.')

        return self.crearInstruccion(
            self.CONTROL, self.MODIFICAR_BANDERAS,
            ord('0') + indice, ord('0') + valor
        )

    def solicitarSenales(self):
        return self.crearInstruccion(self.CONTROL, self.LEER_SENALES)


    def conectarWiFi(self):
        return self.crearInstruccion(self.ADMINISTRACION, self.WIFI_CONECTAR)

    def desconectarWiFi(self):
        return self.crearInstruccion(self.ADMINISTRACION, self.WIFI_DESCONECTAR)

    def conectarSocket(self):
        return self.crearInstruccion(self.ADMINISTRACION, self.SOCKET_CONECTAR)

    def desconectarSocket(self):
        return self.crearInstruccion(self.ADMINISTRACION, self.SOCKET_DESCONECTAR)

    def consultarEstadoRed(self):
        return self.crearInstruccion(self.ADMINISTRACION, self.RED_CONSULTAR_ESTADO)

    def enviarDatosSocket(self, datos):
        if isinstance(datos, str):
            datos = datos.encode('utf-8')
        datos = bytes(datos)
        if not 1 <= len(datos) <= self.MAX_DATOS_TCP:
            raise ValueError('El envio TCP admite entre 1 y 64 bytes por instruccion.')
        return self.crearInstruccion(
            self.ADMINISTRACION, self.SOCKET_ENVIAR_DATOS, datos
        )

    def extraerTramas(self, buffer):
        """Extrae tramas completas y validas del bytearray mutable `buffer`.

        Tolera bytes de ruido, fragmentos recibidos por UART, varias tramas
        y apariciones de '&' o '*' dentro de DATOS. Preserva fragmentos.
        """
        if not isinstance(buffer, bytearray):
            raise TypeError('buffer debe ser bytearray')
        resultado = []
        while len(buffer) >= 7:
            trama_encontrada = False
            for inicio in range(len(buffer) - 6):
                if buffer[inicio] != ord(self.caracterDeInicio):
                    continue
                for fin in range(inicio + 6, min(len(buffer), inicio + self.bufferIndiceMaximo)):
                    if buffer[fin] != ord(self.caracterDeFin):
                        continue
                    candidato = bytes(buffer[inicio:fin + 1])
                    if self.verificarTrama(candidato):
                        resultado.append(candidato)
                        del buffer[:fin + 1]
                        trama_encontrada = True
                        break
                if trama_encontrada:
                    break
            if trama_encontrada:
                continue
            inicio = buffer.find(bytes((ord(self.caracterDeInicio),)))
            if inicio == -1:
                buffer.clear()
            elif inicio > 0:
                del buffer[:inicio]
            if len(buffer) > self.bufferIndiceMaximo:
                del buffer[:len(buffer) - self.bufferIndiceMaximo]
            break
        return resultado

    @staticmethod
    def extraerDatos(trama):
        """Devuelve bytes de DATOS de una trama completa ya verificada."""
        return bytes(trama[3:-4])

    def decodificarEstadoRed(self, trama):
        if not self.verificarTrama(trama):
            raise ValueError('Trama de estado no valida.')
        if (trama[1] != self.ADMINISTRACION or
                trama[2] != self.RED_ESTADO_RESPUESTA):
            raise ValueError('La respuesta no es de estado de red.')
        datos = self.extraerDatos(trama)
        if len(datos) != 7:
            raise ValueError('El estado de red debe contener 7 bytes.')
        return {
            'wifi': datos[0],
            'socket': datos[1],
            'error': datos[2],
            'ip': '.'.join(str(b) for b in datos[3:7]),
        }


if __name__ == '__main__':
    comunicacion = Comunicacion()
    for nombre, trama in (
        ('Version', comunicacion.solicitarVersion()),
        ('Activar M[1]', comunicacion.modificarBandera(1, 1)),
        ('Desactivar M[2]', comunicacion.modificarBandera(2, 1)),
        ('Leer senales', comunicacion.solicitarSenales()),
    ):
        print(f'{nombre}: {trama.hex(" ").upper()} '
              f'({len(trama)} bytes, valida={comunicacion.verificarTrama(trama)})')
