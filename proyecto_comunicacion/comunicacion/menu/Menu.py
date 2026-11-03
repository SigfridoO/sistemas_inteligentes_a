from pathlib import Path
import sys
import threading
import time
from datetime import datetime

from InquirerPy import inquirer
from blessed import Terminal

term = Terminal()

# Permite ejecutar directamente: python comunicacion/menu/Menu.py
raiz_proyecto = Path(__file__).resolve().parent.parent
if str(raiz_proyecto) not in sys.path:
    sys.path.insert(0, str(raiz_proyecto))

from uart.UART import PuertoSerie
from protocolo.Comunicacion import Comunicacion
from temporizador.Temporizador import Temporizador


class Menu:
    def __init__(self, puerto="/dev/ttyUSB0", baudrate=115200):
        self.puerto_serie = PuertoSerie(puerto, baudrate)
        self.comunicacion = Comunicacion()
        self.X = [0] * 8
        self.Y = [0] * 8
        self.TON = []
        self.TON.append(Temporizador("TON_00", 0.5, "Lectura de señales digitales"))

    def submenu_funciones_administrativas(self):
        while True:
            self.limpiar_pantalla()
            print(f"{term.darkorange2}=============================================================")
            print(f"{term.white}Submenú funciones administrativas")
            print(f"{term.darkorange2}============================================================={term.normal}")

            opcion = inquirer.select(
                message="Seleccione una opción:",
                choices=[
                    {"name": "Obtener versión del programa", "value": "obtener_version"},
                    {"name": "Volver al menu princial", "value": "volver"},
                ],
            ).execute()

            match opcion:
                case "volver":
                    break
                case "obtener_version":
                    self.obtener_version()
            self.pausa()


    def submenu_comunicacion_serie(self):
        while True:
            self.limpiar_pantalla()
            print(f"{term.darkorange2}=============================================================")
            print(f"{term.white}Submenú comunicacion serie")
            print(f"{term.darkorange2}============================================================={term.normal}")

            opcion = inquirer.select(
                message="Seleccione una opción:",
                choices=[
                    {"name": "Abrir puerto", "value": "SERIE_ABRIR_PUERTO"},
                    {"name": "cerrar puerto", "value": "SERIE_CERRAR_PUERTO"},
                    {"name": "Volver al menu princial", "value": "volver"},
                ],
            ).execute()

            match opcion:
                case "volver":
                    break
                case "SERIE_ABRIR_PUERTO":
                    self.conectar_puerto_serie()
                case "SERIE_CERRAR_PUERTO":
                    self.desconectar_puerto_serie()
                    
            self.pausa()


    def submenu_senales_digitales(self):
        
        while True:
            self.limpiar_pantalla()
            print(f"{term.darkorange2}=============================================================")
            print(f"{term.white}Submenú señales digitales")
            print(f"{term.darkorange2}============================================================={term.normal}")

            opcion = inquirer.select(
                message="Seleccione una opción:",
                choices=[
                    {"name": "Leer entradas y salidas", "value": "leer_entradas_salidas"},
                    {"name": "Prender LED", "value": "prender_led"},
                    {"name": "Apagar LED", "value": "apagar_led"},

                    {"name": "Volver al menú principal", "value": "volver"},

                ],
            ).execute()

            match opcion:
                case "volver":
                    break
                case "leer_entradas_salidas":
                    self.leer_entradas_salidas()
                    continue

                case "prender_led":
                    self.prender_led()
                case "apagar_led":
                    self.apagar_led()
            self.pausa()

    def pausa(self):
        input("Presione Enter para continuar...")

    def limpiar_pantalla(self):
        print(term.home + term.clear)
        print()

    def mostrar_menu(self):
        
        while True:
            self.limpiar_pantalla()
            print(f"{term.darkorange2}=============================================================")
            print(f"{term.white}Menu microcontroladores")
            print(f"{term.darkorange2}============================================================={term.normal}")

            opcion = inquirer.select(
                message="Seleccione una opción:",
                choices=[
                    {"name": "Puerto serie", "value": "SUBMENU_PUERTO_SERIE"},
                    {"name": "señales digitales", "value": "submenu_senales_digitales"},
                    {"name": "Funciones administrativa", "value": "SUBMENU_FUNCIONES_ADMINISTRATIVAS"},
                    {"name": "Salir", "value": "salir"},
                ],
            ).execute()

            match opcion:
                case "salir":
                    print("Saliendo del programa...")
                    break
                case "SUBMENU_PUERTO_SERIE":
                    self.submenu_comunicacion_serie()
                case "submenu_senales_digitales":
                    self.submenu_senales_digitales()
                case "SUBMENU_FUNCIONES_ADMINISTRATIVAS":
                    self.submenu_funciones_administrativas()


    def conectar_puerto_serie(self):
        self.puerto_serie.abrir()

    def desconectar_puerto_serie(self):
        self.puerto_serie.cerrar()

    def obtener_version(self):
        if not self.puerto_serie.serial_port.is_open:
            print("Primero debes conectar el puerto serie.")
            return
        trama = self.comunicacion.solicitarVersion()
        self.puerto_serie.escribir(trama, len(trama))
        respuesta = self.puerto_serie.leer()
        print(f"Respuesta recibida: {respuesta}")

    def prender_led(self):
        if not self.puerto_serie.serial_port.is_open:
            print("Primero debes conectar el puerto serie.")
            return
        trama = self.comunicacion.modificarBandera(1, 1)
        self.puerto_serie.escribir(trama, len(trama))

    def apagar_led(self):
        if not self.puerto_serie.serial_port.is_open:
            print("Primero debes conectar el puerto serie.")
            return
        trama = self.comunicacion.modificarBandera(2, 1)
        self.puerto_serie.escribir(trama, len(trama))

    def _consultar_senales(self, detener, actualizado, bloqueo, estado):
        self.TON[0].entrada = True
        primera = True
        buffer = bytearray()
        puerto = self.puerto_serie.serial_port
        timeout_original = puerto.timeout
        try:
            puerto.timeout = 0.1
            while not detener.is_set():
                self.TON[0].actualizar()
                if not primera and not self.TON[0].salida:
                    detener.wait(0.02)
                    continue
                primera = False
                self.TON[0].reset = True
                try:
                    trama = self.comunicacion.solicitarSenales()
                    puerto.write(trama)
                    limite = time.monotonic() + 1.0
                    respuesta = None
                    while not detener.is_set() and time.monotonic() < limite:
                        bloque = puerto.read(puerto.in_waiting or 1)
                        if bloque:
                            buffer.extend(bloque)
                            for recibida in self.comunicacion.extraerTramas(buffer):
                                if (recibida[1] == self.comunicacion.CONTROL and
                                        recibida[2] == self.comunicacion.LEER_SENALES_RESPUESTA):
                                    datos = self.comunicacion.extraerDatos(recibida)
                                    if len(datos) == 2:
                                        respuesta = datos
                                        break
                        if respuesta is not None:
                            break
                    with bloqueo:
                        if respuesta is not None:
                            self.X = [(respuesta[0] >> i) & 1 for i in range(8)]
                            self.Y = [(respuesta[1] >> i) & 1 for i in range(8)]
                            estado["lecturas"] += 1
                            estado["ultima"] = datetime.now().strftime("%H:%M:%S")
                            estado["mensaje"] = "Comunicación correcta"
                        else:
                            estado["mensaje"] = "Sin respuesta válida del ESP32"
                    actualizado.set()
                except Exception as error:
                    with bloqueo:
                        estado["mensaje"] = f"Error de comunicación: {error}"
                    actualizado.set()
                    break
        finally:
            self.TON[0].entrada = False
            self.TON[0].actualizar()
            puerto.timeout = timeout_original

    def leer_entradas_salidas(self):
        if not self.puerto_serie.serial_port.is_open:
            print("Primero debes conectar el puerto serie.")
            self.pausa()
            return

        # Reiniciar TON[0] al abrir esta pantalla, antes de iniciar el hilo.
        self.TON[0].entrada = False
        self.TON[0].actualizar()
        self.TON[0].reset = False

        detener = threading.Event()
        actualizado = threading.Event()
        bloqueo = threading.Lock()
        estado = {"lecturas": 0, "ultima": "--:--:--", "mensaje": "Esperando lectura..."}
        tarea = threading.Thread(
            target=self._consultar_senales,
            args=(detener, actualizado, bloqueo, estado),
            name="LecturaSenalesESP32", daemon=True
        )
        tarea.start()
        actualizado.set()
        try:
            with term.cbreak():
                while True:
                    if actualizado.is_set():
                        actualizado.clear()
                        with bloqueo:
                            entradas, salidas = self.X.copy(), self.Y.copy()
                            mensaje, lecturas, ultima = estado["mensaje"], estado["lecturas"], estado["ultima"]
                        self.limpiar_pantalla()
                        print(f"{term.darkorange2}MONITOREO DE ENTRADAS Y SALIDAS DIGITALES{term.normal}")
                        print("+---------+--------+---------+--------+")
                        print("| Entrada | Estado | Salida  | Estado |")
                        print("+---------+--------+---------+--------+")
                        for i in range(8):
                            print(f"| X{i:02d}     |   {entradas[i]}    | Y{i:02d}     |   {salidas[i]}    |")
                        print("+---------+--------+---------+--------+")
                        print(f"{mensaje} | Lecturas: {lecturas} | Última: {ultima}")
                        print("Presione Q, Enter o Esc para volver.")
                    tecla = term.inkey(timeout=0.1)
                    if str(tecla).lower() in ("q", "\r", "\n") or tecla.code == term.KEY_ESCAPE:
                        break
                    if not tarea.is_alive():
                        break
        finally:
            detener.set()
            tarea.join()


def main():
    menu = Menu()
    try:
        menu.mostrar_menu()
    except (KeyboardInterrupt, EOFError):
        print("\nPrograma interrumpido por el usuario.")
    finally:
        menu.desconectar_puerto_serie()


if __name__ == "__main__":
    main()

