

class Persona:

    #constructor
    def __init__(self, nombre, apellido):
        self.nombre = nombre
        self.apellido = apellido
        print("Dentro del constructor")

    def saludar(self):
        print("===================================================")
        print(f"Hola mi nombre es : {self.nombre} {self.apellido}")
        print("===================================================")
        print("\n")

    def __str__(self):
        return ""

def main():
    print("Dentro de main")

    raul = Persona("Raul", "Guzman")

    jose = Persona("José", "Vázquez")


    raul.saludar()
    jose.saludar()

if __name__ == "__main__":
    main()