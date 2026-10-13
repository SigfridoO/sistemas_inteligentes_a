from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton

import sys

class Ventana(QMainWindow):

    def __init__(self):
        super().__init__()

        mi_boton = QPushButton("Presioname")
        mi_boton.setCheckable(True)
        mi_boton.clicked.connect(self.boton_con_estado)
        # mi_boton.pressed.connect(self.boton_presionado)
        # mi_boton.released.connect(self.boton_liberado)
        # mi_boton.clicked.connect(self.boton_clicleado)
        self.setCentralWidget(mi_boton)

        self.resize(300, 100)
        self.setWindowTitle("Mi ventana")

    def boton_presionado(self):
        print("Se presiono el boton")

    def boton_liberado(self):
        print("Se libero el boton")

    def boton_clicleado(self):
        print("Se clicleo el boton")

    def boton_con_estado(self, valor):
        print(f"Se cambio el valor {valor}")

app = QApplication(sys.argv)
ventana = Ventana()
ventana.show()
sys.exit(app.exec())