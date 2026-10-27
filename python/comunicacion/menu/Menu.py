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
        self.X = []
        self.Y = []

    def submenu_funciones_administrativas(self):
        while True:
            self.limpiar_pantalla()
            print(f"{term.darkorange2}=============================================================")
            print(f"{term.white}Submenú funciones administrativas")
            print(f"{term.darkorange2}============================================================={term.normal}")

            opcion = inquirer.select(
                message="Seleccione una opción:",
                choices=[
                    {"name": "Volver al menu princial", "value": "volver"},
                ],
            ).execute()

            match opcion:
                case "volver":
                    break
                    
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
                    # {"name": "Conectar puerto serie", "value": "puerto_serie_conectar"},
                    # {"name": "Desconectar puerto serie", "value": "puerto_serie_desconectar"},
                    {"name": "Puerto serie", "value": "SUBMENU_PUERTO_SERIE"},

                    {"name": "Obtener versión del programa", "value": "obtener_version"},


                    {"name": "señales digitales", "value": "submenu_senales_digitales"},

                    {"name": "Salir", "value": "salir"},
                ],
            ).execute()

            match opcion:
                case "salir":
                    print("Saliendo del programa...")
                    break
                case "SUBMENU_PUERTO_SERIE":
                    self.submenu_comunicacion_serie()
                # case "puerto_serie_conectar":
                #     self.conectar_puerto_serie()
                # case "puerto_serie_desconectar":
                #     self.desconectar_puerto_serie()

                case "submenu_senales_digitales":
                    self.submenu_senales_digitales()

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
        print(f"Respuesta recibida: {respuesta} longitud {len(respuesta)}")
        

        if respuesta and len(respuesta) > 6:
            print(f"X = {respuesta[5]},  Y = {respuesta[6]}")
            X = respuesta[5]
            Y = respuesta[6]

            for i in range(8):
                self.X.append((X >> i) & 1)

            for i in range(8):
                self.Y.append((Y >> i) & 1)

            print ("Estado de las señales")
            for i in range(8):
                print(f"| X{i:02X} = {self.X[i]} |  Y{i:02X} = {self.Y[i]}")
            
            
            



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

