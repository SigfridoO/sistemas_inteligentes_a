from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit

import sys

class Ventana(QMainWindow):

    def __init__(self):
        super().__init__()

        self.campo_texto = QTextEdit()
        self.campo_texto.setPlaceholderText("Escribe algo...")
        self.campo_texto.textChanged.connect(self.texto_cambiado)
        
        self.setCentralWidget(self.campo_texto)

        self.resize(400, 80)
        self.setWindowTitle("Mi ventana")

    def texto_cambiado(self):
        texto = self.campo_texto.toPlainText()
        print("Texto cambiado:", texto)

app = QApplication(sys.argv)
ventana = Ventana()
ventana.show()
sys.exit(app.exec())