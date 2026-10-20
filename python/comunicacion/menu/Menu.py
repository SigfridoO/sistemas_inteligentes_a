from InquirerPy import inquirer
from pathlib import Path
import sys
import struct

ruta = Path(__file__).resolve().parent.parent
sys.path.append(str(ruta))

from uart.UART import PuertoSerie



class Menu:
    def __init__(self):
        self.puerto_serie = PuertoSerie("/dev/ttyUSB0", 115200)

    def mostrar_menu(self):
        while True:
            opcion = inquirer.select(
                message="Seleccione una opción:",
                choices=[
                    {'name':"Conectar puerto serie", "value":"puerto_serie_conectar"},
                    {'name':"Desconectar puerto serie", "value":"puerto_serie_desconectar"},
                    {'name':"Obtener version del programa", "value":"obtener_version"},

                    {'name':"Salir", "value":"Salir"},
                ],
            ).execute()

            match opcion: 
                case "Salir":
                    print("Saliendo del programa...")
                    break
                case "puerto_serie_conectar":
                    self.conectar_puerto_serie()
                case "puerto_serie_desconectar":
                    self.desconectar_puerto_serie()
                case "obtener_version":
                    self.obtener_version()
                case _:
                    print(f"Ha seleccionado: {opcion}")

    def conectar_puerto_serie(self):
        self.puerto_serie.abrir()

    def desconectar_puerto_serie(self):
        self.puerto_serie.cerrar()

    def obtener_version(self):
        arreglo_bytes = bytearray()
        arreglo_bytes.append(struct.pack('c', "&"))
        arreglo_bytes.append(struct.pack('c', "1"))
        arreglo_bytes.append(struct.pack('c', "3"))
        arreglo_bytes.append(struct.pack('c', "*"))
        self.puerto_serie.escribir(arreglo_bytes)

def main():
    print("Bienvenido al menú de opciones")
    menu = Menu()

    try:
        menu.mostrar_menu()

    except KeyboardInterrupt:
        print("\nPrograma interrumpido por el usuario.")
      
if __name__== "__main__":
    main()
