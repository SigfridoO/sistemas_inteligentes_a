
    
  
from pathlib import Path
import sys

from InquirerPy import inquirer

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
            opcion = inquirer.select(
                message="Seleccione una opción:",
                choices=[
                    {"name": "Conectar puerto serie", "value": "puerto_serie_conectar"},
                    {"name": "Desconectar puerto serie", "value": "puerto_serie_desconectar"},
                    {"name": "Obtener versión del programa", "value": "obtener_version"},
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
        arreglo_bytes[:4] = b"&13*"

        self.puerto_serie.escribir(arreglo_bytes):
        


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

