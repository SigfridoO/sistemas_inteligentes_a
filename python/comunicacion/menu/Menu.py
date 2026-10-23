from pathlib import Path
import sys

from InquirerPy import inquirer
from blessed import Terminal

term = Terminal()

# Permite ejecutar directamente: python comunicacion/menu/Menu.py
raiz_proyecto = Path(__file__).resolve().parent.parent
if str(raiz_proyecto) not in sys.path:
    sys.path.insert(0, str(raiz_proyecto))

from uart.UART import PuertoSerie


class Menu:
    def __init__(self, puerto="/dev/ttyUSB0", baudrate=115200):
        self.puerto_serie = PuertoSerie(puerto, baudrate)

    def mostrar_menu(self):
        while True:
            print(f"{term.darkorange2}=============================================================")
            print(f"{term.white}Menu microcontroladores")
            print(f"{term.darkorange2}============================================================={term.normal}")

            opcion = inquirer.select(
                message="Seleccione una opción:",
                choices=[
                    {"name": "Conectar puerto serie", "value": "puerto_serie_conectar"},
                    {"name": "Desconectar puerto serie", "value": "puerto_serie_desconectar"},
                    {"name": "Obtener versión del programa", "value": "obtener_version"},
                    {"name": "Prender LED", "value": "prender_led"},
                    {"name": "Apagar LED", "value": "apagar_led"},

                    {"name": "Leer entradas y salidas", "value": "leer_entradas_salidas"},

                    {"name": "Salir", "value": "salir"},
                ],
            ).execute()

            match opcion:
                case "salir":
                    print("Saliendo del programa...")
                    break
                case "puerto_serie_conectar":
                    self.conectar_puerto_serie()
                case "puerto_serie_desconectar":
                    self.desconectar_puerto_serie()
                case "prender_led":
                    self.prender_led()
                case "apagar_led":
                    self.apagar_led()
                case "leer_entradas_salidas":
                    self.leer_entradas_salidas()

                case "obtener_version":
                    self.obtener_version()

    def conectar_puerto_serie(self):
        self.puerto_serie.abrir()

    def desconectar_puerto_serie(self):
        self.puerto_serie.cerrar()

    def obtener_version(self):
        if not self.puerto_serie.serial_port.is_open:
            print("Primero debes conectar el puerto serie.")
            return

        # Paquete de 100 bytes: b'&13*' seguido de 96 bytes en cero.
        arreglo_bytes = bytearray(100)
        arreglo_bytes[:4] = b"&01*"

        self.puerto_serie.escribir(arreglo_bytes, 4)
        respuesta = self.puerto_serie.leer()  # Leer el primer byte de respuesta
        print(f"Respuesta recibida: {respuesta} ")
        
    def prender_led(self):  
        if not self.puerto_serie.serial_port.is_open:
            print("Primero debes conectar el puerto serie.")
            return
        
        arreglo_bytes = bytearray(100)
        arreglo_bytes[:6] = b"&1011*"
        self.puerto_serie.escribir(arreglo_bytes, 6)

    def apagar_led(self):
        if not self.puerto_serie.serial_port.is_open:
            print("Primero debes conectar el puerto serie.")
            return

        arreglo_bytes = bytearray(100)
        arreglo_bytes[:6] = b"&1021*"
        self.puerto_serie.escribir(arreglo_bytes, 6)

    def leer_entradas_salidas(self):
        if not self.puerto_serie.serial_port.is_open:
            print("Primero debes conectar el puerto serie.")
            return

        arreglo_bytes = bytearray(100)
        arreglo_bytes[:4] = b"&12*"
        self.puerto_serie.escribir(arreglo_bytes, 4)

        respuesta = self.puerto_serie.leer()  # Leer el primer byte de respuesta
        print(f"Respuesta recibida: {respuesta} ")



def main():
    print("Bienvenido al menú de opciones")
    menu = Menu()
    try:
        menu.mostrar_menu()
    except (KeyboardInterrupt, EOFError):
        print("\nPrograma interrumpido por el usuario.")
    finally:
        menu.desconectar_puerto_serie()


if __name__ == "__main__":
    main()

