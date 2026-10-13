class Padre:
    def __init__(self):
        print("Soy padre")

    def trabajar(self):
        print("Estoy trabajando")

class Madre:
    def __init__(self):
        print("Soy madre")

    def criar(self):
        print("Estoy cuidando")

class Hijo (Madre, Padre):
    def __init__(self):
        #super().__init__()
        Padre.__init__(self)
        Madre.__init__(self)
        print("Soy hijo")

def main ():
    print("Dentro de main")
    # padre = Padre()
    hijo = Hijo()
    hijo.trabajar()
    hijo.criar()

if __name__ == "__main__":
    main()