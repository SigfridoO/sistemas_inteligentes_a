from InquirerPy import inquirer
from pathlib import Path
import sys


ruta = Path(__file__).resolve().parent.parent
sys.path.append(str(ruta))

from uart.UART import PuertoSerie



def main():
    print("Bienvenido al menú de opciones")
    try:
        while True:
            opcion = inquirer.select(
                message="Seleccione una opción:",
                choices=[
                    {'name':"Conectar puerto serie", "value":"puerto_serie_conectar"},
                    {'name':"Desconectar puerto serie", "value":"puerto_serie_desconectar"},
                    {'name':"Salir", "value":"Salir"},
                ],
            ).execute()

            if opcion == "Salir":
                print("Saliendo del programa...")
                break
            else:
                print(f"Ha seleccionado: {opcion}")

    except KeyboardInterrupt:
        print("\nPrograma interrumpido por el usuario.")
      

if __name__== "__main__":
    main()
