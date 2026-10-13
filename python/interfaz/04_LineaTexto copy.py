from PyQt6.QtWidgets import QApplication, QMainWindow, QLineEdit

import sys

class Ventana(QMainWindow):

    def __init__(self):
        super().__init__()

        self.campo_texto = QLineEdit()
        self.campo_texto.setMaxLength(10)
        self.campo_texto.setPlaceholderText("Escribe algo...")
        self.campo_texto.textChanged.connect(self.texto_cambiado)
        self.campo_texto.returnPressed.connect(self.texto_presionado)
        
        self.setCentralWidget(self.campo_texto)

        self.resize(400, 80)
        self.setWindowTitle("Mi ventana")

    def texto_cambiado(self):
        texto = self.campo_texto.text()
        print("Texto cambiado:", texto)

    def texto_presionado(self):
        texto = self.campo_texto.text()
        self.campo_texto.clear()
        self.setWindowTitle(texto)

app = QApplication(sys.argv)
ventana = Ventana()
ventana.show()
sys.exit(app.exec())